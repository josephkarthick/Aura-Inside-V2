
import json

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import Workstation
from ITDesk.models import ITAsset


def serialize_workstation(workstation):
    return {
        "id": workstation.id,
        "workstation_code": workstation.workstation_code,
        "floor": workstation.floor,
        "x_position": workstation.x_position,
        "y_position": workstation.y_position,
        "assigned_asset_id": workstation.assigned_asset_id,
        "is_active": workstation.is_active,
    }


@login_required
def floor_chart(request):
    workstations = [
        serialize_workstation(ws)
        for ws in Workstation.objects.filter(is_active=True)
    ]

    # Read existing assets from ITDesk; do not modify ITDesk.
    assets = ITAsset.objects.all().order_by("asset_tag")

    return render(
        request,
        "SpaceView/floor_chart.html",
        {
            "workstations_json": json.dumps(workstations),
            "assets": assets,
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

        if floor not in ("eighth", "second"):
            return JsonResponse(
                {"success": False, "error": "Invalid floor."},
                status=400,
            )

        if not (0 <= x_position <= 100 and 0 <= y_position <= 100):
            return JsonResponse(
                {"success": False, "error": "Invalid map position."},
                status=400,
            )

        # Generate workstation numbers independently for each map.
        existing_codes = Workstation.objects.filter(
            floor=floor,
            workstation_code__startswith="WS"
        ).values_list("workstation_code", flat=True)
        
        numbers = [
            int(existing_code[2:])
            for existing_code in existing_codes
            if existing_code[2:].isdigit()
        ]
        
        code = f"WS{max(numbers, default=0) + 1:03d}"

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
        return JsonResponse(
            {"success": False, "error": "Invalid request data."},
            status=400,
        )
    except IntegrityError:
        return JsonResponse(
            {"success": False, "error": "Unable to create the workstation."},
            status=400,
        )


@login_required
@require_POST
def delete_workstation(request, workstation_id):
    try:
        workstation = Workstation.objects.get(id=workstation_id)
    except Workstation.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Workstation not found."},
            status=404,
        )

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

        # Assignment-only request from the Assign System button.
        if "assigned_asset_id" in data and not any(
            key in data
            for key in (
                "workstation_code",
                "floor",
                "x_position",
                "y_position",
            )
        ):
            raw_asset_id = data.get("assigned_asset_id")

            if raw_asset_id in (None, ""):
                workstation.assigned_asset_id = None
            else:
                try:
                    asset_id = int(raw_asset_id)
                except (ValueError, TypeError):
                    return JsonResponse({
                        "success": False,
                        "error": "Invalid asset selection.",
                    }, status=400)

                if not ITAsset.objects.filter(pk=asset_id).exists():
                    return JsonResponse({
                        "success": False,
                        "error": "Selected asset was not found.",
                    }, status=404)

                # Prevent assigning the same asset to multiple workstations.
                already_assigned = Workstation.objects.filter(
                    assigned_asset_id=asset_id
                ).exclude(pk=workstation.pk).exists()

                if already_assigned:
                    return JsonResponse({
                        "success": False,
                        "error": "This system is already assigned to another workstation.",
                    }, status=400)

                workstation.assigned_asset_id = asset_id

            workstation.save(update_fields=[
                "assigned_asset_id",
                "updated_at",
            ])

            return JsonResponse({
                "success": True,
                "workstation": serialize_workstation(workstation),
            })

        # Normal workstation edit.
        workstation_code = data.get(
            "workstation_code",
            workstation.workstation_code,
        ).strip().upper()

        floor = data.get("floor", workstation.floor)
        x_position = float(data.get("x_position", workstation.x_position))
        y_position = float(data.get("y_position", workstation.y_position))

        if not workstation_code:
            return JsonResponse({
                "success": False,
                "error": "Seat number is required.",
            }, status=400)

        if floor not in ("eighth", "second"):
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
            workstation_code__iexact=workstation_code
        ).exclude(pk=workstation.pk).exists():
            return JsonResponse({
                "success": False,
                "error": "This seat number already exists.",
            }, status=400)

        workstation.workstation_code = workstation_code
        workstation.floor = floor
        workstation.x_position = x_position
        workstation.y_position = y_position

        # If the edit form sends an asset ID, save it too.
        if "assigned_asset_id" in data:
            raw_asset_id = data.get("assigned_asset_id")

            if raw_asset_id in (None, ""):
                workstation.assigned_asset_id = None
            else:
                asset_id = int(raw_asset_id)

                if not ITAsset.objects.filter(pk=asset_id).exists():
                    return JsonResponse({
                        "success": False,
                        "error": "Selected asset was not found.",
                    }, status=404)

                already_assigned = Workstation.objects.filter(
                    assigned_asset_id=asset_id
                ).exclude(pk=workstation.pk).exists()

                if already_assigned:
                    return JsonResponse({
                        "success": False,
                        "error": "This system is already assigned to another workstation.",
                    }, status=400)

                workstation.assigned_asset_id = asset_id

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
            "error": "Unable to save the workstation. Check for duplicate values.",
        }, status=400)
