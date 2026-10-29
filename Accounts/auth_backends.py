from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from ldap3 import Server, Connection, SIMPLE, ALL
import logging

from Accounts.models import Department, Designation, Shift


logger = logging.getLogger(__name__)

LDAP_SERVER = 'ldap://192.168.5.100'
BASE_DN = 'DC=aurarcm,DC=org'

User = get_user_model()


class LDAPBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None):

        if not username or not password:
            return None

        # Add domain if missing
        user_to_bind = (
            username
            if '@' in username
            else f"{username}@aurarcm.org"
        )

        try:
            # Connect to AD
            server = Server(
                LDAP_SERVER,
                get_info=ALL
            )

            conn = Connection(
                server,
                user=user_to_bind,
                password=password,
                authentication=SIMPLE,
                auto_bind=True
            )

            # Search username without domain
            search_username = username.split('@')[0]

            # Search AD user
            conn.search(
                BASE_DN,
                f"(sAMAccountName={search_username})",
                attributes=[
                    'givenName',
                    'sn',
                    'mail',
                    'employeeID',
                    'department',
                    'title',
                    'userAccountControl',
                ]
            )

            ad_entry = conn.entries[0] if conn.entries else None

            conn.unbind()

            # If AD user was not found
            if not ad_entry:
                logger.warning(
                    f"LDAP user not found in AD: {search_username}"
                )
                return None

            # Get or create Django user
            user, created = User.objects.get_or_create(
                username=search_username
            )

            # AD password is used for authentication
            user.set_unusable_password()

            # Update Django user from AD
            self.update_user_from_ad(
                user,
                ad_entry
            )

            user.save()

            # IMPORTANT:
            # If AD account is disabled, do not allow login
            if not user.is_active:
                logger.warning(
                    f"AD account disabled: {search_username}"
                )
                return None

            return user

        except Exception:
            logger.exception(
                f"LDAP authentication failed for user: {username}"
            )
            return None


    def update_user_from_ad(self, user, ad_entry):

        # --------------------------------------------------
        # ACCOUNT STATUS
        # --------------------------------------------------

        if (
            ad_entry
            and 'userAccountControl' in ad_entry
            and ad_entry.userAccountControl.value
        ):
            try:
                uac = int(
                    ad_entry.userAccountControl.value
                )

                # ADS_UF_ACCOUNTDISABLE = 0x0002
                if uac & 0x0002:
                    # AD ACCOUNT DISABLED
                    user.is_active = False

                    logger.info(
                        f"AD account disabled: {user.username}"
                    )

                else:
                    # AD ACCOUNT ENABLED
                    user.is_active = True

                    logger.info(
                        f"AD account enabled: {user.username}"
                    )

            except (ValueError, TypeError):
                logger.warning(
                    f"Invalid userAccountControl value "
                    f"for {user.username}"
                )

        # --------------------------------------------------
        # FIRST NAME
        # --------------------------------------------------

        first_name_from_ad = (
            ad_entry.givenName.value
            if ad_entry
            and 'givenName' in ad_entry
            else None
        )

        user.first_name = (
            first_name_from_ad
            if first_name_from_ad
            else "NA"
        )

        # --------------------------------------------------
        # LAST NAME
        # --------------------------------------------------

        last_name_from_ad = (
            ad_entry.sn.value
            if ad_entry
            and 'sn' in ad_entry
            else None
        )

        user.last_name = (
            last_name_from_ad
            if last_name_from_ad
            else ""
        )

        # --------------------------------------------------
        # EMAIL
        # --------------------------------------------------

        email_from_ad = (
            ad_entry.mail.value
            if ad_entry
            and 'mail' in ad_entry
            else None
        )

        user.email = (
            email_from_ad
            if email_from_ad
            else ""
        )

        # --------------------------------------------------
        # EMPLOYEE ID
        # --------------------------------------------------

        employee_id_from_ad = (
            ad_entry.employeeID.value
            if ad_entry
            and "employeeID" in ad_entry
            and ad_entry.employeeID.value
            else None
        )

        if employee_id_from_ad:

            user.employee_id = (
                employee_id_from_ad
                .strip()
                .upper()
            )

        elif user.username:

            user.employee_id = (
                user.username
                .strip()
                .upper()
            )

        else:

            user.employee_id = None

        # --------------------------------------------------
        # DEPARTMENT
        # --------------------------------------------------

        department_from_ad = (
            ad_entry.department.value
            if ad_entry
            and 'department' in ad_entry
            else None
        )

        if department_from_ad:

            dept, _ = Department.objects.get_or_create(
                name=department_from_ad.strip()
            )

            user.department = dept

        # --------------------------------------------------
        # DESIGNATION
        # --------------------------------------------------

        designation_from_ad = (
            ad_entry.title.value
            if ad_entry
            and 'title' in ad_entry
            else None
        )

        if designation_from_ad:

            desig, _ = Designation.objects.get_or_create(
                title=designation_from_ad.strip()
            )

            user.designation = desig



    def get_user(self, user_id):

        try:
            return User.objects.get(
                pk=user_id
            )

        except User.DoesNotExist:
            return None