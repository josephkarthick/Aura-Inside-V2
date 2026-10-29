import os
import uuid
import pandas as pd
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from CDR.services.importer import FileImporter
from CDR.services.parser import CommonParser
from CDR.services.datetime import DateTimeService
from CDR.services.duration import DurationService
from CDR.services.employee import EmployeeService
from CDR.services.automap import AutoMapper
from datetime import datetime, timedelta
from django.contrib import messages
from django.shortcuts import redirect
from CDR.models import CallLog, Vendor
from Accounts.models import AuraInsideUser
from django.contrib.auth.decorators import login_required
from openpyxl import Workbook
from django.http import HttpResponse
from openpyxl.utils import get_column_letter
from collections import OrderedDict
from .reports import hourly_report
from django.http import HttpResponse
from django.db.models import Count, Sum, Min
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

COMMON_FIELDS = [
    {"name": "from_number", "label": "From Number"},
    {"name": "to_number", "label": "To Number"},
    {"name": "call_datetime", "label": "Date & Time"},
    {"name": "duration", "label": "Duration (Seconds)"},
    {"name": "call_status", "label": "Call Status"},
]
    
@login_required
def import_cdr(request):

    if request.method == "POST":

        uploads = {
            "SIPLINK": request.FILES.get("siplink_file"),
            "SKYFALL": request.FILES.get("skyfall_file"),
            "UNIFIED": request.FILES.get("unified_file"),
            "PULSE": request.FILES.get("pulse_file"),
        }

        # ==========================================================
        # UPLOAD FOLDER
        # ==========================================================

        upload_folder = os.path.join(
            settings.MEDIA_ROOT,
            "cdr_imports"
        )

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        storage = FileSystemStorage(
            location=upload_folder
        )

        uploaded_files = {}
        vendors = []

        # ==========================================================
        # PROCESS EACH VENDOR
        # ==========================================================

        for vendor_name, file in uploads.items():

            if not file:
                continue

            try:

                # ==================================================
                # SAVE UPLOADED FILE
                # ==================================================

                filename = f"{uuid.uuid4()}_{file.name}"

                saved_name = storage.save(
                    filename,
                    file
                )

                full_path = storage.path(
                    saved_name
                )

                uploaded_files[vendor_name] = full_path

                # ==================================================
                # READ ONLY COLUMN HEADERS
                #
                # IMPORTANT:
                # Do NOT read the complete CSV here.
                #
                # Pulse contains a malformed row around line 520.
                # We only need the header for the mapping screen.
                # ==================================================

                if file.name.lower().endswith(".csv"):

                    df = pd.read_csv(
                        full_path,
                        dtype=str,
                        keep_default_na=False,
                        nrows=0
                    )

                else:

                    df = pd.read_excel(
                        full_path,
                        dtype=str,
                        keep_default_na=False,
                        nrows=0
                    )

                # ==================================================
                # GET COLUMNS
                # ==================================================

                columns = list(df.columns)

                # ==================================================
                # AUTO MAPPING
                # ==================================================

                mapping = AutoMapper.detect(
                    columns
                )

                # ==================================================
                # ADD VENDOR
                # ==================================================

                vendors.append({

                    "name": vendor_name,

                    "columns": columns,

                    "mapping": mapping,

                })

            except Exception as e:

                # ==================================================
                # ERROR
                # ==================================================

                print(
                    f"{vendor_name} Import Error: {e}"
                )

                vendors.append({

                    "name": vendor_name,

                    "columns": [
                        f"ERROR : {e}"
                    ],

                    "mapping": {},

                })

        # ==========================================================
        # SAVE FILE PATHS IN SESSION
        # ==========================================================

        request.session[
            "cdr_uploaded_files"
        ] = uploaded_files

        # ==========================================================
        # MAPPING PAGE
        # ==========================================================

        return render(

            request,

            "CDR/mapping.html",

            {
                "vendors": vendors,
                "common_fields": COMMON_FIELDS,
            },

        )

    # ==============================================================
    # GET REQUEST
    # ==============================================================

    return render(

        request,

        "CDR/import.html",

    )

