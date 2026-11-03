
import json
import secrets
import logging

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .services.cpu import sync_desktop_info
from .services.monitor import sync_monitor_info
from .models import DesktopAsset, Monitor, ComputerUserHistory


logger = logging.getLogger(__name__)


# ============================================================
# COMMON AGENT TOKEN VALIDATION
# ============================================================

def validate_agent_token(request):

    expected_token = getattr(
        settings,
        "DESKTOP_AGENT_API_TOKEN",
        None
    )

    received_token = request.headers.get(
        "X-Agent-Token",
        ""
    )

    return bool(
        expected_token
        and received_token
        and secrets.compare_digest(
            str(expected_token),
            str(received_token)
        )
    )


# ============================================================
# RECEIVE COMPUTER HARDWARE INFORMATION
# ============================================================

@csrf_exempt
@require_POST
def receive_desktop_info(request):

    if not validate_agent_token(request):
        return JsonResponse({
            "success": False,
            "message": "Unauthorized agent."
        }, status=401)

    try:
        data = json.loads(request.body)

        if not isinstance(data, dict):
            raise ValueError("Invalid JSON")

    except (json.JSONDecodeError, ValueError):
        return JsonResponse({
            "success": False,
            "message": "Invalid JSON data."
        }, status=400)

    if not str(data.get("hostname") or "").strip():
        return JsonResponse({
            "success": False,
            "message": "Hostname is required."
        }, status=400)

    try:
        result = sync_desktop_info(data)

        return JsonResponse(result, status=200)

    except Exception:
        logger.exception(
            "Computer hardware synchronization failed"
        )

        return JsonResponse({
            "success": False,
            "message": "Computer synchronization failed."
        }, status=500)


# ============================================================
# RECEIVE MONITOR INFORMATION
# ============================================================

@csrf_exempt
@require_POST
def receive_monitor_info(request):

    if not validate_agent_token(request):
        return JsonResponse({
            "status": "error",
            "message": "Invalid agent token."
        }, status=401)

    return sync_monitor_info(request)


# ============================================================
# COMPUTER / DESKTOP LIST
# ============================================================

def desktop_list(request):

    search = request.GET.get("search", "").strip()

    desktops = DesktopAsset.objects.select_related(
        "asset"
    ).all()

    if search:
        desktops = desktops.filter(
            Q(hostname__icontains=search) |
            Q(asset_type__icontains=search) |
            Q(processor__icontains=search) |
            Q(os_installed__icontains=search) |
            Q(logged_in_user__icontains=search) |
            Q(ip_address__icontains=search) |
            Q(asset__asset_tag__icontains=search)
        )

    return render(request, "Assets/desktop_list.html", {
        "desktops": desktops,
        "search_term": search,
        "total_desktops": desktops.count(),
    })


# ============================================================
# COMPUTER DETAIL
# ============================================================


def desktop_detail(request, pk):
    desktop = get_object_or_404(
        DesktopAsset.objects.select_related('asset'),
        pk=pk
    )

    monitors = Monitor.objects.filter(
        hostname__iexact=desktop.hostname
    ).order_by('monitor_id')

    # Official assignment history
    assignments = desktop.asset.assignment_history.select_related(
        'employee',
        'assigned_by'
    ).all()

    # Automatically detected Windows user history
    detected_users = ComputerUserHistory.objects.filter(
        computer_id=desktop.pk
    ).select_related(
        'employee'
    ).order_by('-first_seen')

    context = {
        'desktop': desktop,
        'asset': desktop.asset,
        'monitors': monitors,
        'assignments': assignments,
        'detected_users': detected_users,
    }

    return render(
        request,
        'Assets/desktop_detail.html',
        context
    )



# ============================================================
# MONITOR LIST
# ============================================================

def monitor_list(request):

    search = request.GET.get("search", "").strip()

    monitors = Monitor.objects.all()

    if search:
        monitors = monitors.filter(
            Q(hostname__icontains=search) |
            Q(monitor_id__icontains=search) |
            Q(manufacturer__icontains=search) |
            Q(model__icontains=search) |
            Q(serial_number__icontains=search)
        )

    return render(request, "Assets/monitor_list.html", {
        "monitors": monitors,
        "search_term": search,
        "total_monitors": monitors.count(),
    })
