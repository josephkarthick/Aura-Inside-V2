from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.conf import settings
from Accounts.models import SecurityGroup, AuraInsideUser
from django.db import transaction
from django.views.decorators.http import require_POST
from cryptography.fernet import Fernet

from ADManager.views import (
    get_user_ldap_group_dns,
    get_all_ldap_groups
)

from Accounts.models import SecurityGroup

from .models import (
    PasswordEntry,
    PasswordGroupAccess,
    GroupPermission,
    PasswordUserAccess,    
    VaultAudit
)

# ==========================================================
# 🔐 Encryption helpers
# ==========================================================

_cipher = Fernet(settings.VAULT_SECRET_KEY)


def encrypt_password(password):
    return _cipher.encrypt(password.encode()).decode()


def decrypt_password(encrypted):
    return _cipher.decrypt(encrypted.encode()).decode()


# ==========================================================
# 🔑 Permission helpers
# ==========================================================

def has_read_access(request, user, entry):
    if entry.owner == user:
        return True

    # Individual user access
    user_access = entry.user_access.filter(
        user=user
    ).first()

    if user_access:
        return True

    # LDAP group access
    user_groups = request.session.get("ldap_groups", [])

    return entry.group_access.filter(
        group_dn__in=user_groups
    ).exists()


def has_write_access(request, user, entry):
    if entry.owner == user:
        return True

    # Individual permission overrides group permission
    user_access = entry.user_access.filter(
        user=user
    ).first()

    if user_access:
        return user_access.permission == GroupPermission.WRITE

    # LDAP group permission
    user_groups = request.session.get("ldap_groups", [])

    return entry.group_access.filter(
        group_dn__in=user_groups,
        permission=GroupPermission.WRITE
    ).exists()


# ==========================================================
# 📄 Views
# ==========================================================

@login_required
def vault_list(request):
    # Get LDAP groups for the logged-in user
    if "ldap_groups" not in request.session:
        request.session["ldap_groups"] = get_user_ldap_group_dns(
            request.user.username
        )

    user = request.user
    user_groups = request.session.get("ldap_groups", [])

    # -----------------------------------------
    # Access Filter
    # -----------------------------------------
    filters = (
        Q(owner=user) |
        Q(shared_with=user) |
        Q(user_access__user=user)
    )

    # Allow access through LDAP groups
    if user_groups:
        filters |= Q(
            group_access__group_dn__in=user_groups
        )

    # -----------------------------------------
    # Get Password Entries
    # -----------------------------------------
    entries = (
        PasswordEntry.objects
        .filter(filters)
        .distinct()
        .order_by("name", "id")
    )

    # -----------------------------------------
    # Determine Edit Permission
    # -----------------------------------------
    for entry in entries:
        entry.can_edit = has_write_access(
            request,
            user,
            entry
        )

    # -----------------------------------------
    # Count
    # -----------------------------------------
    voip_count = entries.count()

    security_groups = SecurityGroup.objects.all().order_by(
        "project",
        "process"
    )
    
    project_users = {}
    
    for group in security_groups:
    
        users = (
            AuraInsideUser.objects
            .filter(
                is_active=True,
                security_groups=group
            )
            .distinct()
            .order_by("first_name", "last_name")
        )
    
        project_users[group.distinguished_name] = [
            {
                "id": user.id,
                "name": (
                    f"{user.first_name} {user.last_name}".strip()
                    or user.username
                )
            }
            for user in users
        ]

    # -----------------------------------------
    # Render
    # -----------------------------------------
    return render(
        request,
        "PasswordVault/password_list.html",
        {
            "entries": entries,
            "voip_count": voip_count,
            "security_groups": security_groups,
            "project_users": project_users,
            "permissions": GroupPermission.choices,            
        }
    )


