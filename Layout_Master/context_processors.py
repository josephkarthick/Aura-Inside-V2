from django.db.models import Q, Prefetch
from Layout_Master.models import Menu, SubMenu, ChildMenu
from Intranet.models import FloatingFlag


def aura_flag_context(request):
    flag, _ = FloatingFlag.objects.get_or_create(id=1)
    return {"flag": flag}


def _access_filter(model_level, user):
    """Build visibility filters with per-department designation pairs and explicit-user grants."""
    if not user.is_authenticated:
        return Q(visibility="public")

    result = Q(visibility="public") | Q(visibility="authenticated")
    result |= Q(visibility="department", users=user)

    department_id = getattr(user, "department_id", None)
    designation_id = getattr(user, "designation_id", None)
    if not department_id:
        return result

    # Specific-user-only permissions are not also granted to everybody in a department.
    no_user_restriction = Q(users__isnull=True)
    # Backward-compatible behavior for older permissions that have no pair rows.
    # If legacy designation IDs exist, require the user's designation to match.
    legacy_department_only = Q(
        designation_rules__isnull=True,
        departments__id=department_id,
        designations__isnull=True,
    )
    legacy_designation_match = Q(
        designation_rules__isnull=True,
        departments__id=department_id,
        designations__id=designation_id,
    ) if designation_id else Q(pk__in=[])
    paired_match = Q(
        designation_rules__department_id=department_id,
        designation_rules__designation_id=designation_id,
    ) if designation_id else Q(pk__in=[])

    result |= Q(visibility="department") & no_user_restriction & (
        legacy_department_only | legacy_designation_match | paired_match
    )
    return result


from Layout_Master.models import (
    Menu,
    SubMenu,
    ChildMenu,
    MenuDesignationAccess,
    SubMenuDesignationAccess,
    ChildMenuDesignationAccess,
)


def _has_layout_access(obj, user, level):
    # Public and Login Required menus are visible to everyone.
    # Login enforcement happens when the protected URL is opened.
    if obj.visibility in ("public", "authenticated"):
        return True

    # Department-based menus must be hidden from logged-out users.
    if not user.is_authenticated:
        return False

    if obj.visibility != "department":
        return False

    # Explicitly assigned users receive access directly.
    if obj.users.filter(pk=user.pk).exists():
        return True

    department_id = getattr(user, "department_id", None)
    designation_id = getattr(user, "designation_id", None)

    if not department_id:
        return False

    model_info = {
        "menu": (MenuDesignationAccess, "menu_id"),
        "submenu": (SubMenuDesignationAccess, "submenu_id"),
        "childmenu": (ChildMenuDesignationAccess, "childmenu_id"),
    }.get(level)

    if model_info:
        access_model, fk_field = model_info

        rules = access_model.objects.filter(**{fk_field: obj.pk})

        # Exact department + designation permission.
        if designation_id and rules.filter(
            department_id=department_id,
            designation_id=designation_id,
        ).exists():
            return True

        # Support existing department-only permissions when no
        # department/designation rules have been configured.
        if (
            not rules.exists()
            and obj.departments.filter(pk=department_id).exists()
        ):
            return True

    return False


def layout_menus(request):
    user = request.user
    path = request.path

    visible_menus = []
    active_menu_id = None
    active_submenu_id = None
    active_child_id = None

    menus = Menu.objects.prefetch_related(
        "submenus__child_menus"
    ).order_by("order")

    for menu in menus:
        visible_submenus = []

        for submenu in menu.submenus.all():
            if not _has_layout_access(submenu, user, "submenu"):
                continue

            visible_children = []

            for child in submenu.child_menus.all():
                if _has_layout_access(child, user, "childmenu"):
                    visible_children.append(child)

                    if child.url and path.startswith(child.url):
                        active_menu_id = menu.pk
                        active_submenu_id = submenu.pk
                        active_child_id = child.pk

            submenu.visible_child_menus = visible_children
            visible_submenus.append(submenu)

            if submenu.url and path.startswith(submenu.url):
                active_menu_id = menu.pk
                active_submenu_id = submenu.pk

        # The parent is visible if it is authorized itself or
        # contains at least one submenu the user can access.
        menu_allowed = _has_layout_access(menu, user, "menu")

        if not menu_allowed and not visible_submenus:
            continue

        menu.visible_submenus = visible_submenus
        visible_menus.append(menu)

        if any(
            submenu.url and path.startswith(submenu.url)
            for submenu in visible_submenus
        ):
            active_menu_id = menu.pk

    return {
        "global_menus": visible_menus,
        "active_menu_id": active_menu_id,
        "active_submenu_id": active_submenu_id,
        "active_child_id": active_child_id,
    }