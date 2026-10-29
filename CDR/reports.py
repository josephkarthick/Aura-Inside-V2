from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Border,Side,Alignment
from django.http import HttpResponse
from django.db.models import Count,Sum,Case,When,IntegerField, Min, Q
from django.shortcuts import render
from .models import CallLog
from datetime import date, timedelta   
from collections import OrderedDict
from Accounts.models import AuraInsideUser
from django.contrib.auth.decorators import login_required
from openpyxl.utils import get_column_letter
from datetime import datetime


def seconds_to_time(seconds):
    if not seconds:
        return "-"

    seconds = int(seconds)

    td = timedelta(seconds=seconds)

    total_seconds = int(td.total_seconds())

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    return f"{hours:02}:{minutes:02}:{secs:02}"
    
    
@login_required
def employee_summary(request):
    # Fetch employee DOJ + Security Groups in one query
    employee_map = {}

    for emp in (
        AuraInsideUser.objects
        .prefetch_related("security_groups")
        .all()
    ):
        employee_map[emp.employee_id] = {
            "date_joined": emp.date_joined,
            "security_groups": list(
                emp.security_groups.values_list("name", flat=True)
            ),
        }

    queryset = CallLog.objects.all()

    yesterday = date.today() - timedelta(days=1)

    from_date = request.GET.get("from_date") or yesterday.strftime("%Y-%m-%d")
    to_date = request.GET.get("to_date") or yesterday.strftime("%Y-%m-%d")

    queryset = queryset.filter(
        call_date__gte=from_date,
        call_date__lte=to_date,
    )

    report = (
        queryset
        .values(
            "employee_id",
            "employee_name",
        )
        .annotate(
            total_calls=Count(
                "id",
                filter=~Q(call_category="Less Than 1 Min")
            ),

            total_seconds=Sum(
                "duration_seconds",
                filter=~Q(call_category="Less Than 1 Min")
            ),

            less1_calls=Count(
                Case(
                    When(call_category="Less Than 1 Min", then=1),
                    output_field=IntegerField(),
                )
            ),

            less1_seconds=Sum(
                Case(
                    When(call_category="Less Than 1 Min", then="duration_seconds"),
                    default=0,
                    output_field=IntegerField(),
                )
            ),

            one3_calls=Count(
                Case(
                    When(call_category="1-3 Mins", then=1),
                    output_field=IntegerField(),
                )
            ),

            one3_seconds=Sum(
                Case(
                    When(call_category="1-3 Mins", then="duration_seconds"),
                    default=0,
                    output_field=IntegerField(),
                )
            ),

            gt3_calls=Count(
                Case(
                    When(call_category="3 Mins - 1 Hour", then=1),
                    output_field=IntegerField(),
                )
            ),

            gt3_seconds=Sum(
                Case(
                    When(call_category="3 Mins - 1 Hour", then="duration_seconds"),
                    default=0,
                    output_field=IntegerField(),
                )
            ),

            hold_calls=Count(
                Case(
                    When(call_category="Greater Than 1 Hour", then=1),
                    output_field=IntegerField(),
                )
            ),

            hold_seconds=Sum(
                Case(
                    When(call_category="Greater Than 1 Hour", then="duration_seconds"),
                    default=0,
                    output_field=IntegerField(),
                )
            ),
        )
        .order_by("-total_seconds", "employee_name")
    )

    today = date.today()

    for row in report:

        employee = employee_map.get(row["employee_id"], {})

        doj = employee.get("date_joined")

        row["date_joined"] = doj
        row["security_groups"] = employee.get("security_groups", [])

        if doj:
            years = today.year - doj.year
            months = today.month - doj.month

            if today.day < doj.day:
                months -= 1

            if months < 0:
                years -= 1
                months += 12

            row["experience"] = (
                f"{years} yr{'s' if years != 1 else ''}, "
                f"{months} mo{'s' if months != 1 else ''}"
            )
        else:
            row["experience"] = "-"

        row["total_duration"] = seconds_to_time(row["total_seconds"])
        row["less1_duration"] = seconds_to_time(row["less1_seconds"])
        row["one3_duration"] = seconds_to_time(row["one3_seconds"])
        row["gt3_duration"] = seconds_to_time(row["gt3_seconds"])
        row["hold_duration"] = seconds_to_time(row["hold_seconds"])

    return render(
        request,
        "CDR/employee_summary.html",
        {
            "report": report,
            "from_date": from_date,
            "to_date": to_date,
        },
    )



