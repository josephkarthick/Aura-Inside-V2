import json
import os
import platform
import re
import socket
import subprocess
import time
import uuid
from datetime import datetime, timedelta
import openpyxl
import psutil
from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.db.models import Count, Q, Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from Accounts.models import AuraInsideUser, Department
from AuraInside.utils.calc import percentage
from AuraInside.utils.dates import get_month_ranges
from .models import (
    AssetCategory,
    Invoice,
    ITAsset,
    Monitor,
    New_Tkt,
    Priority_Choice,
    Renewal,
    RenewalHeading,
    TicketHistory,
    Tkt_Cat,
    Tkt_SubCat,
    Vendor,
    VoipRecord,
)


# ============================================================
# SHARED HELPERS
# ============================================================

def get_it_departments():
    """Return both supported IT department names."""
    return Department.objects.filter(
        Q(name__iexact="Information Technology")
    )


def is_it_department_user(user):
    """Allow IT access when department OR designation identifies IT."""

    department = getattr(user, "department", None)
    designation = getattr(user, "designation", None)

    def normalise(value):
        if value is None:
            return ""

        # Supports related objects with a name or designation attribute.
        value = getattr(
            value,
            "name",
            getattr(value, "designation", value),
        )

        return str(value).strip().lower()

    allowed_names = {
        "it",
        "information technology",
    }

    return (
        normalise(department) in allowed_names
        or normalise(designation) in allowed_names
    )


def deny_non_it_user(request):
    messages.error(
        request,
        "You are not authorized to access the IT Service Desk.",
    )
    # Change "intranet" if this is not the name of your home URL.
    return redirect("intranet")


def _ticket_queryset():
    return New_Tkt.objects.select_related(
        "reported_by",
        "affected_user",
        "asset_type",
        "asset",
        "category",
        "subcategory",
        "priority",
        "assigned_to",
    )

def generate_ticket_id():
    """
    Generate ticket IDs in the format:
    ABSITTKT001, ABSITTKT002, ABSITTKT003, ...
    """
    max_id = New_Tkt.objects.aggregate(max_id=Max("id"))["max_id"] or 0
    return f"ARS-ITINC{max_id + 1:03d}"



@login_required
def raise_ticket(request):
    """Create a ticket with an automatic ticket ID."""

    categories = Tkt_Cat.objects.all().order_by("category")

    subcategories = (
        Tkt_SubCat.objects
        .select_related("category", "priority")
        .all()
        .order_by("subcategory")
    )

    priorities = Priority_Choice.objects.all().order_by("name")

    # All employees can be selected as the affected user by IT.
    employees = AuraInsideUser.objects.all().order_by("username")

    # Assigned To must include users from both IT departments.
    it_departments = get_it_departments()

    assigned_users = (
        AuraInsideUser.objects
        .filter(department__in=it_departments)
        .select_related("department")
        .order_by("username")
        .distinct()
    )

    asset_type_model = (
        New_Tkt._meta.get_field("asset_type")
        .remote_field.model
    )

    asset_types = asset_type_model.objects.all().order_by("pk")
    assets = ITAsset.objects.all().order_by("asset_tag")

    is_it_user = is_it_department_user(request.user)

    if request.method == "POST":
        try:
            category_id = request.POST.get("category")
            subcategory_id = request.POST.get("subcategory")
            priority_id = request.POST.get("priority")
            affected_user_id = request.POST.get("affected_user")
            asset_type_id = request.POST.get("asset_type")
            asset_id = request.POST.get("asset")
            description = (
                request.POST.get("description") or ""
            ).strip()

            if not all([
                category_id,
                subcategory_id,
                priority_id,
                description,
            ]):
                messages.error(
                    request,
                    "Please complete all required fields."
                )
                raise ValueError("Required fields are missing.")

            category = get_object_or_404(
                Tkt_Cat,
                pk=category_id,
            )

            subcategory = get_object_or_404(
                Tkt_SubCat,
                pk=subcategory_id,
                category=category,
            )

            priority = get_object_or_404(
                Priority_Choice,
                pk=priority_id,
            )

            # Use the logged-in employee by default.
            if is_it_user:
                affected_user = (
                    get_object_or_404(
                        AuraInsideUser,
                        pk=affected_user_id,
                    )
                    if affected_user_id
                    else request.user
                )

                assigned_to_id = (
                    request.POST.get("assigned_to") or ""
                ).strip()

                assigned_to = None

                if assigned_to_id:
                    assigned_to = get_object_or_404(
                        AuraInsideUser,
                        pk=assigned_to_id,
                        department__in=it_departments,
                    )
            else:
                # Regular employees cannot assign tickets
                # or raise tickets on behalf of others.
                affected_user = request.user
                assigned_to = None

            asset_type = (
                get_object_or_404(
                    asset_type_model,
                    pk=asset_type_id,
                )
                if asset_type_id
                else None
            )

            asset = (
                get_object_or_404(
                    ITAsset,
                    pk=asset_id,
                )
                if asset_id
                else None
            )

            # Enforce the configured subcategory priority.
            if (
                subcategory.priority_id
                and subcategory.priority_id != priority.pk
            ):
                messages.error(
                    request,
                    "The selected priority does not match "
                    "the subcategory configuration."
                )
                raise ValueError("Invalid priority selection.")

            # Generate the ID and save the ticket.
            # Retry if simultaneous requests generate a duplicate ID.
            ticket = None

            for attempt in range(3):
                try:
                    with transaction.atomic():
                        ticket_id = generate_ticket_id()

                        ticket = New_Tkt.objects.create(
                            ticket_id=ticket_id,
                            reported_by=request.user,
                            affected_user=affected_user,
                            asset_type=asset_type,
                            asset=asset,
                            category=category,
                            subcategory=subcategory,
                            priority=priority,
                            assigned_to=assigned_to,
                            description=description,
                            status="NEW",
                        )

                    break

                except IntegrityError:
                    if attempt == 2:
                        raise

            messages.success(
                request,
                f"Ticket {ticket.ticket_id} raised successfully."
            )

            return redirect("ITDesk:ticket_list")

        except ValueError:
            pass

        except Exception:
            messages.error(
                request,
                "Unable to raise the ticket. Please check "
                "the selected details and try again."
            )

    return render(
        request,
        "ITDesk/Tickets/Raise_Ticket.html",
        {
            "categories": categories,
            "subcategories": subcategories,
            "priorities": priorities,
            "employees": employees,
            "users": AuraInsideUser.objects.order_by("username"),
            "assigned_users": assigned_users,
            "it_persons": assigned_users,
            "asset_types": asset_types,
            "assets": assets,
            "logged": request.user,
            "is_it_user": is_it_user,
        },
    )




