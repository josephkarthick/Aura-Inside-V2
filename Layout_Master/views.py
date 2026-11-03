import logging

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from Accounts.models import Department, Designation, AuraInsideUser
from .models import (
    Menu, SubMenu, ChildMenu,
    MenuDesignationAccess, SubMenuDesignationAccess, ChildMenuDesignationAccess,
)

logger = logging.getLogger(__name__)


def _get_designation_title(designation):
    return getattr(designation, 'title', None) or getattr(designation, 'name', None) or str(designation)


def _get_target(level, object_id):
    if level == 'menu':
        return Menu.objects.filter(pk=object_id).first()
    if level == 'submenu':
        return SubMenu.objects.filter(pk=object_id).first()
    if level == 'childmenu':
        return ChildMenu.objects.filter(pk=object_id).first()
    return None


def _get_level_from_request(request):
    for key in ('childmenu_id', 'submenu_id', 'menu_id'):
        object_id = request.GET.get(key) or request.POST.get(key)
        if object_id:
            return key.removesuffix('_id'), object_id
    return None, None


def _pair_model(level):
    return {
        'menu': (MenuDesignationAccess, 'menu'),
        'submenu': (SubMenuDesignationAccess, 'submenu'),
        'childmenu': (ChildMenuDesignationAccess, 'childmenu'),
    }.get(level)


def _pair_rows(level, obj):
    model_info = _pair_model(level)
    if not model_info:
        return []
    model, target_field = model_info
    return list(model.objects.filter(**{target_field: obj}).values(
        'department_id', 'designation_id'
    ))


def _permission_json(level, obj):
    return {
        'success': True,
        'visibility': obj.visibility or 'public',
        'departments': list(obj.departments.values_list('pk', flat=True)),
        'designations': list(obj.designations.values_list('pk', flat=True)),
        'users': list(obj.users.values_list('pk', flat=True)),
        'designation_pairs': _pair_rows(level, obj),
    }


@login_required
def layout_master(request):
    menus = Menu.objects.prefetch_related('submenus__child_menus').order_by('order', 'name')
    departments = Department.objects.all().order_by('name')
    users = AuraInsideUser.objects.all().order_by('username')
    return render(request, 'Layout_Master/layout_master.html', {
        'menus': menus, 'departments': departments, 'users': users,
    })


@login_required
@require_GET
def get_permission(request):
    level, object_id = _get_level_from_request(request)
    if not level or not object_id:
        return JsonResponse({'success': False, 'message': 'Select a menu, submenu, or child menu.'}, status=400)
    obj = _get_target(level, object_id)
    if obj is None:
        return JsonResponse({'success': False, 'message': 'Selected menu item was not found.'}, status=404)
    return JsonResponse(_permission_json(level, obj))


@login_required
@require_GET
def get_designations(request):
    department_id = request.GET.get('department_id')
    if not department_id:
        return JsonResponse({'designations': []})
    include_ids = [value.strip() for value in request.GET.get('include_ids', '').split(',') if value.strip()]
    try:
        employees = (AuraInsideUser.objects.filter(
            department_id=department_id, designation__isnull=False
        ).select_related('designation', 'department').order_by('designation_id'))
        designation_map = {}
        for employee in employees:
            designation = employee.designation
            key = str(designation.pk)
            designation_map[key] = {
                'id': designation.pk,
                'title': _get_designation_title(designation),
                'department_id': employee.department_id,
                'department_name': getattr(employee.department, 'name', None) or str(employee.department),
            }
        if include_ids:
            department = Department.objects.filter(pk=department_id).first()
            department_name = getattr(department, 'name', None) or str(department) if department else str(department_id)
            for designation in Designation.objects.filter(pk__in=include_ids):
                key = str(designation.pk)
                if key not in designation_map:
                    designation_map[key] = {
                        'id': designation.pk,
                        'title': _get_designation_title(designation),
                        'department_id': department_id,
                        'department_name': department_name,
                    }
        return JsonResponse({'designations': list(designation_map.values())})
    except (ValueError, TypeError):
        return JsonResponse({'designations': [], 'message': 'Invalid department ID.'}, status=400)





