from django.urls import path
from . import views

app_name = "passwordvault"

urlpatterns = [
    path("list/", views.vault_list, name="vault_list"),
    path("add/", views.vault_add, name="vault_add"),
    path("view/<int:pk>/", views.vault_view, name="vault_view"),
    path("edit/<int:pk>/", views.vault_edit, name="vault_edit"),      
    path("delete/<int:pk>/", views.vault_delete, name="vault_delete"),     
]