# ============================================================
# TICKETS
# Employee ticket creation is intentionally not included.
# ============================================================

@login_required
def fetch_subcategories(request):
    """Return subcategories and their default priorities for IT forms."""
    if not is_it_department_user(request.user):
        return JsonResponse({"error": "Unauthorized"}, status=403)

    category_id = request.GET.get("category_id")
    data = []

    if category_id:
        for sub in (
            Tkt_SubCat.objects
            .filter(category_id=category_id)
            .select_related("priority")
            .order_by("subcategory")
        ):
            data.append({
                "id": sub.id,
                "subcategory": sub.subcategory,
                "priority_id": sub.priority_id,
                "priority": sub.priority.name if sub.priority else "",
            })

    return JsonResponse(data, safe=False)


@login_required
def ticket_list(request):
    """
    IT / Information Technology:
        View all tickets.

    Other employees:
        View only tickets they raised.
    """

    is_it_user = is_it_department_user(request.user)

    # IT sees every ticket. Other employees see only their own.
    if is_it_user:
        tickets = _ticket_queryset()
    else:
        tickets = _ticket_queryset().filter(
            reported_by=request.user
        )

    tickets = tickets.order_by("-created_at", "-id")

    status_counts = (
        tickets.values("status")
        .annotate(count=Count("id"))
        .order_by("status")
    )

    context = {
        "tickets": tickets,
        "totaltickets": tickets.count(),
        "status_counts": status_counts,
        "is_it_user": is_it_user,
    }

    return render(
        request,
        "ITDesk/Tickets/Ticket_List.html",
        context,
    )


