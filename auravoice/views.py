from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from .models import VoiceTask, VoiceSchedule
from django.http import JsonResponse
from .models import VoiceSchedule
from django.utils.timezone import localtime, make_aware, get_current_timezone, is_aware
from django.utils.timezone import now


from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils.timezone import (
    now, localtime, make_aware, get_current_timezone, is_aware
)
from .models import VoiceTask, VoiceSchedule


def voice_dashboard(request):
    tz = get_current_timezone()
    current = now()

    # Ensure datetime is aware before calling localtime()
    if not is_aware(current):
        current = make_aware(current, tz)

    tasks = VoiceTask.objects.all()
    schedules = VoiceSchedule.objects.select_related("task")
    for s in schedules:
        s.interval_minutes = 60 // s.times_per_hour if s.times_per_hour else 0

    all_announcements = get_next_announcement()

    return render(request, 'auravoice/dashboard.html', {
        'tasks': tasks,
        'schedules': schedules,
        'next_announcements': all_announcements,
        'now': localtime(current),
    })


def get_next_announcement():
    tz = get_current_timezone()
    current = now()
    if not is_aware(current):
        current = make_aware(current, tz)
    current = localtime(current)

    announcements = []
    print("🔍 Current Time:", current.strftime("%H:%M"))

    for s in VoiceSchedule.objects.select_related('task'):
        today = current.date()

        # Ensure start and end are timezone-aware
        start_dt = datetime.combine(today, s.start_time)
        end_dt = datetime.combine(today, s.end_time)

        if not is_aware(start_dt):
            start_dt = make_aware(start_dt, tz)
        if not is_aware(end_dt):
            end_dt = make_aware(end_dt, tz)

        if end_dt <= start_dt:
            end_dt += timedelta(days=1)

        interval_minutes = 60 // s.times_per_hour if s.times_per_hour else 0
        if interval_minutes == 0:
            continue

        slot = start_dt
        while slot <= end_dt:
            if slot > current:
                announcements.append({
                    'time': slot.strftime('%H:%M'),
                    'title': s.task.title,
                    'description': s.task.description,
                    'voice_name': s.voice_name,
                    'voice_rate': s.voice_rate,
                })
                break
            slot += timedelta(minutes=interval_minutes)

    return announcements



def create_task(request):
    if request.method == 'POST':
        VoiceTask.objects.create(
            title=request.POST['title'],
            description=request.POST['description']
        )
    return redirect('auravoice:voice_dashboard')

def create_schedule(request):
    if request.method == 'POST':
        task = VoiceTask.objects.get(id=request.POST['task_id'])
        interval = int(request.POST['repeat_minutes'])
        repeat_per_hour = 60 // interval
        VoiceSchedule.objects.create(
            task=task,
            start_time=request.POST['start_time'],
            end_time=request.POST['end_time'],
            times_per_hour=repeat_per_hour,
            voice_name=request.POST.get('voice_name', ''),
            voice_rate=float(request.POST.get('voice_rate', 1)),
        )
    return redirect('auravoice:voice_dashboard')

def make_aware_if_needed(dt, tz):
    return dt if is_aware(dt) else make_aware(dt, tz)

def get_announcements_api(request):
    current = localtime()
    tz = get_current_timezone()
    now_str = current.strftime('%H:%M')
    result = []

    for s in VoiceSchedule.objects.select_related('task'):
        today = current.date()
        start_dt = make_aware_if_needed(datetime.combine(today, s.start_time), tz)
        end_dt = make_aware_if_needed(datetime.combine(today, s.end_time), tz)

        if end_dt <= start_dt:
            end_dt += timedelta(days=1)

        interval = 60 // s.times_per_hour if s.times_per_hour else 0
        if interval == 0:
            continue

        slot = start_dt
        while slot <= end_dt:
            if slot.strftime('%H:%M') == now_str:
                result.append({
                    "title": s.task.title,
                    "description": s.task.description,
                    "voice_name": s.voice_name,
                    "voice_rate": s.voice_rate,
                })
                break
            slot += timedelta(minutes=interval)

    return JsonResponse(result, safe=False)


def delete_task(request, task_id):
    t = get_object_or_404(VoiceTask, id=task_id)
    t.delete()
    return redirect('auravoice:voice_dashboard')

def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(VoiceSchedule, id=schedule_id)
    schedule.delete()
    return redirect('auravoice:voice_dashboard')
