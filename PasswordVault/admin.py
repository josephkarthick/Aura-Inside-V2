from django.contrib import admin

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

    def owner_display(self, obj):
        return f"({obj.owner.username.upper()}) {obj.owner.first_name.upper()} {obj.owner.last_name.upper()}"

    owner_display.short_description = "Owner"

    def password_display(self, obj):
        try:
            return decrypt_password(
                obj.encrypted_password
            )
        except Exception:
            return "Unable to decrypt"

    password_display.short_description = "Password"