@login_required
def it_ticket_detail(request, ticket_id):
    """IT ticket detail, assignment, status updates, and history."""
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)

    ticket = get_object_or_404(_ticket_queryset(), ticket_id=ticket_id)

    it_departments = get_it_departments()
    it_persons = (
        AuraInsideUser.objects
        .filter(department__in=it_departments)
        .order_by("username")
    )

    # Canonical status values are uppercase. Template option values should
    # use these exact values: NEW, VIEWED, IN_PROGRESS, PENDING, ON_HOLD,
    # RESOLVED, CLOSED.
    allowed_statuses = {
        "NEW",
        "VIEWED",
        "IN_PROGRESS",
        "PENDING",
        "ON_HOLD",
        "RESOLVED",
        "CLOSED",
    }

    if request.method == "POST":
        requested_status = request.POST.get("status", "").strip()
        new_status = requested_status.upper() if requested_status else ticket.status.upper()
        assigned_to_id = request.POST.get("assigned_to", "").strip()
        notes = request.POST.get("notes", "").strip()

        if new_status not in allowed_statuses:
            messages.error(request, "Please select a valid ticket status.")
            return redirect(
                "ITDesk:it_ticket_detail",
                ticket_id=ticket.ticket_id,
            )

        if ticket.status.upper() == "CLOSED":
            messages.error(request, "Closed tickets cannot be updated.")
            return redirect(
                "ITDesk:it_ticket_detail",
                ticket_id=ticket.ticket_id,
            )

        new_assigned_user = ticket.assigned_to

        # Empty assignment means keep the current assignee. To unassign,
        # submit assigned_to="unassigned" from the form.
        if assigned_to_id == "unassigned":
            new_assigned_user = None
        elif assigned_to_id:
            new_assigned_user = get_object_or_404(
                AuraInsideUser,
                pk=assigned_to_id,
                department__in=it_departments,
            )

        previous_status = ticket.status
        previous_assignee = ticket.assigned_to
        status_changed = previous_status.upper() != new_status
        assignment_changed = previous_assignee != new_assigned_user

        if not notes and not status_changed and not assignment_changed:
            messages.info(request, "No changes were submitted.")
            return redirect(
                "ITDesk:it_ticket_detail",
                ticket_id=ticket.ticket_id,
            )

        with transaction.atomic():
            ticket.status = new_status
            ticket.assigned_to = new_assigned_user
            ticket.save(update_fields=["status", "assigned_to"])

            TicketHistory.objects.create(
                ticket=ticket,
                previous_status=previous_status,
                new_status=new_status,
                changed_by=request.user.username,
                changed_at=now(),
                assigned_to=(
                    new_assigned_user.username
                    if new_assigned_user else None
                ),
                notes=notes or None,
            )

        # Notify the assignee if an email address is available.
        if assignment_changed and new_assigned_user and new_assigned_user.email:
            try:
                send_mail(
                    subject=f"Ticket {ticket.ticket_id} assigned to you",
                    message=(
                        f"Hi {new_assigned_user.username},\n\n"
                        f"Ticket {ticket.ticket_id} has been assigned to you.\n"
                        f"Status: {ticket.status}\n"
                    ),
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                    recipient_list=[new_assigned_user.email],
                    fail_silently=True,
                )
            except Exception:
                pass

        messages.success(
            request,
            f"Ticket {ticket.ticket_id} updated successfully.",
        )
        return redirect(
            "ITDesk:it_ticket_detail",
            ticket_id=ticket.ticket_id,
        )

    
    # Automatically mark a NEW ticket as VIEWED when IT opens it.
    # Existing statuses such as IN_PROGRESS, PENDING, and RESOLVED
    # will not be changed when the ticket is opened again.
    if request.method == "GET" and ticket.status.upper() == "NEW":
        with transaction.atomic():
            ticket = New_Tkt.objects.select_for_update().get(
                pk=ticket.pk
            )

            if ticket.status.upper() == "NEW":
                previous_status = ticket.status
                viewed_at = now()

                ticket.status = "VIEWED"
                ticket.save(update_fields=["status"])

                TicketHistory.objects.create(
                    ticket=ticket,
                    previous_status=previous_status,
                    new_status="VIEWED",
                    changed_by=request.user.username,
                    changed_at=viewed_at,
                    assigned_to=(
                        ticket.assigned_to.username
                        if ticket.assigned_to
                        else None
                    ),
                    notes="Ticket automatically marked as VIEWED when opened.",
                )

    # Reload history so the newly recorded VIEWED entry appears immediately.
    history = ticket.history.all().order_by("changed_at", "id")


    return render(
        request,
        "ITDesk/Tickets/Ticket_Details.html",
        {
            "ticket": ticket,
            "Dticket": ticket,
            "history": history,
            "IT_persons": it_persons,
            "logged": request.user,
            "assigned_user": ticket.assigned_to,
            "is_it_user": True,
        },
    )


