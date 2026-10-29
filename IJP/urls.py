from django.urls import path
from . import views

app_name = "IJP"

urlpatterns = [

    # ==========================
    # Admin
    # ==========================
    path(
        "create_ijp/",
        views.create_ijp,
        name="create_ijp"
    ),
    
    path(
        "admin/ijps/<int:ijp_id>/edit/",
        views.edit_ijp,
        name="edit_ijp",
    ),  

    path(
        "admin/ijps/",
        views.hr_ijp_list,
        name="hr_ijp_list",
    ),  

    # ==========================
    # Employee
    # ==========================
    path(
        "jobs/",
        views.user_ijp_list,
        name="user_ijp_list"
    ),

    path(
        "apply/<int:ijp_id>/",
        views.apply_ijp,
        name="apply_ijp"
    ),

    path(
        "admin/ijps/",
        views.hr_ijp_list,
        name="hr_ijp_list",
    ),
    
    path(
        "results/<int:ijp_id>/",
        views.ijp_results,
        name="ijp_results"
    ),
    
    path(
        "my-applications/",
        views.my_ijp_applications,
        name="my_ijp_applications",
    ),
    path(
        "training-pdf/<int:application_id>/",
        views.download_ijp_training_pdf,
        name="download_ijp_training_pdf",
    ),
]
