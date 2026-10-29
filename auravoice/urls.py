from django.urls import path
from . import views

app_name = 'auravoice'

urlpatterns = [
    path('', views.voice_dashboard, name='voice_dashboard'),
    path('create_task/', views.create_task, name='create_task'),
    path('create_schedule/', views.create_schedule, name='create_schedule'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('api/announcements/', views.get_announcements_api, name='get_announcements_api'),
    path('delete_schedule/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),


]