@login_required
def export_tickets_excel(request):
    """Export the full IT ticket queue and ticket history to Excel."""
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)

    tickets = _ticket_queryset().order_by("-created_at", "-id")

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Support Tickets"

    headers = [
        "Ticket ID",
        "Created Date",
        "Reported By",
        "Affected User",
        "Assigned To",
        "Asset Type",
        "Asset",
        "Category",
        "Subcategory",
        "Description",
        "Priority",
        "Status",
        "Last Resolved/Closed",
        "Resolution Time",
        "Ticket History",
    ]
    worksheet.append(headers)

    header_fill = PatternFill(fill_type="solid", fgColor="1F4E78")
    header_font = Font(color="FFFFFF", bold=True)

    for cell in worksheet[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True,
        )

    for ticket in tickets:
        description = re.sub(
            r"<[^<]+?>",
            "",
            ticket.description or "",
        )

        closed_history = (
            ticket.history
            .filter(
                new_status__in=[
                    "RESOLVED",
                    "CLOSED",
                    "Resolved",
                    "Closed",
                ]
            )
            .order_by("-changed_at")
            .first()
        )

        closed_date = ""
        resolution_time = ""

        if closed_history and ticket.created_at:
            closed_datetime = closed_history.changed_at

            if closed_datetime:
                seconds = max(
                    0,
                    int(
                        (
                            closed_datetime - ticket.created_at
                        ).total_seconds()
                    ),
                )

                days, remainder = divmod(seconds, 86400)
                hours, remainder = divmod(remainder, 3600)
                minutes, _ = divmod(remainder, 60)

                closed_date = closed_datetime.strftime(
                    "%d-%m-%Y %I:%M %p"
                )
                resolution_time = (
                    f"{days} Day(s) {hours} Hour(s) "
                    f"{minutes} Minute(s)"
                )

        asset_label = ""

        if ticket.asset:
            asset_label = " - ".join(
                value
                for value in [
                    ticket.asset.asset_tag or "",
                    ticket.asset.product_name or "",
                ]
                if value
            )

        # Collect complete ticket history into one Excel cell.
        history_entries = []

        for history in ticket.history.order_by("changed_at", "id"):
            changed_at = (
                history.changed_at.strftime("%d-%m-%Y %I:%M %p")
                if history.changed_at
                else ""
            )

            changed_by = getattr(history, "changed_by", None)
            if changed_by is None:
                changed_by = getattr(history, "user", None)

            old_status = getattr(history, "old_status", "") or ""
            new_status = getattr(history, "new_status", "") or ""

            remarks = getattr(history, "remarks", None)
            if remarks is None:
                remarks = getattr(history, "comment", "")

            history_entries.append(
                "\n".join([
                    f"Date: {changed_at}",
                    f"Changed By: {changed_by or ''}",
                    f"Old Status: {old_status}",
                    f"New Status: {new_status}",
                    f"Remarks: {remarks or ''}",
                    "-" * 30,
                ])
            )

        history_text = (
            "\n".join(history_entries)
            if history_entries
            else "No history available."
        )

        worksheet.append([
            ticket.ticket_id or "",
            (
                ticket.created_at.strftime("%d-%m-%Y %I:%M %p")
                if ticket.created_at
                else ""
            ),
            str(ticket.reported_by) if ticket.reported_by else "",
            str(ticket.affected_user) if ticket.affected_user else "",
            str(ticket.assigned_to) if ticket.assigned_to else "Unassigned",
            ticket.asset_type.name if ticket.asset_type else "",
            asset_label,
            ticket.category.category if ticket.category else "",
            ticket.subcategory.subcategory if ticket.subcategory else "",
            description,
            ticket.priority.name if ticket.priority else "",
            ticket.status or "",
            closed_date,
            resolution_time,
            history_text,
        ])

        # Wrap long text in the Description and Ticket History columns.
        current_row = worksheet.max_row

        worksheet.cell(
            row=current_row,
            column=10,
        ).alignment = Alignment(vertical="top", wrap_text=True)

        worksheet.cell(
            row=current_row,
            column=15,
        ).alignment = Alignment(vertical="top", wrap_text=True)

    # Auto-adjust column widths.
    for column_cells in worksheet.columns:
        max_length = max(
            (
                len(str(cell.value))
                for cell in column_cells
                if cell.value is not None
            ),
            default=0,
        )

        col_letter = get_column_letter(column_cells[0].column)

        worksheet.column_dimensions[col_letter].width = min(
            max_length + 3,
            55,
        )

    # Give the history column enough width to read comfortably.
    worksheet.column_dimensions["O"].width = 55

    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    response["Content-Disposition"] = (
        'attachment; filename="Support_Tickets_Report.xlsx"'
    )

    workbook.save(response)
    return response



# ============================================================
# DASHBOARD
# ============================================================

