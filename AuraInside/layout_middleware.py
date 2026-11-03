
from django.shortcuts import redirect
from django.urls import reverse

from Layout_Master.models import (
    SubMenu,
    ChildMenu,
)


class MenuLoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path = request.path.rstrip("/") or "/"

        # Excluded paths
        excluded_paths = [
            "/admin",
            "/static",
            "/media",
            "/login",
            "/logout",
            "/accounts",
        ]

        if any(
            path == item or path.startswith(item + "/")
            for item in excluded_paths
        ):
            return self.get_response(request)

        user = request.user

        # Collect matching URL records
        matches = []

        for submenu in SubMenu.objects.exclude(
            url__isnull=True
        ).exclude(url=""):

            url = submenu.url.rstrip("/") or "/"

            if path == url or path.startswith(url + "/"):
                matches.append({
                    "level": "submenu",
                    "object": submenu,
                    "url": url,
                    "priority": 2,
                })

        for child in ChildMenu.objects.exclude(
            url__isnull=True
        ).exclude(url=""):

            url = child.url.rstrip("/") or "/"

            if path == url or path.startswith(url + "/"):
                matches.append({
                    "level": "childmenu",
                    "object": child,
                    "url": url,
                    "priority": 1,
                })

        if not matches:
            return self.get_response(request)

        # Longest URL wins.
        # If URLs are identical, SubMenu wins over ChildMenu.
        matches.sort(
            key=lambda item: (
                len(item["url"]),
                item["priority"],
            ),
            reverse=True,
        )

        matched = matches[0]
        obj = matched["object"]
        access_type = (obj.visibility or "public").lower()

        # PUBLIC: Allow without login
        if access_type == "public":
            return self.get_response(request)

        # AUTHENTICATED: Login required
        if access_type == "authenticated":
            if not user.is_authenticated:
                return redirect(
                    reverse("Accounts:access_warning")
                )

            return self.get_response(request)

        # DEPARTMENT: User-specific permission
        if access_type == "department":

            if not user.is_authenticated:
                return redirect(
                    reverse("Accounts:access_warning")
                )

            # Explicit user permission
            if obj.users.filter(pk=user.pk).exists():
                return self.get_response(request)

            # Department + Designation permission
            department_id = getattr(user, "department_id", None)
            designation_id = getattr(user, "designation_id", None)

            if department_id and designation_id:

                if obj.designation_rules.filter(
                    department_id=department_id,
                    designation_id=designation_id,
                ).exists():
                    return self.get_response(request)

            # Legacy department-only permission
            if not obj.designation_rules.exists():
                if department_id and obj.departments.filter(
                    pk=department_id
                ).exists():
                    return self.get_response(request)

            return redirect(
                reverse("Accounts:access_warning")
            )

        return self.get_response(request)