# ----------------------------------------------------------
@login_required
def vault_add(request):

    if request.method == "POST":

        print("POST DATA:", request.POST)

        # ==========================================================
        # Create Password
        # ==========================================================

        entry = PasswordEntry.objects.create(
            name=request.POST["name"],
            url=request.POST.get("url"),
            username=request.POST["username"],
            email_id=request.POST.get("email_id"),

            encrypted_password=encrypt_password(
                request.POST["password"]
            ),

            recovery_code=request.POST.get("recovery_code"),
            security_questions=request.POST.get("security_questions"),

            notes=request.POST.get("notes"),
            owner=request.user
        )

        # ==========================================================
        # Project / Process Access
        # ==========================================================
        
        group_dns = request.POST.getlist("group_dn[]")
        permissions = request.POST.getlist("permission[]")
        
        print("GROUP DNS:", group_dns)
        print("PERMISSIONS:", permissions)
        
        # Prevent duplicate group access
        group_access = {}
        
        for group_dn, permission in zip(group_dns, permissions):
        
            if not group_dn or not permission:
                continue
        
            # Keep the latest permission for each group
            group_access[group_dn] = permission
        
        
        for group_dn, permission in group_access.items():
        
            PasswordGroupAccess.objects.create(
                password_entry=entry,
                group_dn=group_dn,
                permission=permission
            )

        # ==========================================================
        # Individual User Access
        # ==========================================================

        user_ids = request.POST.getlist("user_id[]")
        user_permissions = request.POST.getlist(
            "user_permission[]"
        )

        print("USER IDS:", user_ids)
        print("USER PERMISSIONS:", user_permissions)

        for user_id, permission in zip(
            user_ids,
            user_permissions
        ):

            if not user_id or not permission:
                continue

            PasswordUserAccess.objects.create(
                password_entry=entry,
                user_id=user_id,
                permission=permission
            )

        # ==========================================================
        # Audit
        # ==========================================================

        VaultAudit.objects.create(
            user=request.user,
            action="created",
            password_entry=entry
        )

        return redirect(
            "passwordvault:vault_list"
        )

    # ==========================================================
    # GET
    # ==========================================================

    security_groups = (
        SecurityGroup.objects
        .all()
        .order_by(
            "project",
            "process"
        )
    )

    projects = (
        SecurityGroup.objects
        .values_list(
            "project",
            flat=True
        )
        .distinct()
        .order_by("project")
    )

    # ==========================================================
    # Get Users Belonging To Each Project
    # ==========================================================

    project_users = {}
    
    for group in security_groups:
        users = (
            AuraInsideUser.objects
            .filter(
                is_active=True,
                security_groups=group
            )
            .distinct()
            .order_by("first_name", "last_name")
        )
    
        project_users[group.distinguished_name] = [
            {
                "id": user.id,
                "name": (
                    f"{user.first_name} {user.last_name}".strip()
                    or user.username
                ),
            }
            for user in users
        ]

    # ==========================================================
    # Render Template
    # ==========================================================

    return render(
        request,
        "PasswordVault/password_add.html",
        {
            "security_groups": security_groups,
            "projects": projects,
            "project_users": project_users,
            "permissions": GroupPermission.choices,
        }
    )

# ----------------------------------------------------------

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404

@login_required
def vault_view(request, pk):
    entry = get_object_or_404(PasswordEntry, pk=pk)

    # Check read access
    if not has_read_access(request, request.user, entry):
        return HttpResponseForbidden("Read access denied")

    try:
        # Decrypt password
        password = decrypt_password(entry.encrypted_password)

        # Create audit log
        VaultAudit.objects.create(
            user=request.user,
            action="viewed",
            password_entry=entry
        )

        response = JsonResponse({
            "password": password
        })

        # Prevent browser/proxy caching
        response["Cache-Control"] = "no-store, no-cache, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"

        return response

    except Exception:
        return JsonResponse({
            "error": "Unable to retrieve password"
        }, status=500)


# ----------------------------------------------------------