@login_required
def it_dashboard(request):
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)

    ranges = get_month_ranges()
    time_threshold = now() - timedelta(hours=42)

    overdue_tickets = New_Tkt.objects.exclude(
        status__in=["RESOLVED", "CLOSED", "Resolved", "Closed"]
    ).filter(created_at__lte=time_threshold)

    current_month = New_Tkt.objects.filter(
        created_at__gte=ranges["start_current_month"]
    )
    last_month = New_Tkt.objects.filter(
        created_at__gte=ranges["start_last_month"],
        created_at__lte=ranges["end_last_month"],
    )

    cm_total = current_month.count()
    lm_total = last_month.count()

    rows = current_month.values(
        "category__category", "status"
    ).annotate(count=Count("id"))

    chart_data = {}
    for row in rows:
        category_name = row["category__category"] or "Uncategorized"
        status = (row["status"] or "Unknown").upper()
        chart_data.setdefault(category_name, {"Open": 0, "Closed": 0})
        if status == "CLOSED":
            chart_data[category_name]["Closed"] += row["count"]
        else:
            chart_data[category_name]["Open"] += row["count"]

    cm_by_user = current_month.values(
        "assigned_to__username"
    ).annotate(ticket_count=Count("id")).order_by("assigned_to__username")

    lm_by_user = last_month.values(
        "assigned_to__username"
    ).annotate(ticket_count=Count("id")).order_by("assigned_to__username")

    return render(
        request,
        "ITDesk/Dashboard.html",
        {
            "cm_total_tickets": cm_total,
            "lm_total_tickets": lm_total,
            "ticket_change_percent": percentage(cm_total, lm_total),
            "chart_categories": list(chart_data.keys()),
            "chart_open_series": [chart_data[key]["Open"] for key in chart_data],
            "chart_closed_series": [chart_data[key]["Closed"] for key in chart_data],
            "cm_ticket_by_user": cm_by_user,
            "lm_ticket_by_user": lm_by_user,
            "tickets": overdue_tickets,
        },
    )


# ============================================================
# RENEWALS
# ============================================================

@login_required
def view_renewals(request):
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)

    headings = RenewalHeading.objects.prefetch_related("renewals").all()
    return render(request, "ITDesk/Renewals.html", {"headings": headings})


# ============================================================
# SYSTEM INFORMATION
# ============================================================

@login_required
def system_info(request):
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)

    context = {}
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.connect(("8.8.8.8", 80))
            server_ip = sock.getsockname()[0]
        finally:
            sock.close()

        logged_user = subprocess.run(
            ["whoami"], capture_output=True, text=True, shell=True
        ).stdout.strip()
        os_name = platform.system()
        os_arch = platform.machine()

        if os_name == "Windows":
            win_ver = platform.win32_ver()
            os_version = f"Windows {win_ver[0]}"
            activation_status = subprocess.run(
                ["cscript", "//Nologo", r"C:\Windows\System32\slmgr.vbs", "/xpr"],
                capture_output=True, text=True, shell=True,
            ).stdout.strip()
            product_key = subprocess.run(
                [
                    "powershell", "-Command",
                    "(Get-WmiObject -query 'select * from SoftwareLicensingService').OA3xOriginalProductKey",
                ],
                capture_output=True, text=True, shell=True,
            ).stdout.strip() or "Not found"
        else:
            os_version = platform.version()
            activation_status = "N/A"
            product_key = "N/A"

        context.update({
            "server_ip": server_ip,
            "logged_in_user": logged_user,
            "server_hostname": socket.gethostname(),
            "os_name": os_name,
            "os_version": os_version,
            "os_arch": os_arch,
            "cpu_count": psutil.cpu_count(logical=False),
            "cpu_threads": psutil.cpu_count(logical=True),
            "cpu_freq": psutil.cpu_freq().current if psutil.cpu_freq() else "N/A",
            "total_memory": psutil.virtual_memory().total,
            "available_memory": psutil.virtual_memory().available,
            "used_memory": psutil.virtual_memory().used,
            "total_disk": psutil.disk_usage(os.path.abspath(os.sep)).total,
            "used_disk": psutil.disk_usage(os.path.abspath(os.sep)).used,
            "free_disk": psutil.disk_usage(os.path.abspath(os.sep)).free,
            "uptime": time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(psutil.boot_time()),
            ),
            "activation_status": activation_status,
            "product_key": product_key,
        })
    except Exception as exc:
        context["error"] = str(exc)

    return render(request, "ITDesk/system_info.html", context)


# ============================================================
# ASSET AGENT API
# ============================================================