@login_required
def generate_cdr(request):

    uploaded_files = request.session.get(
        "cdr_uploaded_files",
        {}
    )

    preview_rows = []
    all_rows = []

    for vendor, path in uploaded_files.items():

        if not os.path.exists(path):
            continue

        df = FileImporter.read(path)

        auto_mapping = AutoMapper.detect(
            df.columns
        )

        mapping = {
        
            "from_number": (
                request.POST.get(
                    f"{vendor}__from_number"
                )
                or auto_mapping["from_number"]
            ),
        
            "to_number": (
                request.POST.get(
                    f"{vendor}__to_number"
                )
                or auto_mapping["to_number"]
            ),
        
            "call_datetime": (
                request.POST.get(
                    f"{vendor}__call_datetime"
                )
                or auto_mapping["call_datetime"]
            ),
        
            "duration": (
                request.POST.get(
                    f"{vendor}__duration"
                )
                or auto_mapping["duration"]
            ),
        
            "call_status": (
                request.POST.get(
                    f"{vendor}__call_status"
                )
                or auto_mapping["call_status"]
            ),
        
            "direction": auto_mapping.get(
                "direction",
                ""
            ),
        }

        # ==========================================================
        # PARSE ALL ROWS
        # ==========================================================

        vendor_rows = []

        for _, row in df.iterrows():

            parsed = CommonParser.parse(
                vendor=vendor,
                row=row,
                mapping=mapping,
                datetime_service=DateTimeService,
                duration_service=DurationService,
                employee_service=EmployeeService,
            )

            vendor_rows.append(parsed)
            all_rows.append(parsed)

        # ==========================================================
        # FIRST 20 ROWS FOR PREVIEW
        # ==========================================================

        preview_rows.extend(
            vendor_rows[:20]
        )

    # ==============================================================
    # SAVE ALL ROWS
    # ==============================================================

    request.session["cdr_all_rows"] = all_rows

    return render(
        request,
        "CDR/preview.html",
        {
            "preview_rows": preview_rows,
        },
    )

def import_to_database(request):

    all_rows = request.session.get("cdr_all_rows", [])

    imported = 0
    skipped = 0
    errors = 0

    for row in all_rows:
    
        # Skip rows with 0 duration
        if int(row.get("duration_seconds", 0)) == 0:
            skipped += 1
            continue
    
        try:
    
            # Convert Date
            call_date = datetime.strptime(
                row["date"],
                "%d-%m-%Y"
            ).date()
    
            # Convert EST Time
            est_time = datetime.strptime(
                row["est_time"],
                "%I:%M:%S %p"
            ).time()
    
            # Convert IST Time
            ist_time = datetime.strptime(
                row["ist_time"],
                "%I:%M:%S %p"
            ).time()
    
            # Skip duplicate
            if CallLog.objects.filter(
                vendor=row["vendor"],
                employee_id=row["employee_id"],
                source=row["from"],
                destination=row["to"],
                call_date=call_date,
                ist_time=ist_time,
                duration_seconds=row["duration_seconds"],
            ).exists():
    
                skipped += 1
                continue
    
            CallLog.objects.create(
                vendor=row["vendor"],
                employee_id=row["employee_id"],
                employee_name=row["employee"],
                source=row["from"],
                destination=row["to"],
                call_date=call_date,
                est_time=est_time,
                ist_time=ist_time,
                hour=row["hour"],
                duration=row["duration"],
                duration_seconds=row["duration_seconds"],
                call_status=row["status"],
                call_category=row["category"],
            )
    
            imported += 1
    
        except Exception as e:
            print("Import Error :", e)
            errors += 1

    messages.success(

        request,

        f"Imported : {imported} | Skipped : {skipped} | Errors : {errors}"

    )

    request.session.pop("cdr_all_rows", None)

    return redirect("CDR:import_cdr")


        

from datetime import timedelta

from django.db.models import (
    Avg,
    Case,
    Count,
    Max,
    Sum,
    When,
    IntegerField,
)
from django.shortcuts import render

from .models import CallLog

def seconds_to_time(seconds):
    if not seconds:
        return "00:00:00"

    seconds = int(seconds)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return f"{hours:02}:{minutes:02}:{secs:02}"
    
EXCLUDED_EMPLOYEES = [
    "ABSPL350",
    "ABSPL641",
    "TEST001",
]    

