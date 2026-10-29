
from django.urls import path
from . import views

app_name = "SpaceView"

urlpatterns = [
    path("", views.floor_chart, name="floor_chart"),
    path("add-seat/", views.add_workstation, name="add_workstation"),
    path(
        "delete-seat/<int:workstation_id>/",
        views.delete_workstation,
        name="delete_workstation",
    ),
    path(
        "edit-seat/<int:workstation_id>/",
        views.edit_workstation,
        name="edit_workstation",
    ),    
]