@csrf_exempt
def receive_asset_info(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        data = json.loads(request.body or b"{}")
        hostname = (data.get("hostname") or "").strip()
        if not hostname:
            return JsonResponse({"error": "Hostname is required"}, status=400)

        with transaction.atomic():
            asset, created = ITAsset.objects.update_or_create(
                hostname=hostname,
                defaults={
                    "processor": data.get("processor"),
                    "ram_gb": data.get("ram_gb"),
                    "hdd_gb": data.get("hdd_gb"),
                    "free_disk_gb": data.get("free_disk_gb"),
                    "serial_number": data.get("serial_number"),
                    "os_installed": data.get("os_installed"),
                    "windows_key_last5": data.get("windows_key_last5"),
                    "windows_license_status": data.get("windows_license_status"),
                    "license_type": data.get("license_type"),
                    "logged_in_user": data.get("logged_in_user"),
                    "ip_address": data.get("ip_address"),
                    "mac_address": data.get("mac_address"),
                    "manufacturer": data.get("manufacturer"),
                    "model": data.get("model"),
                    "bios_version": data.get("bios_version"),
                    "system_type": data.get("system_type"),
                    "domain_name": data.get("domain_name"),
                },
            )

            monitors = data.get("monitors") or []
            Monitor.objects.filter(asset=asset).delete()
            for index, monitor_data in enumerate(monitors, start=1):
                Monitor.objects.create(
                    asset=asset,
                    monitor_number=monitor_data.get("monitor_number", index),
                    manufacturer=monitor_data.get("manufacturer"),
                    model=monitor_data.get("model"),
                    serial_number=monitor_data.get("serial_number"),
                    resolution=monitor_data.get("resolution"),
                    refresh_rate=monitor_data.get("refresh_rate"),
                )

        return JsonResponse({
            "status": "success",
            "created": created,
            "asset_id": asset.id,
            "hostname": asset.hostname,
            "monitor_count": len(monitors),
        })
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except (TypeError, ValueError) as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    except Exception:
        return JsonResponse({"error": "Unable to process asset information"}, status=500)


# ============================================================
# VENDORS
# ============================================================

@login_required
def addvendor(request):
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)

    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        if not name:
            messages.error(request, "Vendor name is required.")
        else:
            vendor = Vendor.objects.create(
                name=name,
                gst_number=request.POST.get("gst_number") or None,
                address=request.POST.get("address") or None,
                contact_number=request.POST.get("contact_number") or None,
                email=request.POST.get("email") or None,
            )
            messages.success(request, f"Vendor '{vendor.name}' added successfully.")
            return redirect("ITDesk:vendor_list")

    return render(request, "itdesk/Asset/add_vendor.html")


@login_required
def vendor_list(request):
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)
    vendors = Vendor.objects.all().order_by("name")
    return render(request, "itdesk/Asset/vendor_list.html", {"vendors": vendors})


@login_required
def deletevendor(request, pk):
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)
    vendor = get_object_or_404(Vendor, pk=pk)
    vendor_name = vendor.name
    if request.method != "POST":
        messages.error(request, "Use the delete form to remove a vendor.")
        return redirect("ITDesk:vendor_list")
    vendor.delete()
    messages.success(request, f"Vendor '{vendor_name}' deleted.")
    return redirect("ITDesk:vendor_list")


# ============================================================
# INVOICES
# ============================================================

@login_required
def addinvoice(request):
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)

    vendors = Vendor.objects.all().order_by("name")

    if request.method == "POST":
        invoice_no = (request.POST.get("invoice_number") or "").strip()
        vendor_id = request.POST.get("vendor")
        purchase_date = request.POST.get("invoice_date")
        total_amount = request.POST.get("amount")
        remarks = request.POST.get("remarks")
        uploaded_copy = request.FILES.get("invoice_copy")

        if uploaded_copy and not uploaded_copy.name.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):
            messages.error(request, "Only JPG, JPEG, and PNG files are allowed.")
            return redirect("ITDesk:addinvoice")

        if not all([invoice_no, vendor_id, purchase_date, total_amount]):
            messages.error(request, "Invoice number, vendor, date, and amount are required.")
        else:
            try:
                vendor = get_object_or_404(Vendor, pk=vendor_id)
                invoice = Invoice.objects.create(
                    invoice_no=invoice_no,
                    vendor=vendor,
                    date_of_purchase=datetime.strptime(
                        purchase_date, "%Y-%m-%d"
                    ).date(),
                    total_amount=total_amount,
                    remarks=remarks,
                    uploaded_copy=uploaded_copy,
                )
                messages.success(
                    request,
                    f"Invoice '{invoice.invoice_no}' added successfully.",
                )
                return redirect("ITDesk:invoice_list")
            except IntegrityError:
                messages.error(request, f"Invoice number '{invoice_no}' already exists.")
            except (ValueError, TypeError):
                messages.error(request, "Please enter a valid date and amount.")

    return render(request, "itdesk/Asset/add_invoice.html", {"vendors": vendors})


@login_required
def invoice_list(request):
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)
    invoices = Invoice.objects.select_related("vendor").order_by("-date_of_purchase")
    return render(request, "itdesk/Asset/invoice_list.html", {"invoices": invoices})


@login_required
def deleteinvoice(request, pk):
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice_no = invoice.invoice_no
    if request.method != "POST":
        messages.error(request, "Use the delete form to remove an invoice.")
        return redirect("ITDesk:invoice_list")
    invoice.delete()
    messages.success(request, f"Invoice '{invoice_no}' deleted.")
    return redirect("ITDesk:invoice_list")


