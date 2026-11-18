
import json

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import Workstation
from Assets.models import Asset


def serialize_workstation(workstation, assigned_assets=None):
    assigned_assets = assigned_assets or []

    return {
        "id": workstation.id,
        "workstation_code": workstation.workstation_code,
        "floor": workstation.floor,
        "x_position": workstation.x_position,
        "y_position": workstation.y_position,
        "is_active": workstation.is_active,
        "assets": assigned_assets,
    }


@login_required
def floor_chart(request):

    workstations = Workstation.objects.filter(
        is_active=True
    ).order_by("floor", "workstation_code")

    # Fetch assignments directly from the Assets table.
    assets = Asset.objects.filter(
        location__in=["Agastya", "Vishwam"],
    ).exclude(
        workstation__isnull=True
    ).exclude(
        workstation=""
    ).values(
        "asset_name",
        "asset_tag",
        "location",
        "workstation",
        "status",
    )

    # Map each asset to its floor and workstation.
    asset_map = {}

    for asset in assets:
        key = (asset["location"], asset["workstation"].strip().upper())
        asset_map.setdefault(key, []).append(asset)

    workstation_data = []

    for ws in workstations:
        key = (ws.floor, ws.workstation_code.strip().upper())

        workstation_data.append(
            serialize_workstation(
                ws,
                asset_map.get(key, [])
            )
        )

    return render(
        request,
        "SpaceView/floor_chart.html",
        {
            "workstations_json": json.dumps(workstation_data),
        },
    )


@login_required
@require_POST
def add_workstation(request):
    try:
        data = json.loads(request.body)

        floor = data.get("floor")
        x_position = float(data.get("x_position"))
        y_position = float(data.get("y_position"))

        if floor not in ("Agastya", "Vishwam"):
            return JsonResponse({
                "success": False,
                "error": "Invalid floor.",
            }, status=400)

        if not (0 <= x_position <= 100 and 0 <= y_position <= 100):
            return JsonResponse({
                "success": False,
                "error": "Invalid map position.",
            }, status=400)

        prefix = {
            "Vishwam": "VWS",
            "Agastya": "AWS",
        }[floor]

        existing_codes = Workstation.objects.filter(
            floor=floor,
            workstation_code__startswith=f"{prefix}-",
        ).values_list("workstation_code", flat=True)

        numbers = [
            int(code.split("-")[-1])
            for code in existing_codes
            if code.split("-")[-1].isdigit()
        ]

        code = f"{prefix}-{max(numbers, default=0) + 1:03d}"

        workstation = Workstation.objects.create(
            workstation_code=code,
            floor=floor,
            x_position=x_position,
            y_position=y_position,
        )

        return JsonResponse({
            "success": True,
            "workstation": serialize_workstation(workstation),
        })

    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({
            "success": False,
            "error": "Invalid request data.",
        }, status=400)

    except IntegrityError:
        return JsonResponse({
            "success": False,
            "error": "Unable to create the workstation.",
        }, status=400)


@login_required
@require_POST
def delete_workstation(request, workstation_id):
    try:
        workstation = Workstation.objects.get(id=workstation_id)
    except Workstation.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": "Workstation not found.",
        }, status=404)

    code = workstation.workstation_code
    workstation.delete()

    return JsonResponse({
        "success": True,
        "message": f"{code} deleted successfully.",
    })


@login_required
@require_POST
def edit_workstation(request, workstation_id):
    try:
        data = json.loads(request.body)
        workstation = Workstation.objects.get(id=workstation_id)

        workstation_code = data.get(
            "workstation_code",
            workstation.workstation_code,
        ).strip().upper()

        floor = data.get("floor", workstation.floor)
        x_position = float(
            data.get("x_position", workstation.x_position)
        )
        y_position = float(
            data.get("y_position", workstation.y_position)
        )

        if not workstation_code:
            return JsonResponse({
                "success": False,
                "error": "Seat number is required.",
            }, status=400)

        if floor not in ("Agastya", "Vishwam"):
            return JsonResponse({
                "success": False,
                "error": "Invalid floor.",
            }, status=400)

        if not (0 <= x_position <= 100 and 0 <= y_position <= 100):
            return JsonResponse({
                "success": False,
                "error": "Invalid seat position.",
            }, status=400)

        if Workstation.objects.filter(
            floor=floor,
            workstation_code__iexact=workstation_code,
        ).exclude(pk=workstation.pk).exists():
            return JsonResponse({
                "success": False,
                "error": "This seat number already exists on this floor.",
            }, status=400)

        workstation.workstation_code = workstation_code
        workstation.floor = floor
        workstation.x_position = x_position
        workstation.y_position = y_position
        workstation.save()

        return JsonResponse({
            "success": True,
            "workstation": serialize_workstation(workstation),
        })

    except Workstation.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": "Workstation not found.",
        }, status=404)

    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({
            "success": False,
            "error": "Invalid request data.",
        }, status=400)

    except IntegrityError:
        return JsonResponse({
            "success": False,
            "error": "Unable to save the workstation.",
        }, status=400)