def _get_permission_targets(level, target):
    """
    Return the selected item, its ancestors and applicable descendants.
    """

    targets = []
    seen = set()

    def add(item_level, obj):
        key = (item_level, obj.pk)

        if key not in seen:
            seen.add(key)
            targets.append((item_level, obj))

    if level == "menu":
        menu = target

    elif level == "submenu":
        menu = target.menu

    elif level == "childmenu":
        menu = target.submenu.menu

    else:
        return []

    # Always include the parent Menu
    add("menu", menu)

    if level == "menu":
        submenus = SubMenu.objects.filter(menu=menu)

    elif level == "submenu":
        submenus = SubMenu.objects.filter(pk=target.pk)

    else:
        submenus = SubMenu.objects.filter(pk=target.submenu_id)

    for submenu in submenus:
        add("submenu", submenu)

        if level == "childmenu":
            # Only the selected ChildMenu
            if submenu.pk == target.submenu_id:
                add("childmenu", target)

        else:
            # All descendants of the selected SubMenu
            for child in ChildMenu.objects.filter(submenu=submenu):
                add("childmenu", child)

    return targets



@login_required
@require_POST
def save_permission(request):

    level, object_id = _get_level_from_request(request)

    if not level or not object_id:
        return JsonResponse({
            "success": False,
            "message": "Please select a menu."
        }, status=400)

    target = _get_target(level, object_id)

    if target is None:
        return JsonResponse({
            "success": False,
            "message": "Selected menu item was not found."
        }, status=404)

    visibility = request.POST.get("visibility", "public")

    if visibility not in {"public", "authenticated", "department"}:
        return JsonResponse({
            "success": False,
            "message": "Invalid access type."
        }, status=400)

    department_ids = list(dict.fromkeys(request.POST.getlist("departments")))
    designation_ids = list(dict.fromkeys(request.POST.getlist("designations")))
    user_ids = list(dict.fromkeys(request.POST.getlist("users")))
    pair_values = list(dict.fromkeys(request.POST.getlist("designation_pairs")))

    departments = list(Department.objects.filter(pk__in=department_ids))
    designations = list(Designation.objects.filter(pk__in=designation_ids))
    users = list(AuraInsideUser.objects.filter(pk__in=user_ids))

    if len(departments) != len(department_ids):
        return JsonResponse({
            "success": False,
            "message": "One or more departments are invalid."
        }, status=400)

    if len(designations) != len(designation_ids):
        return JsonResponse({
            "success": False,
            "message": "One or more designations are invalid."
        }, status=400)

    if len(users) != len(user_ids):
        return JsonResponse({
            "success": False,
            "message": "One or more users are invalid."
        }, status=400)

    valid_department_ids = {str(item.pk) for item in departments}
    valid_designation_ids = {str(item.pk) for item in designations}

    parsed_pairs = []

    for value in pair_values:
        try:
            department_id, designation_id = value.split(":", 1)
        except ValueError:
            return JsonResponse({
                "success": False,
                "message": f"Invalid designation pair: {value}"
            }, status=400)

        if (
            department_id not in valid_department_ids
            or designation_id not in valid_designation_ids
        ):
            return JsonResponse({
                "success": False,
                "message": (
                    "A designation pair refers to an unselected "
                    "or invalid department/designation."
                )
            }, status=400)

        parsed_pairs.append((department_id, designation_id))

    if visibility == "department" and not department_ids and not user_ids:
        return JsonResponse({
            "success": False,
            "message": "Select at least one department or specific user."
        }, status=400)

    # Get selected item and all descendants
    targets = _get_permission_targets(level, target)

    try:
        with transaction.atomic():

            for target_level, obj in targets:

                pair_info = _pair_model(target_level)

                if pair_info is None:
                    raise ValueError(
                        f"Unsupported permission level: {target_level}"
                    )

                pair_model, target_field = pair_info

                # Apply access type
                obj.visibility = visibility
                obj.save(update_fields=["visibility"])

                if visibility != "department":

                    obj.departments.clear()
                    obj.designations.clear()
                    obj.users.clear()

                    pair_model.objects.filter(
                        **{target_field: obj}
                    ).delete()

                else:

                    # Apply same selected permissions
                    obj.departments.set(departments)
                    obj.designations.set(designations)
                    obj.users.set(users)

                    # Replace designation pairs for this item
                    pair_model.objects.filter(
                        **{target_field: obj}
                    ).delete()

                    pair_model.objects.bulk_create([
                        pair_model(
                            **{
                                target_field: obj,
                                "department_id": department_id,
                                "designation_id": designation_id,
                            }
                        )
                        for department_id, designation_id in parsed_pairs
                    ], ignore_conflicts=True)

    except Exception:
        logger.exception("Failed to update hierarchical permissions.")

        return JsonResponse({
            "success": False,
            "message": "Unable to save permissions. Check Django server log."
        }, status=500)

    return JsonResponse({
        "success": True,
        "message": (
            f"Permission successfully applied to {len(targets)} "
            f"menu items, including all applicable descendants."
        ),
        "updated_count": len(targets),
    })

def maintenance(request):
    return render(request, 'Layout_Master/maintenance.html')