# ============================================================
# ASSETS
# ============================================================

@login_required
def add_asset(request):
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)

    categories = AssetCategory.objects.order_by("name")
    invoices = Invoice.objects.order_by("-date_of_purchase")

    if request.method == "POST":
        asset_tag = (request.POST.get("asset_tag") or "").strip()
        product_name = (request.POST.get("product_name") or "").strip()
        category_id = request.POST.get("category")
        invoice_id = request.POST.get("invoice")

        if not asset_tag or not product_name:
            messages.error(request, "Asset Tag and Product Name are required.")
        else:
            try:
                ITAsset.objects.create(
                    asset_tag=asset_tag,
                    product_name=product_name,
                    category=get_object_or_404(AssetCategory, pk=category_id) if category_id else None,
                    invoice=get_object_or_404(Invoice, pk=invoice_id) if invoice_id else None,
                    warranty_expiry=request.POST.get("warranty_expiry") or None,
                    location=request.POST.get("location") or None,
                    remarks=request.POST.get("remarks") or None,
                    status=request.POST.get("status") or "in_stock",
                    hostname=request.POST.get("hostname") or None,
                    serial_number=request.POST.get("serial_number") or None,
                    brand=request.POST.get("brand") or None,
                    model=request.POST.get("model") or None,
                )
                messages.success(request, f"Asset '{asset_tag}' added successfully.")
                return redirect("ITDesk:assetlist")
            except IntegrityError:
                messages.error(request, "Asset tag or hostname already exists.")
            except Exception as exc:
                messages.error(request, f"Unable to add asset: {exc}")

    return render(
        request,
        "itdesk/Asset/add_asset.html",
        {"categories": categories, "invoices": invoices},
    )


@login_required
def asset_list(request):
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)

    selected_status = request.GET.get("status", "all")
    assets = (
        ITAsset.objects
        .select_related("category", "invoice")
        .order_by("-created_at")
    )
    valid_statuses = {value for value, label in ITAsset.STATUS_CHOICES}
    if selected_status != "all" and selected_status in valid_statuses:
        assets = assets.filter(status=selected_status)
    elif selected_status != "all":
        selected_status = "all"

    for asset in assets:
        asset.invoice_file_exists = bool(
            asset.invoice
            and asset.invoice.uploaded_copy
            and asset.invoice.uploaded_copy.name
            and os.path.exists(
                os.path.join(settings.MEDIA_ROOT, asset.invoice.uploaded_copy.name)
            )
        )

    return render(
        request,
        "itdesk/Asset/asset_list.html",
        {
            "assets": assets,
            "selected_status": selected_status,
            "total_assets": ITAsset.objects.count(),
            "managed_count": ITAsset.objects.filter(category__is_managed=True).count(),
            "non_managed_count": ITAsset.objects.filter(category__is_managed=False).count(),
            "in_use_count": ITAsset.objects.filter(status="in_use").count(),
            "in_stock_count": ITAsset.objects.filter(status="in_stock").count(),
            "repair_count": ITAsset.objects.filter(status="repair").count(),
            "damaged_count": ITAsset.objects.filter(status="damaged").count(),
            "disposed_count": ITAsset.objects.filter(status="disposed").count(),
        },
    )


@login_required
def edit_asset(request, asset_id):
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)

    asset = get_object_or_404(ITAsset, pk=asset_id)
    categories = AssetCategory.objects.order_by("name")
    invoices = Invoice.objects.order_by("-date_of_purchase")

    if request.method == "POST":
        asset_tag = (request.POST.get("asset_tag") or "").strip()
        product_name = (request.POST.get("product_name") or "").strip()
        if not asset_tag or not product_name:
            messages.error(request, "Asset Tag and Product Name are required.")
        else:
            asset.asset_tag = asset_tag
            asset.product_name = product_name
            asset.serial_number = request.POST.get("serial_number") or None
            asset.model = request.POST.get("model") or None
            asset.brand = request.POST.get("brand") or None
            asset.warranty_expiry = request.POST.get("warranty_expiry") or None
            asset.location = request.POST.get("location") or None
            asset.remarks = request.POST.get("remarks") or None
            asset.status = request.POST.get("status") or "in_stock"
            asset.hostname = request.POST.get("hostname") or None
            category_id = request.POST.get("category")
            invoice_id = request.POST.get("invoice")
            asset.category = get_object_or_404(AssetCategory, pk=category_id) if category_id else None
            asset.invoice = get_object_or_404(Invoice, pk=invoice_id) if invoice_id else None
            try:
                asset.save()
                messages.success(request, f"Asset '{asset.asset_tag}' updated successfully.")
                return redirect("ITDesk:assetlist")
            except IntegrityError:
                messages.error(request, "Asset tag or hostname already exists.")

    return render(
        request,
        "itdesk/Asset/edit_asset.html",
        {"asset": asset, "categories": categories, "invoices": invoices},
    )


