import re
import json

from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone

from ..models import Monitor

def generate_monitor_id(hostname):
    """Generate the next available monitor ID for a hostname."""

    existing_ids = Monitor.objects.filter(
        hostname=hostname
    ).values_list('monitor_id', flat=True)

    numbers = []

    for monitor_id in existing_ids:
        match = re.search(r'-D(\d+)$', monitor_id)
        if match:
            numbers.append(int(match.group(1)))

    next_number = max(numbers, default=0) + 1

    return f"{hostname}-D{next_number}"




def sync_monitor_info(request):

    # Read JSON payload
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({
            "status": "error",
            "message": "Invalid JSON payload"
        }, status=400)

    hostname = str(data.get("hostname") or "").strip().upper()

    if not hostname:
        return JsonResponse({
            "status": "error",
            "message": "Hostname is required"
        }, status=400)

    monitors = data.get("monitors", [])

    if not isinstance(monitors, list):
        return JsonResponse({
            "status": "error",
            "message": "Monitors must be a list"
        }, status=400)

    created_count = 0
    updated_count = 0
    skipped_count = 0

    valid_types = {"INTERNAL", "EXTERNAL", "UNKNOWN"}

    try:
        with transaction.atomic():

            for item in monitors:

                if not isinstance(item, dict):
                    skipped_count += 1
                    continue

                # Accept only physical EDID monitors
                if item.get("is_physical") is not True:
                    skipped_count += 1
                    continue

                edid_instance = str(
                    item.get("edid_instance") or ""
                ).strip()

                if not edid_instance:
                    skipped_count += 1
                    continue

                # Automatic monitor classification
                monitor_type = str(
                    item.get("monitor_type") or "UNKNOWN"
                ).strip().upper()

                if monitor_type not in valid_types:
                    monitor_type = "UNKNOWN"

                defaults = {
                    "manufacturer": item.get("manufacturer"),
                    "manufacturer_code": item.get("manufacturer_code"),
                    "model": item.get("model"),
                    "product_code": item.get("product_code"),
                    "serial_number": item.get("serial_number"),
                    "screen_size": item.get("screen_size"),
                    "connection_type": item.get("connection_type"),
                    "last_sync": timezone.now(),
                }

                monitor = Monitor.objects.filter(
                    hostname=hostname,
                    edid_instance=edid_instance
                ).first()

                if monitor:

                    for field, value in defaults.items():

                        # Do not erase existing values with empty data
                        if value is not None and str(value).strip():
                            setattr(monitor, field, value)

                    # Do not downgrade a known type to UNKNOWN
                    if (
                        monitor_type != "UNKNOWN"
                        or monitor.monitor_type == "UNKNOWN"
                    ):
                        monitor.monitor_type = monitor_type

                    monitor.save()
                    updated_count += 1

                else:

                    Monitor.objects.create(
                        hostname=hostname,
                        monitor_id=generate_monitor_id(hostname),
                        edid_instance=edid_instance,
                        monitor_type=monitor_type,
                        **defaults
                    )

                    created_count += 1

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

    return JsonResponse({
        "status": "success",
        "hostname": hostname,
        "created": created_count,
        "updated": updated_count,
        "skipped": skipped_count,
        "message": "Monitor synchronization completed"
    })



