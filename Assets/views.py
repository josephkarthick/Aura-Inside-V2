
import json
import secrets
import logging

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .services.cpu import sync_desktop_info
from .services.monitor import sync_monitor_info
from .models import DesktopAsset, Monitor, ComputerUserHistory


logger = logging.getLogger(__name__)


# ============================================================
# COMMON AGENT TOKEN VALIDATION
# ============================================================

def validate_agent_token(request):

    expected_token = getattr(
        settings,
        "DESKTOP_AGENT_API_TOKEN",
        None
    )

    received_token = request.headers.get(
        "X-Agent-Token",
        ""
    )

    return bool(
        expected_token
        and received_token
        and secrets.compare_digest(
            str(expected_token),
            str(received_token)
        )
    )


# ============================================================
# RECEIVE COMPUTER HARDWARE INFORMATION
# ============================================================

@csrf_exempt
@require_POST
def receive_desktop_info(request):

    if not validate_agent_token(request):
        return JsonResponse({
            "success": False,
            "message": "Unauthorized agent."
        }, status=401)

    try:
        data = json.loads(request.body)

        if not isinstance(data, dict):
            raise ValueError("Invalid JSON")

    except (json.JSONDecodeError, ValueError):
        return JsonResponse({
            "success": False,
            "message": "Invalid JSON data."
        }, status=400)

    if not str(data.get("hostname") or "").strip():
        return JsonResponse({
            "success": False,
            "message": "Hostname is required."
        }, status=400)

    try:
        result = sync_desktop_info(data)

        return JsonResponse(result, status=200)

    except Exception:
        logger.exception(
            "Computer hardware synchronization failed"
        )

        return JsonResponse({
            "success": False,
            "message": "Computer synchronization failed."
        }, status=500)


# ============================================================
# RECEIVE MONITOR INFORMATION
# ============================================================

@csrf_exempt
@require_POST
def receive_monitor_info(request):

    if not validate_agent_token(request):
        return JsonResponse({
            "status": "error",
            "message": "Invalid agent token."
        }, status=401)

    return sync_monitor_info(request)


# ============================================================
# COMPUTER / DESKTOP LIST
# ============================================================

def desktop_list(request):

    search = request.GET.get("search", "").strip()

    desktops = DesktopAsset.objects.select_related(
        "asset"
    ).filter(
        asset_type__iexact="Desktop"
    )

    if search:
        desktops = desktops.filter(
            Q(hostname__icontains=search) |
            Q(asset_type__icontains=search) |
            Q(processor__icontains=search) |
            Q(os_installed__icontains=search) |
            Q(logged_in_user__icontains=search) |
            Q(ip_address__icontains=search) |
            Q(asset__asset_tag__icontains=search)
        )

    return render(request, "Assets/desktop_list.html", {
        "desktops": desktops,
        "search_term": search,
        "total_desktops": desktops.count(),
    })


# ============================================================
# COMPUTER DETAIL
# ============================================================

from django.shortcuts import get_object_or_404, render

from .models import (
    DesktopAsset,
    Monitor,
    ComputerUserHistory,
)

from Accounts.models import SecurityGroup
from SpaceView.models import Workstation


def desktop_detail(request, pk):

    desktop = get_object_or_404(
        DesktopAsset.objects.select_related('asset'),
        pk=pk
    )

    asset = desktop.asset

    # --------------------------------------------------------
    # MONITORS
    # --------------------------------------------------------

    monitors = Monitor.objects.filter(
        hostname__iexact=desktop.hostname
    ).order_by('monitor_id')

    # --------------------------------------------------------
    # OFFICIAL ASSIGNMENT HISTORY
    # --------------------------------------------------------

    assignments = asset.assignment_history.select_related(
        'employee',
        'assigned_by'
    ).all()

    # --------------------------------------------------------
    # AUTOMATICALLY DETECTED WINDOWS USER HISTORY
    # --------------------------------------------------------

    detected_users = ComputerUserHistory.objects.filter(
        computer_id=desktop.pk
    ).select_related(
        'employee'
    ).order_by('-first_seen')

    # --------------------------------------------------------
    # PROJECT DROPDOWNS
    # --------------------------------------------------------

    projects = list(
        SecurityGroup.objects
        .exclude(project__isnull=True)
        .exclude(project__exact='')
        .values_list('project', flat=True)
        .distinct()
        .order_by('project')
    )

    # --------------------------------------------------------
    # WORKSTATION DROPDOWN
    # --------------------------------------------------------

    workstations = list(
        Workstation.objects.filter(
            is_active=True
        ).order_by('workstation_code')
    )

    workstation_codes = [
        ws.workstation_code for ws in workstations
    ]

    # --------------------------------------------------------
    # CONTEXT
    # --------------------------------------------------------

    context = {
        'desktop': desktop,
        'asset': asset,
        'monitors': monitors,
        'assignments': assignments,
        'detected_users': detected_users,

        # Asset edit modal
        'projects': projects,
        'workstations': workstations,
        'workstation_codes': workstation_codes,
    }

    return render(
        request,
        'Assets/desktop_detail.html',
        context
    )
    
    