@login_required
def delete_asset(request, asset_id):
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)
    asset = get_object_or_404(ITAsset, pk=asset_id)
    if request.method != "POST":
        messages.error(request, "Use the delete form to remove an asset.")
        return redirect("ITDesk:assetlist")
    asset.delete()
    messages.success(request, "Asset deleted successfully.")
    return redirect("ITDesk:assetlist")


# ============================================================
# VOIP
# ============================================================

@login_required
def add_voip(request):
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)

    vendors = Vendor.objects.order_by("name")
    employeeid = AuraInsideUser.objects.order_by("username")

    if request.method == "POST":
        try:
            vendor = get_object_or_404(Vendor, pk=request.POST.get("vendor"))
            emp_value = request.POST.get("empid")
            if emp_value == "free":
                empid = None
                is_free = True
            elif emp_value:
                empid = get_object_or_404(AuraInsideUser, pk=emp_value)
                is_free = False
            else:
                empid = None
                is_free = False

            VoipRecord.objects.create(
                vendor=vendor,
                callback_number=request.POST.get("callback_number", "").strip(),
                username=request.POST.get("username", "").strip(),
                password=request.POST.get("password", ""),
                domain=request.POST.get("domain", "").strip(),
                cdr_id=request.POST.get("cdr_id") or None,
                empid=empid,
                is_free=is_free,
            )
            messages.success(request, "VoIP record added successfully.")
            return redirect("ITDesk:list_voip")
        except Exception as exc:
            messages.error(request, f"Unable to add VoIP record: {exc}")

    return render(
        request,
        "itdesk/Voip/Voip_add.html",
        {"vendors": vendors, "employeeid": employeeid},
    )


def list_voip(request):
    voip_list = VoipRecord.objects.select_related(
        'vendor', 'empid'
    ).order_by('-id')

    voip_count = voip_list.count()

    # Check user's Department / Designation
    can_edit = False

    if request.user.is_authenticated:
        department = getattr(request.user, 'department', None)
        designation = getattr(request.user, 'designation', None)

        if department:
            department_name = str(department).strip().lower()
            if department_name in ['it', 'information technology']:
                can_edit = True

        if designation:
            designation_name = str(designation).strip().lower()
            if designation_name in ['it', 'information technology']:
                can_edit = True

    context = {
        "voip_list": voip_list,
        "voip_count": voip_count,
        "can_edit": can_edit,
    }

    return render(request, "itdesk/Voip/Voip_list.html", context)


@login_required
def edit_voip(request, pk):
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)

    voip = get_object_or_404(VoipRecord, pk=pk)
    vendors = Vendor.objects.order_by("name")
    employeeid = AuraInsideUser.objects.order_by("username")

    if request.method == "POST":
        try:
            voip.vendor = get_object_or_404(Vendor, pk=request.POST.get("vendor"))
            emp_value = request.POST.get("empid")
            if emp_value == "free":
                voip.empid = None
                voip.is_free = True
            elif emp_value:
                voip.empid = get_object_or_404(AuraInsideUser, pk=emp_value)
                voip.is_free = False
            else:
                voip.empid = None
                voip.is_free = False

            voip.callback_number = request.POST.get("callback_number", "").strip()
            voip.username = request.POST.get("username", "").strip()
            voip.password = request.POST.get("password", "")
            voip.domain = request.POST.get("domain", "").strip()
            voip.cdr_id = request.POST.get("cdr_id") or None
            voip.save()
            messages.success(request, "VoIP record updated successfully.")
            return redirect("ITDesk:list_voip")
        except Exception as exc:
            messages.error(request, f"Unable to update VoIP record: {exc}")

    return render(
        request,
        "itdesk/Voip/Edit_Voip_sheet.html",
        {
            "voip": voip,
            "vendors": vendors,
            "employeeid": employeeid,
            "is_edit": True,
        },
    )


@login_required
def export_voip_excel(request):
    if not is_it_department_user(request.user):
        return deny_non_it_user(request)

    voip_model = apps.get_model("ITDesk", "VoipRecord")
    records = voip_model.objects.select_related("vendor", "empid").all()

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "VoIP Records"

    fields = voip_model._meta.fields
    sheet.append([field.verbose_name.title() for field in fields])

    for obj in records:
        row = []
        for field in fields:
            value = getattr(obj, field.name)
            if field.is_relation and value is not None:
                value = str(value)
            row.append(value)
        sheet.append(row)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="voip_full_report.xlsx"'
    workbook.save(response)
    return response