@login_required
def hourly_report(request, export=False):

    queryset = CallLog.objects.all()

    # ==========================================================
    # EMPLOYEE MAP
    # ==========================================================

    employee_map = {}

    for emp in AuraInsideUser.objects.prefetch_related("security_groups"):
        employee_map[emp.employee_id] = {
            "date_joined": emp.date_joined,
            "security_groups": list(
                emp.security_groups.values_list("name", flat=True)
            ),
        }

    # ==========================================================
    # DATE FILTER
    # ==========================================================

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    if from_date:
        queryset = queryset.filter(call_date__gte=from_date)

    if to_date:
        queryset = queryset.filter(call_date__lte=to_date)

    # ==========================================================
    # HOURS
    # ==========================================================

    HOURS = [
        "05 PM",
        "06 PM",
        "07 PM",
        "08 PM",
        "09 PM",
        "10 PM",
        "11 PM",
        "12 AM",
        "01 AM",
        "02 AM",
        "03 AM",
        "04 AM",
        "05 AM",
    ]

    # ==========================================================
    # QUERY
    # ==========================================================

    data = (
        queryset.values(
            "employee_id",
            "employee_name",
            "call_date",
            "hour",
        )
        .annotate(
            calls=Count("id"),
            seconds=Sum("duration_seconds"),
            first_call=Min("ist_time"),
        )
        .order_by(
            "employee_name",
            "call_date",
            "hour",
        )
    )

    # ==========================================================
    # EMPLOYEE DATA
    # ==========================================================

    employees = OrderedDict()

    for row in data:

        key = (
            row["employee_id"],
            row["employee_name"],
        )

        # ------------------------------------------------------
        # CREATE EMPLOYEE
        # ------------------------------------------------------

        if key not in employees:

            emp = employee_map.get(
                row["employee_id"],
                {}
            )

            employees[key] = {
                "employee_id": row["employee_id"],
                "employee_name": row["employee_name"],
                "date_joined": emp.get("date_joined"),
                "security_groups": emp.get(
                    "security_groups",
                    []
                ),

                # Overall hourly summary
                # This will contain totals across
                # the entire selected date range.
                "hourly": [
                    {
                        "calls": 0,
                        "seconds": 0,
                        "duration": "0",
                        "first_call": "-"
                    }
                    for _ in range(24)
                ],

                # Daily details
                "daily": OrderedDict(),

                # Overall employee totals
                "total_calls": 0,
                "total_seconds": 0,
            }

        call_date = row["call_date"]

        # ------------------------------------------------------
        # CREATE DAILY RECORD
        # ------------------------------------------------------

        if call_date not in employees[key]["daily"]:

            employees[key]["daily"][call_date] = {
                "date": call_date,

                "hourly": [
                    {
                        "calls": 0,
                        "seconds": 0,
                        "duration": "0",
                        "first_call": "-"
                    }
                    for _ in range(24)
                ],

                "total_calls": 0,
                "total_seconds": 0,
            }

        # ------------------------------------------------------
        # IGNORE HOURS NOT IN REPORT
        # ------------------------------------------------------

        if row["hour"] not in HOURS:
            continue

        idx = HOURS.index(row["hour"])

        calls = row["calls"] or 0
        seconds = row["seconds"] or 0

        # ======================================================
        # EMPLOYEE HOURLY TOTAL
        # ======================================================
        #
        # IMPORTANT:
        # Accumulate across ALL selected dates.
        #
        # Example:
        #
        # 01 Aug 05 PM = 10 minutes
        # 02 Aug 05 PM = 20 minutes
        # 03 Aug 05 PM = 15 minutes
        #
        # Employee 05 PM = 45 minutes
        #
        # ======================================================

        employee_hour = employees[key]["hourly"][idx]

        employee_hour["calls"] += calls

        employee_hour["seconds"] += seconds

        employee_hour["duration"] = seconds_to_time(
            employee_hour["seconds"]
        )

        # Keep the first call time that we encounter
        if (
            row["first_call"]
            and employee_hour["first_call"] == "-"
        ):
            employee_hour["first_call"] = (
                row["first_call"].strftime("%I:%M %p")
            )

        # ======================================================
        # EMPLOYEE TOTAL
        # ======================================================

        employees[key]["total_calls"] += calls

        employees[key]["total_seconds"] += seconds

        # ======================================================
        # DAILY HOURLY DATA
        # ======================================================
        #
        # Daily data is NOT accumulated across dates.
        # Each date has its own hourly values.
        #
        # ======================================================

        daily_hour = (
            employees[key]["daily"][call_date]["hourly"][idx]
        )

        daily_hour["calls"] = calls

        daily_hour["seconds"] = seconds

        daily_hour["duration"] = seconds_to_time(
            seconds
        )

        daily_hour["first_call"] = (
            row["first_call"].strftime("%I:%M %p")
            if row["first_call"]
            else "-"
        )

        # ======================================================
        # DAILY TOTAL
        # ======================================================

        employees[key]["daily"][call_date]["total_calls"] += calls

        employees[key]["daily"][call_date]["total_seconds"] += seconds

    # ==========================================================
    # FINAL REPORT
    # ==========================================================

    report = list(employees.values())

    # Sort employees by total duration
    report.sort(
        key=lambda x: x["total_seconds"],
        reverse=True
    )

    # ==========================================================
    # FIND VISIBLE HOURS
    # ==========================================================

    visible_hours = []

    for i, h in enumerate(HOURS):

        if any(
            employee["hourly"][i]["calls"] > 0
            for employee in report
        ):
            visible_hours.append(
                {
                    "index": i,
                    "label": h,
                }
            )

    # ==========================================================
    # FORMAT FINAL REPORT
    # ==========================================================

    for emp in report:

        # ------------------------------------------------------
        # EMPLOYEE TOTAL DURATION
        # ------------------------------------------------------

        emp["total_duration"] = seconds_to_time(
            emp["total_seconds"]
        )

        # ------------------------------------------------------
        # EMPLOYEE VISIBLE HOURLY DATA
        # ------------------------------------------------------

        emp["visible_hourly"] = [
            emp["hourly"][h["index"]]
            for h in visible_hours
        ]

        # ------------------------------------------------------
        # DAILY DATA
        # ------------------------------------------------------

        emp["daily"] = list(
            emp["daily"].values()
        )

        for day in emp["daily"]:

            # Daily total duration
            day["total_duration"] = seconds_to_time(
                day["total_seconds"]
            )

            # Daily visible hours
            day["visible_hourly"] = [
                day["hourly"][h["index"]]
                for h in visible_hours
            ]

    # ==========================================================
    # EXPORT
    # ==========================================================

    if export:
        return (
            report,
            visible_hours,
            from_date,
            to_date,
        )

    # ==========================================================
    # RENDER
    # ==========================================================

    return render(
        request,
        "CDR/hourly_report.html",
        {
            "report": report,
            "visible_hours": visible_hours,
            "from_date": from_date,
            "to_date": to_date,
        },
    )