@login_required    
def cdr_dashboard(request):
    # Default to latest available call date
    latest_date = CallLog.objects.aggregate(
        latest=Max("call_date")
    )["latest"]

    if not latest_date:
        return render(
            request,
            "CDR/dashboard.html",
            {
                "from_date": "",
                "to_date": "",
            },
        )

    from_date = request.GET.get("from_date") or latest_date
    to_date = request.GET.get("to_date") or latest_date

    queryset = CallLog.objects.filter(
        call_date__gte=from_date,
        call_date__lte=to_date,
    )
    
    top_queryset = queryset.filter(
        duration_seconds__gte=60
    ).exclude(
        employee_id__in=EXCLUDED_EMPLOYEES
    )    

    
    # Current period length
    from_dt = datetime.strptime(str(from_date), "%Y-%m-%d").date()
    to_dt = datetime.strptime(str(to_date), "%Y-%m-%d").date()
    
    days = (to_dt - from_dt).days + 1
    
    # Find previous available date with data
    previous_end = (
        CallLog.objects.filter(call_date__lt=from_dt)
        .aggregate(last=Max("call_date"))["last"]
    )
    
    previous_queryset = CallLog.objects.none()
    comparison_label = None
    
    if previous_end:
        previous_start = previous_end - timedelta(days=days - 1)
    
        previous_queryset = CallLog.objects.filter(
            call_date__gte=previous_start,
            call_date__lte=previous_end,
        )
    
        if days == 1:
            comparison_label = previous_end.strftime("%d %b %Y")
        else:
            comparison_label = (
                f"{previous_start.strftime('%d %b')} - "
                f"{previous_end.strftime('%d %b %Y')}"
            )    

    # ==============================
    # KPI Cards
    # ==============================
    
    previous_summary = previous_queryset.aggregate(
        total_calls=Count("id"),
        active_users=Count("employee_id", distinct=True),
        total_seconds=Sum("duration_seconds"),
        avg_seconds=Avg("duration_seconds"),
    )    

    summary = queryset.aggregate(
        total_calls=Count("id"),
        active_users=Count("employee_id", distinct=True),
        total_seconds=Sum("duration_seconds"),
        avg_seconds=Avg("duration_seconds"),

        less1_calls=Count(
            Case(
                When(call_category="Less Than 1 Min", then=1),
                output_field=IntegerField(),
            )
        ),

        one3_calls=Count(
            Case(
                When(call_category="1-3 Mins", then=1),
                output_field=IntegerField(),
            )
        ),

        gt3_calls=Count(
            Case(
                When(call_category="3 Mins - 1 Hour", then=1),
                output_field=IntegerField(),
            )
        ),

        hold_calls=Count(
            Case(
                When(call_category="Greater Than 1 Hour", then=1),
                output_field=IntegerField(),
            )
        ),
    )
    
    

    # Convert seconds
    summary["total_duration"] = seconds_to_time(summary["total_seconds"] or 0)
    summary["avg_duration"] = seconds_to_time(int(summary["avg_seconds"] or 0))

    # ==============================
    # Peak / Lowest Hour
    # ==============================

    hourly = (
        queryset.values("hour")
        .annotate(total_calls=Count("id"))
        .order_by("hour")
    )

    peak_hour = hourly.order_by("-total_calls").first()
    low_hour = hourly.order_by("total_calls").first()

    # ==============================
    # Top 3 Talk Time
    # ==============================

    top_duration = (
        top_queryset
        .values(
            "employee_id",
            "employee_name",
        )
        .annotate(
            total_calls=Count("id"),
            total_seconds=Sum("duration_seconds"),
        )
        .order_by("-total_seconds")[:3]
    )

    for row in top_duration:
        row["duration"] = seconds_to_time(row["total_seconds"] or 0)

    # ==============================
    # Top 3 Call Count
    # ==============================

    top_calls = (
        top_queryset
        .values(
            "employee_id",
            "employee_name",
        )
        .annotate(
            total_calls=Count("id"),
        )
        .order_by("-total_calls")[:3]
    )

    # ==============================
    # Lowest 3 Talk Time
    # ==============================

    low_duration = (
        top_queryset
        .values(
            "employee_id",
            "employee_name",
        )
        .annotate(
            total_calls=Count("id"),
            total_seconds=Sum("duration_seconds"),
        )
        .filter(total_calls__gt=0)
        .order_by("total_seconds")[:3]
    )

    for row in low_duration:
        row["duration"] = seconds_to_time(row["total_seconds"] or 0)
        
    comparison = {
    "total_calls": compare(
        summary["total_calls"],
        previous_summary["total_calls"],
    ),
    "active_users": compare(
        summary["active_users"],
        previous_summary["active_users"],
    ),
    "talk_time": compare(
        summary["total_seconds"],
        previous_summary["total_seconds"],
    ),
    "avg_call": compare(
        summary["avg_seconds"],
        previous_summary["avg_seconds"],
    ),

}    


    comparison["talk_time"]["difference_time"] = seconds_to_time(
        abs(int(comparison["talk_time"]["difference"] or 0))
    )
    
    comparison["avg_call"]["difference_time"] = seconds_to_time(
        abs(int(comparison["avg_call"]["difference"] or 0))
    )
    
    
    current_period = {
        "from": from_dt.strftime("%d %b %Y"),
        "to": to_dt.strftime("%d %b %Y"),
    }
    
    previous_period = None
    
    if previous_end:
        previous_period = {
            "from": previous_start.strftime("%d %b %Y"),
            "to": previous_end.strftime("%d %b %Y"),
        }    
        
        
    context = {
        "summary": summary,
        "peak_hour": peak_hour,
        "low_hour": low_hour,
        "top_duration": top_duration,
        "top_calls": top_calls,
        "low_duration": low_duration,
        "hourly": hourly,
        "from_date": from_date,
        "to_date": to_date,
        "comparison": comparison,
        "comparison_label": comparison_label,        
        "current_period": current_period,
        "previous_period": previous_period,
        
    }
    
    

    return render(
        request,
        "CDR/dashboard.html",
        context,
    )


