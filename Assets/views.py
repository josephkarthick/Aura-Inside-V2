
import json
import secrets
import logging

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .services.cpu import sync_desktop_info

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def receive_desktop_info(request):

    # API token authentication
    expected_token = getattr(
        settings,
        'DESKTOP_AGENT_API_TOKEN',
        None
    )

    received_token = request.headers.get(
        'X-Agent-Token', ''
    )

    if (
        not expected_token
        or not received_token
        or not secrets.compare_digest(
            str(expected_token),
            str(received_token)
        )
    ):
        return JsonResponse({
            'success': False,
            'message': 'Unauthorized agent.'
        }, status=401)

    # Read JSON data
    try:
        data = json.loads(request.body)

        if not isinstance(data, dict):
            raise ValueError("Invalid JSON")

    except (json.JSONDecodeError, ValueError):
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data.'
        }, status=400)

    if not str(data.get('hostname') or '').strip():
        return JsonResponse({
            'success': False,
            'message': 'Hostname is required.'
        }, status=400)

    # Synchronize desktop information
    try:
        result = sync_desktop_info(data)

        return JsonResponse(result, status=200)

    except Exception:
        logger.exception("Desktop hardware synchronization failed")

        return JsonResponse({
            'success': False,
            'message': 'Desktop synchronization failed.'
        }, status=500)
