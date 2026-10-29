from ldap3 import Server, Connection, ALL
from django.conf import settings
from django.conf import settings

LDAP_SERVER = settings.LDAP_SERVER
LDAP_DOMAIN = settings.LDAP_DOMAIN


def authenticate_with_ldap(username, password):
    try:
        server = Server(settings.LDAP_SERVER, get_info=ALL)
        user_dn = f"{settings.LDAP_DOMAIN}\\{username}"  # DOMAIN\\username format

        conn = Connection(server, user=user_dn, password=password, authentication="SIMPLE", auto_bind=True)

        if conn.bind():
            conn.unbind()
            return True
        return False

    except Exception as e:
        print(f"[LDAP ERROR] {e}")
        return False

