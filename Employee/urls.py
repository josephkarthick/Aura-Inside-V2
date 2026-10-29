from django.urls import path
from . import views
from .services import voip_call

app_name = 'employee'

urlpatterns = [
    path(
        'calendar/',
        views.calendar_page,
        name='calendar_page'
    ),

    # Calendar CRUD
    path(
        'calendar/events/create/',
        views.api_create_event,
        name='api_create_event'
    ),

    path(
        'calendar/events/<int:event_id>/update/',
        views.api_update_event,
        name='api_update_event'
    ),

    path(
        'calendar/events/<int:event_id>/delete/',
        views.api_delete_event,
        name='api_delete_event'
    ),

    path(
        'calendar/events/json/',
        views.events_json,
        name='events_json'
    ),

    # Employee Profile
    path(
        'userprofile/',
        views.userprofile,
        name='userprofile'
    ),

    # Click To Call
    path(
        "call/",
        voip_call.initiate_employee_call,
        name="initiate_employee_call"
    ),
    
]