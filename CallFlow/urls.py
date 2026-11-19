
from django.urls import path
from . import views

app_name = "CallFlow"

urlpatterns = [
    path(
        "create/",
        views.create_form,
        name="callflow_create_form"
    ),

    path(
        "builder/<int:scenario_id>/",
        views.form_builder,
        name="callflow_form_builder"
    ),
    
    path(
        "forms/",
        views.form_list,
        name="callflow_form_list"
    ),    
    
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
