# Employee/views.py
import json
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from ADManager.views import fetch_ldap_user_by_username
from .models import Calendar_Event
from ITDesk.models import VoipRecord

# ---------- helper: parse iso string -> naive datetime (no tzinfo) ----------
def parse_date_to_naive(dt_string):
    """
    Convert ISO datetime string to a naive datetime (no tzinfo).
    - Accepts: '2025-12-11', '2025-12-11T08:00', '2025-12-11T08:00:00Z', or with +05:30 offsets.
    - Returns None for falsy input or parse failure.
    """
    if not dt_string:
        return None
    s = str(dt_string).strip()
    try:
        # handle trailing Z (UTC)
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"

        # datetime.fromisoformat supports offsets like +05:30 on Python3.7+
        dt = datetime.fromisoformat(s)
    except Exception:
        # if fromisoformat fails, try date-only
        try:
            dt = datetime.fromisoformat(s.split("T")[0])
        except Exception:
            return None

    # If dt is timezone-aware, convert to local/default tz then drop tzinfo to make it naive.
    if dt.tzinfo is not None:
        try:
            local_tz = timezone.get_default_timezone()
            dt = dt.astimezone(local_tz).replace(tzinfo=None)
        except Exception:
            # fallback: convert to UTC then drop tzinfo
            try:
                dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
            except Exception:
                dt = dt.replace(tzinfo=None)
    # If dt.tzinfo is already None, keep as-is (naive)
    return dt


@login_required
def calendar_page(request):
    """
    Render calendar page.
    Template path used in this repo: Employee/calendar/calendar_page.html
    """
    return render(request, "Employee/calendar/calendar_page.html")


# ---------- CREATE EVENT ----------
@csrf_exempt
@login_required
def api_create_event(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)
    try:
        data = json.loads(request.body.decode("utf-8") or "{}")
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    title = data.get("title")
    if not title:
        return JsonResponse({"error": "title required"}, status=400)

    try:
        ev = Calendar_Event.objects.create(
            owner=request.user,
            title=title,
            description=data.get("description", ""),
            type=data.get("type", "title"),
            priority=data.get("priority", "normal"),
            start=parse_date_to_naive(data.get("start")),
            end=parse_date_to_naive(data.get("end")),
            reminder=bool(data.get("reminder", False)),
            reminder_date=parse_date_to_naive(data.get("reminder_date")),
        )
        return JsonResponse({"id": ev.id, "message": "created"}, status=201)
    except Exception as e:
        # return helpful error message (don't leak secrets in production)
        return JsonResponse({"error": str(e)}, status=500)


# ---------- UPDATE EVENT ----------
@csrf_exempt
@login_required
def api_update_event(request, event_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8") or "{}")
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    ev = get_object_or_404(Calendar_Event, id=event_id, owner=request.user)
    try:
        if "title" in data:
            ev.title = data.get("title") or ev.title
        if "description" in data:
            ev.description = data.get("description", "")
        if "type" in data:
            ev.type = data.get("type", ev.type)
        if "priority" in data:
            ev.priority = data.get("priority", ev.priority)
        if "start" in data:
            ev.start = parse_date_to_naive(data.get("start"))
        if "end" in data:
            ev.end = parse_date_to_naive(data.get("end"))
        if "reminder" in data:
            ev.reminder = bool(data.get("reminder", False))
        if "reminder_date" in data:
            ev.reminder_date = parse_date_to_naive(data.get("reminder_date"))

        ev.save()
        return JsonResponse({"message": "updated"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ---------- DELETE EVENT ----------
@csrf_exempt
@login_required
def api_delete_event(request, event_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)
    try:
        Calendar_Event.objects.filter(id=event_id, owner=request.user).delete()
        return JsonResponse({"message": "deleted"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ---------- LIST EVENTS (JSON) ----------
@login_required
def events_json(request):
    events = Calendar_Event.objects.filter(owner=request.user).order_by("start")
    out = []
    for ev in events:
        out.append({
            "id": ev.id,
            "title": ev.title,
            "description": ev.description,
            "start": ev.start.isoformat() if ev.start else None,
            "end": ev.end.isoformat() if ev.end else None,
            "type": ev.type,
            "priority": ev.priority,
            "reminder": ev.reminder,
            "reminder_date": ev.reminder_date.isoformat() if ev.reminder_date else None,
        })
    return JsonResponse(out, safe=False)
    


@login_required
def userprofile(request):
    user = request.user  # Logged-in user

    # 🔹 Fetch AD groups (read-only)
    ad_user = fetch_ldap_user_by_username(user.username)
    ad_groups = []
    if ad_user and 'groups' in ad_user:
        ad_groups = ad_user['groups']  # [(group_name, dn)]

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.gender = request.POST.get('gender', '').strip()
        user.birthdate = request.POST.get('birthdate') or None
        user.marital_status = request.POST.get('marital_status', '').strip()
        user.blood_grp = request.POST.get('blood_grp', '').strip()

        # ✅ Editable Contact Info
        user.phone = request.POST.get('phone', '').strip()
        user.address = request.POST.get('address', '').strip()

        try:
            user.save()
            messages.success(request, "Profile updated successfully.")
        except Exception as e:
            messages.error(request, f"Error updating profile: {e}")

        return redirect('employee:userprofile')

    return render(request, 'employee/userprofile.html', {
        'user': user,
        'ad_groups': ad_groups,
    })
  
