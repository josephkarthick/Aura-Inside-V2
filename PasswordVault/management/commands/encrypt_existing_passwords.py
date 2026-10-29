from django.core.management.base import BaseCommand
from PasswordVault.models import PasswordEntry
from cryptography.fernet import Fernet
from django.conf import settings


class Command(BaseCommand):
    help = "Encrypt existing plain-text Password Vault passwords"

    def handle(self, *args, **options):

        cipher = Fernet(settings.VAULT_SECRET_KEY)

        entries = PasswordEntry.objects.all()

        count = 0

        for entry in entries:

            try:
                # Check whether password is already encrypted
                cipher.decrypt(entry.encrypted_password.encode())

                self.stdout.write(
                    f"SKIPPED: {entry.name} - already encrypted"
                )

            except Exception:

                # Currently plain text → encrypt it
                entry.encrypted_password = cipher.encrypt(
                    entry.encrypted_password.encode()
                ).decode()

                entry.save(update_fields=["encrypted_password"])

                count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"ENCRYPTED: {entry.name} - {entry.username}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nCompleted. {count} passwords encrypted."
            )
        )