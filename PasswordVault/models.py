from django.db import models
from Accounts.models import AuraInsideUser


class GroupPermission(models.TextChoices):
    READ = "read", "Read Only"
    WRITE = "write", "Read & Write"


class PasswordEntry(models.Model):
    name = models.CharField(max_length=200)
    url = models.TextField(null=True, blank=True)
    username = models.CharField(max_length=200)
    email_id = models.EmailField(
        null=True,
        blank=True
    )    
    encrypted_password = models.TextField()
    recovery_code = models.TextField(
        null=True,
        blank=True
    )
    security_questions = models.TextField(
        null=True,
        blank=True
    )    

    owner = models.ForeignKey(
        AuraInsideUser,
        on_delete=models.CASCADE,
        related_name="owned_passwords"
    )

    shared_with = models.ManyToManyField(
        AuraInsideUser,
        blank=True,
        related_name="shared_passwords"
    )

    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PasswordGroupAccess(models.Model):
    password_entry = models.ForeignKey(
        PasswordEntry,
        on_delete=models.CASCADE,
        related_name="group_access"
    )

    group_dn = models.CharField(max_length=512, db_index=True)

    permission = models.CharField(
        max_length=10,
        choices=GroupPermission.choices,
        default=GroupPermission.READ
    )

    class Meta:
        unique_together = ("password_entry", "group_dn")

    def __str__(self):
        return f"{self.password_entry} - {self.group_dn} ({self.permission})"


class PasswordUserAccess(models.Model):
    password_entry = models.ForeignKey(
        PasswordEntry,
        on_delete=models.CASCADE,
        related_name="user_access"
    )

    user = models.ForeignKey(
        AuraInsideUser,
        on_delete=models.CASCADE,
        related_name="password_access"
    )

    # Reference the LDAP group/process
    group_dn = models.CharField(
        max_length=512,
        db_index=True
    )

    permission = models.CharField(
        max_length=10,
        choices=GroupPermission.choices,
        default=GroupPermission.READ
    )

    class Meta:
        unique_together = (
            "password_entry",
            "user",
            "group_dn"
        )

    def __str__(self):
        return (
            f"{self.password_entry} - "
            f"{self.user.username} - "
            f"{self.permission}"
        )

class VaultAudit(models.Model):
    user = models.ForeignKey(
        AuraInsideUser,
        on_delete=models.CASCADE,
        related_name="vault_audits"
    )
    action = models.CharField(max_length=50)
    password_entry = models.ForeignKey(
        PasswordEntry,
        on_delete=models.CASCADE,
        related_name="audits"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