def compare(current, previous):
    current = float(current or 0)
    previous = float(previous or 0)

    diff = current - previous

    if previous > 0:
        percent = abs(round((diff / previous) * 100, 1))
    else:
        percent = 0

    return {
        "current": current,
        "previous": previous,
        "difference": diff,
        "percent": percent,
        "up": diff > 0,
        "down": diff < 0,
        "same": diff == 0,
    }
    
@login_required
def export_hourly_report(request):
    report, visible_hours, from_date, to_date = hourly_report(
        request,
        export=True
    )

    # Create Excel Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Hourly Count"
   
    
    # Header
    headers = [
        "Employee Name",
        "Employee ID",
        "Project",
    ]
    
    # Dynamic Hour Columns
    for hour in visible_hours:
        headers.append(hour["label"])
    
    headers.append("Total Calls")

    
    ws.append(headers)
    
    # Employee Data
    for emp in report:
    
        row = [
            emp["employee_name"],
            emp["employee_id"],
            ", ".join(emp["security_groups"]),
        ]
    
        # Hourly Call Count
        for hour in emp["visible_hourly"]:
            row.append(hour["calls"])
    
        row.append(emp["total_calls"])

    
        ws.append(row)
    
    # Auto Width
    for column in ws.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)
    
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
    
        ws.column_dimensions[column_letter].width = max_length + 3

    # Second Sheet
    ws2 = wb.create_sheet(title="Hourly Duration")
    headers = [
        "Employee Name",
        "Employee ID",
        "Project",
    ]
    
    for hour in visible_hours:
        headers.append(hour["label"])
    
    headers.append("Total Duration")
    
    ws2.append(headers)
    
    for emp in report:
    
        row = [
            emp["employee_name"],
            emp["employee_id"],
            ", ".join(emp["security_groups"]),
        ]
    
        # Hourly Duration
        for hour in emp["visible_hourly"]:
            row.append(hour["duration"])
    
        # Total Duration
        row.append(emp["total_duration"])
    
        ws2.append(row)  

    for sheet in [ws, ws2]:
    
        for column in sheet.columns:
    
            max_length = 0
            column_letter = get_column_letter(column[0].column)
    
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
    
            sheet.column_dimensions[column_letter].width = max_length + 3 

    ws3 = wb.create_sheet(title="Hourly Start Time")
    
    headers = [
        "Employee Name",
        "Employee ID",
        "Project",
    ]
    
    for hour in visible_hours:
        headers.append(hour["label"])
    
    ws3.append(headers)
    
    for emp in report:
    
        row = [
            emp["employee_name"],
            emp["employee_id"],
            ", ".join(emp["security_groups"]),
        ]
    
        for hour in emp["visible_hourly"]:
            row.append(hour["first_call"])
    
        ws3.append(row)            
        
    # Download
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    response["Content-Disposition"] = (
        f'attachment; filename="Hourly_Report_{from_date}_{to_date}.xlsx"'
    )
    
    wb.save(response)
    
    return response 