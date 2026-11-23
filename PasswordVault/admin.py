
from django.contrib import admin
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

from .models import (
    PasswordEntry,
    PasswordGroupAccess,
    VaultAudit,
)

from .views import decrypt_password


@admin.register(PasswordEntry)
class PasswordEntryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "username",
        "owner_display",
        "password_display",
    )

    actions = [
        "export_all_passwords",
    ]

    def owner_display(self, obj):
        return (
            f"({obj.owner.username.upper()}) "
            f"{obj.owner.first_name.upper()} "
            f"{obj.owner.last_name.upper()}"
        )

    owner_display.short_description = "Owner"

    def password_display(self, obj):
        try:
            return decrypt_password(obj.encrypted_password)
        except Exception:
            return "Unable to decrypt"

    password_display.short_description = "Password"

    @admin.action(
        description="Export ALL Passwords to Excel"
    )
    def export_all_passwords(self, request, queryset):

        if not request.user.is_superuser:
            raise PermissionDenied

        # Export ALL records, irrespective of selected rows
        all_passwords = PasswordEntry.objects.select_related(
            "owner"
        ).all()

        wb = Workbook()
        ws = wb.active
        ws.title = "Password Vault"

        headers = [
            "Name",
            "Username",
            "Password",
            "Owner",
        ]

        ws.append(headers)

        # Header styling
        for cell in ws[1]:
            cell.font = Font(
                bold=True,
                color="FFFFFF"
            )
            cell.fill = PatternFill(
                start_color="1F4E78",
                end_color="1F4E78",
                fill_type="solid"
            )

        # Add all password records
        for obj in all_passwords:

            try:
                password = decrypt_password(
                    obj.encrypted_password
                )
            except Exception:
                password = "Unable to decrypt"

            ws.append([
                obj.name,
                obj.username,
                password,
                obj.owner.username if obj.owner else "",
            ])

        # Column widths
        for column in ws.columns:
            max_length = max(
                len(str(cell.value or ""))
                for cell in column
            )

            ws.column_dimensions[
                get_column_letter(column[0].column)
            ].width = min(max_length + 4, 40)

        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions

        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )

        response["Content-Disposition"] = (
            'attachment; filename="PasswordVault_All.xlsx"'
        )

        wb.save(response)

        return response

    export_all_passwords.short_description = (
        "Export ALL Passwords to Excel"
    )
