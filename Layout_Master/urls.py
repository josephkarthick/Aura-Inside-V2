
from django.urls import path
from . import views

app_name = "Layout_Master"

urlpatterns = [
    path(
        "",
        views.layout_master,
        name="layout_master",
    ),
    path(
        "get-permission/",
        views.get_permission,
        name="get_permission",
    ),
    path(
        "get-designations/",
        views.get_designations,
        name="get_designations",
    ),
    path(
        "save-permission/",
        views.save_permission,
        name="save_permission",
    ),
    
    path('maintenance/', views.maintenance, name='maintenance'),    
]

