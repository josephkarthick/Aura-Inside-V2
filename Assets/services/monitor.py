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

    # Validate agent token
    agent_token = request.headers.get('X-Agent-Token')

    if agent_token != settings.DESKTOP_AGENT_API_TOKEN:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid agent token'
        }, status=401)

    # Read JSON payload
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON payload'
        }, status=400)

    hostname = str(data.get('hostname') or '').strip().upper()

    if not hostname:
        return JsonResponse({
            'status': 'error',
            'message': 'Hostname is required'
        }, status=400)

    monitors = data.get('monitors', [])

    if not isinstance(monitors, list):
        return JsonResponse({
            'status': 'error',
            'message': 'Monitors must be a list'
        }, status=400)

    created_count = 0
    updated_count = 0
    skipped_count = 0

    try:
        with transaction.atomic():

            for item in monitors:

                if not isinstance(item, dict):
                    skipped_count += 1
                    continue

                # Only accept actual physical EDID monitors.
                # RDP and virtual display adapters must never be saved.
                if item.get('is_physical') is not True:
                    skipped_count += 1
                    continue

                edid_instance = str(
                    item.get('edid_instance') or ''
                ).strip()

                # EDID instance is our primary matching identifier.
                if not edid_instance:
                    skipped_count += 1
                    continue

                defaults = {
                    'manufacturer': item.get('manufacturer'),
                    'manufacturer_code': item.get('manufacturer_code'),
                    'model': item.get('model'),
                    'product_code': item.get('product_code'),
                    'serial_number': item.get('serial_number'),
                    'screen_size': item.get('screen_size'),
                    'connection_type': item.get('connection_type'),
                    'resolution': item.get('resolution'),
                    'refresh_rate': item.get('refresh_rate'),
                    'last_sync': timezone.now(),
                }

                monitor = Monitor.objects.filter(
                    hostname=hostname,
                    edid_instance=edid_instance
                ).first()

                if monitor:
                    for field, value in defaults.items():
                        # Do not erase existing values with empty data.
                        if value is not None and str(value).strip():
                            setattr(monitor, field, value)

                    monitor.save()
                    updated_count += 1

                else:
                    monitor = Monitor(
                        hostname=hostname,
                        monitor_id=generate_monitor_id(hostname),
                        edid_instance=edid_instance,
                        **defaults
                    )
                    monitor.save()
                    created_count += 1

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

    return JsonResponse({
        'status': 'success',
        'hostname': hostname,
        'created': created_count,
        'updated': updated_count,
        'skipped': skipped_count,
        'message': 'Monitor synchronization completed'
    })


