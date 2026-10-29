import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from PasswordVault.models import (
    PasswordEntry,
    PasswordGroupAccess,
    GroupPermission,
)

from Accounts.models import SecurityGroup


class Command(BaseCommand):
    help = "Import Password Vault access from CSV"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            type=str
        )

    def handle(self, *args, **options):

        csv_file = options["csv_file"]

        created_count = 0
        updated_count = 0
        skipped_count = 0

        with open(
            csv_file,
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            with transaction.atomic():

                for row_number, row in enumerate(reader, start=2):

                    password_name = row["password_name"].strip()
                    project = row["project"].strip()
                    process = row["process"].strip()
                    permission = row["permission"].strip().lower()

                    # -----------------------------------------
                    # Permission
                    # -----------------------------------------

                    if permission in ["read", "read only"]:
                        permission = GroupPermission.READ

                    elif permission in [
                        "write",
                        "read & write",
                        "read and write"
                    ]:
                        permission = GroupPermission.WRITE

                    else:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Row {row_number}: Invalid permission "
                                f"'{permission}'"
                            )
                        )

                        skipped_count += 1
                        continue

                    # -----------------------------------------
                    # Find Passwords
                    # -----------------------------------------

                    password_entries = PasswordEntry.objects.filter(
                        name=password_name
                    )

                    if not password_entries.exists():

                        self.stdout.write(
                            self.style.ERROR(
                                f"Row {row_number}: Password not found - "
                                f"{password_name}"
                            )
                        )

                        skipped_count += 1
                        continue

                    # -----------------------------------------
                    # Find Security Group
                    # -----------------------------------------

                    try:

                        security_group = SecurityGroup.objects.get(
                            project=project,
                            process=process
                        )

                    except SecurityGroup.DoesNotExist:

                        self.stdout.write(
                            self.style.ERROR(
                                f"Row {row_number}: Security Group not found - "
                                f"{project} / {process}"
                            )
                        )

                        skipped_count += 1
                        continue

                    except SecurityGroup.MultipleObjectsReturned:

                        self.stdout.write(
                            self.style.ERROR(
                                f"Row {row_number}: Multiple Security "
                                f"Groups found - {project} / {process}"
                            )
                        )

                        skipped_count += 1
                        continue

                    # -----------------------------------------
                    # Create / Update Access
                    # For ALL matching password accounts
                    # -----------------------------------------

                    for password_entry in password_entries:

                        access, created = (
                            PasswordGroupAccess.objects.update_or_create(
                                password_entry=password_entry,
                                group_dn=security_group.distinguished_name,
                                defaults={
                                    "permission": permission
                                }
                            )
                        )

                        if created:

                            created_count += 1

                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"ADDED: "
                                    f"{password_entry.name} | "
                                    f"{password_entry.username} | "
                                    f"{project} | "
                                    f"{process} | "
                                    f"{permission}"
                                )
                            )

                        else:

                            updated_count += 1

                            self.stdout.write(
                                f"UPDATED: "
                                f"{password_entry.name} | "
                                f"{password_entry.username} | "
                                f"{project} | "
                                f"{process} | "
                                f"{permission}"
                            )

        # -----------------------------------------
        # Summary
        # -----------------------------------------

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "Import completed."
            )
        )

        self.stdout.write(
            f"Created : {created_count}"
        )

        self.stdout.write(
            f"Updated : {updated_count}"
        )

        self.stdout.write(
            f"Skipped : {skipped_count}"
        )