@login_required
def daily_report(request, employee_id, call_date):

    calls = (
        CallLog.objects
        .filter(
            employee_id=employee_id,
            call_date=call_date,
        )
        .order_by("ist_time")
    )

    employee_name = calls.first().employee_name if calls.exists() else employee_id

    return render(
        request,
        "CDR/daily_report.html",
        {
            "calls": calls,
            "employee_id": employee_id,
            "employee_name": employee_name,
            "call_date": call_date,
        },
    )

    
@login_required    
def export_cdr_report(request):

    queryset = CallLog.objects.all()

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    if from_date:
        queryset = queryset.filter(call_date__gte=from_date)

    if to_date:
        queryset = queryset.filter(call_date__lte=to_date)

    wb = Workbook()
    ws = wb.active
    ws.title = "Employee Summary Data"

    # Header
    headers = [
        "Employee ID",
        "Employee Name",
        "Source",
        "Destination",
        "Call Date",
        "IST Time",
        "EST Time",
        "Duration",
        "Duration Seconds",
        "Status",
        "Category",
        "Vendor",
        "hrs",
    ]

    ws.append(headers)

    # 1. Write all rows
    for call in queryset.order_by("employee_name", "call_date", "ist_time"):
        ws.append([
            call.employee_id,
            call.employee_name,
            call.source,
            call.destination,
            call.call_date,
            call.ist_time,
            call.est_time,
            timedelta(seconds=int(call.duration_seconds)),
            call.duration_seconds,
            call.call_status,
            call.call_category,
            call.vendor,
            call.hour,
        ])
    
    # 2. Format the Duration column
    for row in range(2, ws.max_row + 1):
        ws.cell(row=row, column=8).number_format = "[h]:mm:ss"
    
    # 3. Create the response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    response["Content-Disposition"] = 'attachment; filename="Employee_Summary_Source.xlsx"'
    
    # 4. Save workbook
    wb.save(response)
    
    return response




    