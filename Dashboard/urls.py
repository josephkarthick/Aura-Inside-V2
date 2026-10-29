from django.urls import path
from . import views

app_name = 'Dashboard'

urlpatterns = [
    path('it-dashboard/', views.IT_Dashboard, name="IT_Dashboard")
]
