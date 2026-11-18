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

    path(
        'desktop/<int:pk>/update-asset/',
        views.update_desktop_asset,
        name='update_desktop_asset'
    ),   

    # Laptop Management
    path(
        'laptops/',
        views.laptop_list,
        name='laptop_list'
    ),
    
    path(
        'laptops/<int:pk>/',
        views.laptop_detail,
        name='laptop_detail'
    ),
    
    path(
        'laptops/<int:pk>/update/',
        views.update_laptop_asset,
        name='update_laptop_asset'
    ),    
    
    path(
        'desktops/export/',
        views.export_desktops_excel,
        name='export_desktops_excel'
    ),    
    
]