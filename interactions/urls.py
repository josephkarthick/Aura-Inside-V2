from django.urls import path
from . import views

app_name ="interactions"

urlpatterns = [
    path("react/", views.add_reaction, name="add_reaction"),
    path("comment/", views.add_comment, name="add_comment"),

    # 👇 NEW
    path("details/", views.interaction_details, name="interaction_details"),
]

