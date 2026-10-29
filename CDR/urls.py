from django.urls import path
from . import views
from . import reports

app_name = "CDR"

urlpatterns = [
    path("import/", views.import_cdr, name="import_cdr"),
    path("generate/", views.generate_cdr, name="generate_cdr"),
    path("import-save/", views.import_to_database, name="import_to_database"),

    path("employee-summary/", reports.employee_summary, name="employee_summary"),
    path("hourly-report/", reports.hourly_report, name="hourly_report"),
    path(
        "daily-report/<str:employee_id>/<str:call_date>/",
        reports.daily_report,
        name="daily_report",
    ),
    path("export-cdr-report/", reports.export_cdr_report, name="export_cdr_report"),
    path("export-hourly-report/",views.export_hourly_report,name="export_hourly_report"),
    

    path("cdr-dashboard/", views.cdr_dashboard, name="cdr_dashboard"),
]