from decimal import Decimal, InvalidOperation
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import DesktopAsset


@require_POST
def update_desktop_asset(request, pk):

    desktop = get_object_or_404(
        DesktopAsset.objects.select_related('asset'),
        pk=pk
    )

    asset = desktop.asset

    try:
        asset.asset_name = request.POST.get('asset_name', '').strip()
        asset.manufacturer = request.POST.get('manufacturer', '').strip() or None
        asset.model = request.POST.get('model', '').strip() or None
        asset.serial_number = request.POST.get('serial_number', '').strip() or None

        purchase_date = request.POST.get('purchase_date', '').strip()
        warranty_start = request.POST.get('warranty_start', '').strip()
        warranty_end = request.POST.get('warranty_end', '').strip()

        asset.purchase_date = parse_date(purchase_date) if purchase_date else None
        asset.warranty_start = parse_date(warranty_start) if warranty_start else None
        asset.warranty_end = parse_date(warranty_end) if warranty_end else None

        cost = request.POST.get('purchase_cost', '').strip()
        asset.purchase_cost = Decimal(cost) if cost else None

        asset.assigned_day_project = (
            request.POST.get('assigned_day_project', '').strip() or None
        )

        asset.assigned_night_project = (
            request.POST.get('assigned_night_project', '').strip() or None
        )

        asset.workstation = (
            request.POST.get('workstation', '').strip() or None
        )

        asset.location = request.POST.get('location', '').strip() or None
        asset.description = request.POST.get('description', '').strip() or None

        new_status = request.POST.get('status', '')

        valid_statuses = dict(asset.STATUS_CHOICES)

        if new_status not in valid_statuses:
            raise ValueError("Invalid asset status.")

        asset.status = new_status

        if not asset.asset_name:
            raise ValueError("Asset name is required.")

        if asset.purchase_cost is not None and asset.purchase_cost < 0:
            raise ValueError("Purchase cost cannot be negative.")

        if purchase_date and asset.purchase_date is None:
            raise ValueError("Invalid purchase date.")

        if warranty_start and asset.warranty_start is None:
            raise ValueError("Invalid warranty start date.")

        if warranty_end and asset.warranty_end is None:
            raise ValueError("Invalid warranty end date.")

        if asset.warranty_start and asset.warranty_end:
            if asset.warranty_end < asset.warranty_start:
                raise ValueError("Warranty end cannot precede warranty start.")

        asset.save()

        messages.success(request, "Asset information updated successfully.")

    except (ValueError, InvalidOperation, TypeError) as e:
        messages.error(request, str(e))

    return redirect('Assets:desktop_detail', pk=desktop.pk)    



# ============================================================
# MONITOR LIST
# ============================================================

def monitor_list(request):

    search = request.GET.get("search", "").strip()

    monitors = Monitor.objects.all()

    if search:
        monitors = monitors.filter(
            Q(hostname__icontains=search) |
            Q(monitor_id__icontains=search) |
            Q(manufacturer__icontains=search) |
            Q(model__icontains=search) |
            Q(serial_number__icontains=search)
        )

    return render(request, "Assets/monitor_list.html", {
        "monitors": monitors,
        "search_term": search,
        "total_monitors": monitors.count(),
    })
