from django.urls import path
from . import views

app_name = 'Assets'

urlpatterns = [
    path(
        'api/receive-desktop-info/',
        views.receive_desktop_info,
        name='receive_desktop_info'
    ),
]