@login_required
def vault_edit(request, pk):

    entry = get_object_or_404(PasswordEntry, pk=pk)

    if not has_write_access(request, request.user, entry):
        return HttpResponseForbidden("Write access denied")

    # ==========================================================
    # POST
    # ==========================================================

    if request.method == "POST":

        # ------------------------------------------------------
        # Basic Details
        # ------------------------------------------------------

        entry.name = request.POST["name"]
        entry.url = request.POST.get("url")
        entry.username = request.POST["username"]
        entry.email_id = request.POST.get("email_id")

        entry.recovery_code = request.POST.get("recovery_code")
        entry.security_questions = request.POST.get(
            "security_questions"
        )
        entry.notes = request.POST.get("notes")

        # ------------------------------------------------------
        # Password
        # ------------------------------------------------------

        new_password = request.POST.get("password")

        if new_password:
            entry.encrypted_password = encrypt_password(
                new_password
            )

        entry.save()

        # ======================================================
        # REMOVE EXISTING ACCESS
        # ======================================================

        PasswordGroupAccess.objects.filter(
            password_entry=entry
        ).delete()

        PasswordUserAccess.objects.filter(
            password_entry=entry
        ).delete()

        # ======================================================
        # GROUP ACCESS
        # ======================================================

        group_dns = request.POST.getlist("group_dn[]")
        permissions = request.POST.getlist("permission[]")

        print("GROUP DNS:", group_dns)
        print("PERMISSIONS:", permissions)

        # Prevent duplicate group access
        group_access = {}

        for group_dn, permission in zip(
            group_dns,
            permissions
        ):

            if not group_dn or not permission:
                continue

            group_access[group_dn] = permission

        for group_dn, permission in group_access.items():

            PasswordGroupAccess.objects.create(
                password_entry=entry,
                group_dn=group_dn,
                permission=permission
            )

        # ======================================================
        # INDIVIDUAL USER ACCESS
        # ======================================================
        
        user_ids = request.POST.getlist("user_id[]")
        
        user_permissions = request.POST.getlist(
            "user_permission[]"
        )
        
        user_group_dns = request.POST.getlist(
            "user_group_dn[]"
        )
        
        print("USER IDS:", user_ids)
        print("USER PERMISSIONS:", user_permissions)
        print("USER GROUP DNS:", user_group_dns)
        
        # Prevent duplicate individual users per group
        user_access = {}
        
        for user_id, permission, group_dn in zip(
            user_ids,
            user_permissions,
            user_group_dns
        ):
        
            if not user_id or not permission or not group_dn:
                continue
        
            key = (user_id, group_dn)
        
            user_access[key] = permission
        
        
        for (user_id, group_dn), permission in user_access.items():
        
            PasswordUserAccess.objects.create(
                password_entry=entry,
                user_id=user_id,
                group_dn=group_dn,
                permission=permission
            )

        # ======================================================
        # AUDIT
        # ======================================================

        VaultAudit.objects.create(
            user=request.user,
            action="updated",
            password_entry=entry
        )

        return redirect(
            "passwordvault:vault_list"
        )

    # ==========================================================
    # GET
    # ==========================================================

    # ==========================================================
    # EXISTING GROUP ACCESS
    # ==========================================================

    existing_access = []

    accesses = PasswordGroupAccess.objects.filter(
        password_entry=entry
    )

    for access in accesses:

        try:

            security_group = SecurityGroup.objects.get(
                distinguished_name=access.group_dn
            )

            existing_access.append({
                "id": security_group.id,
                "project": security_group.project,
                "process": security_group.process,
                "group_dn": security_group.distinguished_name,
                "permission": access.permission,
            })

        except SecurityGroup.DoesNotExist:
            continue

    # ==========================================================
    # EXISTING INDIVIDUAL USER ACCESS
    # ==========================================================

    existing_user_access = []

    user_accesses = PasswordUserAccess.objects.filter(
        password_entry=entry
    ).select_related("user")

    for access in user_accesses:

        existing_user_access.append({
            "user_id": access.user_id,
        
            "username": (
                f"{access.user.first_name} "
                f"{access.user.last_name}"
            ).strip() or access.user.username,
        
            "group_dn": access.group_dn,
        
            "permission": access.permission,
        })

    # ==========================================================
    # ALL SECURITY GROUPS
    # ==========================================================

    security_groups = (
        SecurityGroup.objects
        .all()
        .order_by("project", "process")
    )

    # ==========================================================
    # PROJECTS / PROCESSES
    # ==========================================================

    projects = {}

    for group in security_groups:

        if group.project not in projects:
            projects[group.project] = []

        projects[group.project].append({
            "id": group.id,
            "process": group.process,
            "group_dn": group.distinguished_name,
        })

    # ==========================================================
    # PROJECT USERS BY GROUP DN
    # ==========================================================

    project_users = {}

    for group in security_groups:

        users = (
            AuraInsideUser.objects
            .filter(
                is_active=True,
                security_groups=group
            )
            .distinct()
            .order_by("first_name", "last_name")
        )

        project_users[group.distinguished_name] = [
            {
                "id": user.id,
                "name": (
                    f"{user.first_name} "
                    f"{user.last_name}"
                ).strip() or user.username,
            }
            for user in users
        ]

    # ==========================================================
    # RENDER
    # ==========================================================

    return render(
        request,
        "PasswordVault/password_edit.html",
        {
            "entry": entry,
            "security_groups": security_groups,
            "projects": projects,
            "project_users": project_users,
            "existing_access": existing_access,
            "existing_user_access": existing_user_access,
            "permissions": GroupPermission.choices,
        }
    )


