from django.urls import path
from . import views

app_name = "Floating_Flag"

urlpatterns = [
    path("", views.flag_list, name="flag_list"),
    path("create/", views.flag_create, name="flag_create"),
    path("edit/<int:pk>/", views.flag_edit, name="flag_edit"),
    path("delete/<int:pk>/", views.flag_delete, name="flag_delete"),
]