
from django.urls import path
from . import views

app_name = "Workflow"

urlpatterns = [

    # =========================================
    # ADMIN - MENU BUILDER
    # =========================================

    path(
        "menu-builder/",
        views.menu_builder,
        name="menu_builder"
    ),

    # =========================================
    # ADMIN - FORM BUILDER
    # =========================================

    path(
        "form/<int:form_id>/",
        views.form_edit,
        name="form_edit"
    ),

    # =========================================
    # EMPLOYEE - WORKFLOW PAGE
    # =========================================

    path(
        "employee/",
        views.employee_page,
        name="employee_page"
    ),

    # =========================================
    # EMPLOYEE - FILL FORM / SAVE DRAFT / SUBMIT
    # =========================================

    path(
        "employee/form/<int:form_id>/",
        views.employee_form,
        name="employee_form"
    ),

    # =========================================
    # EMPLOYEE - SUBMITTED FORMS
    # =========================================

    path(
        "employee/form/<int:form_id>/submissions/",
        views.employee_submissions,
        name="employee_submissions"
    ),

    # =========================================
    # EMPLOYEE - VIEW SUBMISSION DETAILS
    # =========================================

    path(
        "employee/submission/<int:submission_id>/",
        views.employee_submission_detail,
        name="employee_submission_detail"
    ),

]
