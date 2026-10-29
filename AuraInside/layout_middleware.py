
import logging

from django.shortcuts import redirect
from django.urls import reverse

from Layout_Master.models import (
    Menu,
    SubMenu,
    ChildMenu,
    MenuDesignationAccess,
    SubMenuDesignationAccess,
    ChildMenuDesignationAccess,
)

logger = logging.getLogger("aurainside")


class MenuLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.rstrip("/") or "/"
        user = request.user

        # Skip login, logout, account, admin, static and media routes.
        if path.startswith((
            "/admin",
            "/static/",
            "/media/",
            "/login",
            "/logout",
            "/accounts/",
        )):
            return self.get_response(request)

        def matches(url):
            if not url:
                return False

            url = url.rstrip("/") or "/"

            return path == url or (
                url != "/" and path.startswith(url + "/")
            )

        def allowed(obj, level):
            if obj.visibility in ("public", "authenticated"):
                result = (
                    obj.visibility == "public"
                    or user.is_authenticated
                )
                logger.warning(
                    "LAYOUT ACCESS | user=%s path=%s level=%s "
                    "item_id=%s visibility=%s allowed=%s",
                    getattr(user, "username", "anonymous"),
                    path, level, obj.pk, obj.visibility, result,
                )
                return result

            if not user.is_authenticated:
                logger.warning(
                    "LAYOUT DENIED | anonymous user path=%s level=%s item=%s",
                    path, level, obj.pk,
                )
                return False

            if obj.visibility != "department":
                logger.warning(
                    "LAYOUT DENIED | user=%s path=%s level=%s "
                    "item=%s unexpected_visibility=%s",
                    user.username, path, level, obj.pk, obj.visibility,
                )
                return False

            # Explicit user grant.
            if obj.users.filter(pk=user.pk).exists():
                logger.warning(
                    "LAYOUT ACCESS | explicit user grant user=%s "
                    "path=%s level=%s item=%s",
                    user.username, path, level, obj.pk,
                )
                return True

            department_id = getattr(user, "department_id", None)
            designation_id = getattr(user, "designation_id", None)

            if not department_id:
                logger.warning(
                    "LAYOUT DENIED | user=%s path=%s level=%s "
                    "item=%s missing_department",
                    user.username, path, level, obj.pk,
                )
                return False

            access_models = {
                "menu": (MenuDesignationAccess, "menu"),
                "submenu": (SubMenuDesignationAccess, "submenu"),
                "childmenu": (ChildMenuDesignationAccess, "childmenu"),
            }

            access_model, field = access_models[level]
            rules = access_model.objects.filter(**{field: obj})

            rule_rows = list(
                rules.values("department_id", "designation_id")
            )

            logger.warning(
                "LAYOUT ACCESS CHECK | user=%s path=%s level=%s "
                "item_id=%s item_url=%s department=%s designation=%s "
                "visibility=%s rules=%s",
                user.username,
                path,
                level,
                obj.pk,
                obj.url,
                department_id,
                designation_id,
                obj.visibility,
                rule_rows,
            )

            # Exact department + designation grant.
            if designation_id and rules.filter(
                department_id=department_id,
                designation_id=designation_id,
            ).exists():
                return True

            # Legacy department-only grant is allowed only when
            # no department/designation pair rules exist for this item.
            if (
                not rules.exists()
                and obj.departments.filter(pk=department_id).exists()
            ):
                return True

            logger.warning(
                "LAYOUT DENIED | user=%s path=%s level=%s item_id=%s",
                user.username, path, level, obj.pk,
            )
            return False

        # Find the most specific matching child-menu URL.
        child = max(
            (
                item
                for item in ChildMenu.objects.select_related(
                    "submenu__menu"
                )
                if matches(item.url)
            ),
            key=lambda item: len((item.url or "").rstrip("/")),
            default=None,
        )

        if child:
            if not allowed(child, "childmenu"):
                return redirect(reverse("Accounts:access_warning"))
            return self.get_response(request)

        # Otherwise check submenu URL.
        submenu = max(
            (
                item
                for item in SubMenu.objects.all()
                if matches(item.url)
            ),
            key=lambda item: len((item.url or "").rstrip("/")),
            default=None,
        )

        if submenu:
            if not allowed(submenu, "submenu"):
                return redirect(reverse("Accounts:access_warning"))
            return self.get_response(request)

        # Finally check parent-menu URL.
        menu = None

        if menu and not allowed(menu, "menu"):
            return redirect(reverse("Accounts:access_warning"))

        return self.get_response(request)