# ----------------------------------------------------------

@login_required
def vault_delete(request, pk):
    entry = get_object_or_404(PasswordEntry, pk=pk)

    if entry.owner != request.user:
        return HttpResponseForbidden("Only owner can delete")

    VaultAudit.objects.create(
        user=request.user,
        action="deleted",
        password_entry=entry
    )

    entry.delete()
    return redirect("passwordvault:vault_list")


# ==========================================================
# BULK SHARE PASSWORDS
# ==========================================================

@login_required
@require_POST
def vault_bulk_share(request):

    password_ids = request.POST.getlist("password_ids[]")

    group_dns = request.POST.getlist("group_dn[]")
    permissions = request.POST.getlist("permission[]")

    user_ids = request.POST.getlist("user_id[]")
    user_permissions = request.POST.getlist("user_permission[]")
    user_group_dns = request.POST.getlist("user_group_dn[]")

    if not password_ids:
        return JsonResponse(
            {"error": "Please select at least one password."},
            status=400
        )

    # Validate selected passwords
    entries = list(
        PasswordEntry.objects.filter(
            id__in=password_ids
        ).select_related("owner")
    )

    if len(entries) != len(set(password_ids)):
        return JsonResponse(
            {"error": "One or more selected passwords are invalid."},
            status=400
        )

    # Only owners or users with write access can manage sharing
    for entry in entries:
        if not has_write_access(request, request.user, entry):
            return HttpResponseForbidden(
                f"You cannot manage access for {entry.name}."
            )

    # Prepare and validate group permissions
    group_access = {}

    valid_permissions = {
        value for value, label in GroupPermission.choices
    }

    for group_dn, permission in zip(group_dns, permissions):

        if not group_dn or permission not in valid_permissions:
            return JsonResponse(
                {"error": "Invalid project/process permission."},
                status=400
            )

        if not SecurityGroup.objects.filter(
            distinguished_name=group_dn
        ).exists():
            return JsonResponse(
                {"error": "Invalid security group."},
                status=400
            )

        group_access[group_dn] = permission

    # Prepare and validate individual user permissions
    user_access = {}

    for user_id, permission, group_dn in zip(
        user_ids,
        user_permissions,
        user_group_dns
    ):

        if (
            not user_id
            or not group_dn
            or permission not in valid_permissions
        ):
            return JsonResponse(
                {"error": "Invalid individual user permission."},
                status=400
            )

        valid_user = AuraInsideUser.objects.filter(
            id=user_id,
            is_active=True,
            security_groups__distinguished_name=group_dn
        ).exists()

        if not valid_user:
            return JsonResponse(
                {"error": "Invalid user or process assignment."},
                status=400
            )

        user_access[(user_id, group_dn)] = permission

    if not group_access and not user_access:
        return JsonResponse(
            {"error": "Please select at least one access permission."},
            status=400
        )

    # Apply access to all selected passwords
    try:
        with transaction.atomic():

            for entry in entries:

                # LDAP Group Access
                for group_dn, permission in group_access.items():

                    PasswordGroupAccess.objects.update_or_create(
                        password_entry=entry,
                        group_dn=group_dn,
                        defaults={
                            "permission": permission
                        }
                    )

                # Individual User Access
                for (user_id, group_dn), permission in user_access.items():

                    PasswordUserAccess.objects.update_or_create(
                        password_entry=entry,
                        user_id=user_id,
                        group_dn=group_dn,
                        defaults={
                            "permission": permission
                        }
                    )

                # Audit
                VaultAudit.objects.create(
                    user=request.user,
                    action="bulk_shared",
                    password_entry=entry
                )

    except Exception:
        return JsonResponse(
            {"error": "Bulk sharing failed. No changes were saved."},
            status=500
        )

    return redirect("passwordvault:vault_list")