from django.urls import path
from . import views

app_name = "CallFlow"

urlpatterns = [
    # Single Admin Form Builder
    path(
        "builder/",
        views.form_builder,
        name="callflow_form_builder"
    ),

    # Employee CallFlow
    path(
        "employee/",
        views.employee_callflow_home,
        name="employee_callflow_home"
    ),
    path(
        "employee/new/",
        views.employee_new_form,
        name="employee_new_form"
    ),
    path(
        "employee/form/<int:scenario_id>/",
        views.employee_fill_form,
        name="employee_fill_form"
    ),
]