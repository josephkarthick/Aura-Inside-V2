from django.urls import path
from . import views

app_name = 'Assets'

urlpatterns = [
    path(
        'api/receive-desktop-info/',
        views.receive_desktop_info,
        name='receive_desktop_info'
    ),

    path(
        'api/receive-monitor-info/',
        views.receive_monitor_info,
        name='receive_monitor_info'
    ),
  
    path(
        'desktops/',
        views.desktop_list,
        name='desktop_list'
    ),
    
    path(
        'desktops/<int:pk>/',
        views.desktop_detail,
        name='desktop_detail'
    ),    
    path(
        'monitors/',
        views.monitor_list,
        name='monitor_list'
    ),  
    
]