from ldap3 import Server, Connection, SIMPLE, SUBTREE, ALL

from django.conf import settings
from django.db import transaction

from Accounts.models import AuraInsideUser, SecurityGroup


# ============================================================
# LDAP SETTINGS
# ============================================================

LDAP_SERVER = settings.LDAP_SERVER
LDAP_USER = settings.LDAP_USER
LDAP_PASSWORD = settings.LDAP_PASSWORD
BASE_DN = settings.BASE_DN


# ============================================================
# ACTIVE DIRECTORY ACCOUNT CONTROL FLAG
# ============================================================

# AD userAccountControl flag:
# 0x0002 = ACCOUNTDISABLE
ACCOUNT_DISABLED_FLAG = 0x0002


# ============================================================
# SYNC AD SECURITY GROUPS + ACCOUNT STATUS
# ============================================================

def sync_ad_security_groups():
    """
    Synchronize Active Directory Security Groups into AuraInside DB.

    Also synchronizes AD account status:

        AD Enabled  -> AuraInside active = 1
        AD Disabled -> AuraInside active = 0

    Returns:
    {
        "users_synced": int,
        "groups_created": int,
        "relationships": int,
        "users_not_found": list
    }
    """

    result = {
        "users_synced": 0,
        "groups_created": 0,
        "relationships": 0,
        "users_not_found": [],
    }

    # ========================================================
    # CONNECT TO ACTIVE DIRECTORY
    # ========================================================

    server = Server(
        LDAP_SERVER,
        get_info=ALL
    )

    conn = Connection(
        server,
        user=LDAP_USER,
        password=LDAP_PASSWORD,
        authentication=SIMPLE,
        auto_bind=True,
    )

    try:

        # ====================================================
        # GET ALL AD USERS
        # ====================================================

        conn.search(
            search_base=BASE_DN,

            # Only users, exclude computer accounts
            search_filter="(&(objectClass=user)(!(objectClass=computer)))",

            search_scope=SUBTREE,

            attributes=[
                "sAMAccountName",
                "memberOf",
                "userAccountControl",
            ],
        )

        # ====================================================
        # DATABASE TRANSACTION
        # ====================================================

        with transaction.atomic():

            for entry in conn.entries:

                # =================================================
                # GET USERNAME
                # =================================================

                username = ""

                try:
                    username = str(
                        entry.sAMAccountName.value
                    ).strip()

                except Exception:
                    continue

                if not username:
                    continue

                # =================================================
                # FIND USER IN AURAINSIDE
                # =================================================

                try:

                    user = AuraInsideUser.objects.get(
                        username=username
                    )

                except AuraInsideUser.DoesNotExist:

                    result["users_not_found"].append(
                        username
                    )

                    continue

                except AuraInsideUser.MultipleObjectsReturned:

                    result["users_not_found"].append(
                        f"{username} (Duplicate Username)"
                    )

                    continue

                # =================================================
                # SYNC ACTIVE STATUS FROM ACTIVE DIRECTORY
                # =================================================
                
                try:
                
                    uac_value = entry.userAccountControl.value
                    uac = int(uac_value)
                
                    # 0x0002 = ACCOUNTDISABLE
                
                    if uac & ACCOUNT_DISABLED_FLAG:
                
                        # AD account disabled
                        user.is_active = False
                
                    else:
                
                        # AD account enabled
                        user.is_active = True
                
                except (
                    ValueError,
                    TypeError,
                    AttributeError
                ):
                
                    # Keep existing status if AD value is invalid
                    pass

                # =================================================
                # GET USER'S AD SECURITY GROUPS
                # =================================================

                member_of = getattr(
                    entry,
                    "memberOf",
                    None
                )

                ldap_groups = (
                    member_of.values
                    if member_of
                    else []
                )

                group_objects = []

                # =================================================
                # PROCESS EACH SECURITY GROUP
                # =================================================

                for group_dn in ldap_groups:

                    # Example:
                    #
                    # CN=HR,OU=Groups,DC=aurarcm,DC=org
                    #
                    # becomes:
                    #
                    # HR

                    group_name = (
                        group_dn
                        .split(",")[0]
                        .replace("CN=", "")
                        .strip()
                    )

                    if not group_name:
                        continue

                    # =================================================
                    # GET OR CREATE SECURITY GROUP
                    # =================================================

                    group, created = (
                        SecurityGroup.objects.get_or_create(
                            name=group_name,
                            defaults={
                                "distinguished_name": group_dn
                            },
                        )
                    )

                    # =================================================
                    # NEW GROUP CREATED
                    # =================================================

                    if created:

                        result["groups_created"] += 1

                    # =================================================
                    # UPDATE GROUP DN IF CHANGED
                    # =================================================

                    elif (
                        group.distinguished_name
                        != group_dn
                    ):

                        group.distinguished_name = group_dn

                        group.save(
                            update_fields=[
                                "distinguished_name"
                            ]
                        )

                    group_objects.append(group)

                # =================================================
                # REPLACE OLD GROUPS WITH CURRENT AD GROUPS
                # =================================================

                user.security_groups.set(
                    group_objects
                )

                # =================================================
                # SAVE ACTIVE STATUS
                # =================================================

                user.save(
                    update_fields=[
                        "is_active"
                    ]
                )

                # =================================================
                # UPDATE RESULT COUNTERS
                # =================================================

                result["relationships"] += len(
                    group_objects
                )

                result["users_synced"] += 1

    finally:

        # ========================================================
        # CLOSE LDAP CONNECTION
        # ========================================================

        conn.unbind()

    return result