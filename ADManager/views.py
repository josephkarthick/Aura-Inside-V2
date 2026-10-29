from django.shortcuts import render, redirect
from django.contrib import messages
import re
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.shortcuts import render, redirect
from django.contrib import messages
from ldap3 import Server, Connection, ALL, SIMPLE, SUBTREE, MODIFY_ADD, MODIFY_DELETE, MODIFY_REPLACE
import csv
from django.http import HttpResponse
from .ldap_sync import sync_ad_security_groups

from django.conf import settings

LDAP_SERVER = settings.LDAP_SERVER
LDAP_USER = settings.LDAP_USER
LDAP_PASSWORD = settings.LDAP_PASSWORD
BASE_DN = settings.BASE_DN


def aduser(request):
    search_term = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', 'enabled')

    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(
        server,
        user=LDAP_USER,
        password=LDAP_PASSWORD,
        authentication=SIMPLE,
        auto_bind=True
    )

    if request.method == 'POST':
        user_dn = request.POST.get('user_dn')
        action = request.POST.get('action')
        selected_groups = request.POST.getlist('group_dns')

        if user_dn and selected_groups and action:
            for group_dn in selected_groups:
                conn.modify(group_dn, {
                    'member': [
                        (
                            MODIFY_ADD if action == 'add' else MODIFY_DELETE,
                            [user_dn]
                        )
                    ]
                })

            messages.success(
                request,
                f"✅ User {action}ed in {len(selected_groups)} group(s)."
            )
        else:
            messages.error(request, "❌ Missing fields or invalid request.")

        conn.unbind()
        return redirect('ADManager:ldap_employee_list')

    # ============================================================
    # LDAP SEARCH
    # Show BOTH ENABLED and DISABLED AD users
    # ============================================================

    if search_term:
        search_filter = (
            f'(&(objectClass=user)'
            f'(!(objectClass=computer))'
            f'(|'
            f'(cn=*{search_term}*)'
            f'(sAMAccountName=*{search_term}*)'
            f'(mail=*{search_term}*)'
            f'(department=*{search_term}*)'
            f'))'
        )
    else:
        search_filter = (
            '(&(objectClass=user)'
            '(!(objectClass=computer))'
            ')'
        )

    attributes = [
        'sAMAccountName',
        'cn',
        'mail',
        'title',
        'department',
        'telephoneNumber',
        'distinguishedName',
        'memberOf',
        'userAccountControl',
        'lockoutTime'
    ]

    conn.search(
        BASE_DN,
        search_filter,
        SUBTREE,
        attributes=attributes
    )

    user_data = []

    for entry in conn.entries:

        # ========================================================
        # Groups
        # ========================================================

        groups = entry.memberOf.values if 'memberOf' in entry else []

        group_pairs = [
            (dn.split(',')[0].replace('CN=', ''), dn)
            for dn in groups
        ]

        # ========================================================
        # Account Lock Status
        # ========================================================

        try:
            lockout_time = int(entry.lockoutTime.value) \
                if 'lockoutTime' in entry else 0
        except Exception:
            lockout_time = 0

        account_locked = (
            lockout_time not in
            (0, 9223372036854775807)
        )

        # ========================================================
        # Account Enabled / Disabled Status
        #
        # userAccountControl bit 2:
        # 0 = Enabled
        # 1 = Disabled
        # ========================================================

        try:
            uac = int(entry.userAccountControl.value)
            account_enabled = (uac & 2) == 0
        except Exception:
            account_enabled = False

        user_data.append({
            'username': (
                entry.sAMAccountName.value
                if entry.sAMAccountName else ''
            ),

            'name': (
                entry.cn.value
                if entry.cn else ''
            ),

            'email': (
                entry.mail.value
                if entry.mail else ''
            ),

            'title': (
                entry.title.value
                if entry.title else ''
            ),

            'department': (
                entry.department.value
                if entry.department else ''
            ),

            'phone': (
                entry.telephoneNumber.value
                if entry.telephoneNumber else ''
            ),

            'groups': group_pairs,

            'dn': (
                entry.distinguishedName.value
                if entry.distinguishedName else ''
            ),

            # Used by toggle button
            'account_enabled': account_enabled,

            # Optional display/status
            'account_locked': account_locked,
        })

    # ============================================================
    # FILTER ACCOUNT STATUS
    # Default = ENABLED
    # ============================================================

    if status_filter == 'enabled':
        user_data = [
            user for user in user_data
            if user['account_enabled']
        ]

    elif status_filter == 'disabled':
        user_data = [
            user for user in user_data
            if not user['account_enabled']
        ]

    # status_filter == 'all'
    # No filtering

    # Sort alphabetically
    user_data.sort(
        key=lambda x: x['username'].lower()
        if x['username'] else ''
    )

    # ============================================================
    # FETCH ALL GROUPS
    # ============================================================

    conn.search(
        BASE_DN,
        '(objectClass=group)',
        SUBTREE,
        attributes=['cn', 'distinguishedName']
    )

    all_groups = sorted(
        [
            (
                e.cn.value,
                e.distinguishedName.value
            )
            for e in conn.entries
        ],
        key=lambda x: x[0].lower()
    )

    # ============================================================
    # FETCH ALL OUs
    # ============================================================

    conn.search(
        BASE_DN,
        '(objectClass=organizationalUnit)',
        SUBTREE,
        attributes=['distinguishedName']
    )

    ous = []

    for entry in conn.entries:
        dn = entry.distinguishedName.value
        name = dn.split(',')[0].replace('OU=', '')
        ous.append((name, dn))

    conn.unbind()

    return render(
        request,
        'ADManager/ADUser_list.html',
        {
            'employees': user_data,
            'all_groups': all_groups,
            'total_users': len(user_data),
            'ous': ous,
            'search_term': search_term,
            'status_filter': status_filter,
        }
    )

def fetch_ldap_user_by_username(username):
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, authentication=SIMPLE, auto_bind=True)

    search_filter = f'(&(objectClass=user)(sAMAccountName={username}))'
    attributes = ['sAMAccountName', 'cn', 'mail', 'title', 'department', 'telephoneNumber', 'distinguishedName', 'manager', 'memberOf', 'userAccountControl', 'lockoutTime']

    conn.search(BASE_DN, search_filter, SUBTREE, attributes=attributes)

    if conn.entries:
        entry = conn.entries[0]

        # Handle group memberships
        groups = entry.memberOf.values if 'memberOf' in entry else []
        group_pairs = [(dn.split(',')[0].replace('CN=', ''), dn) for dn in groups]

        # Handle lockoutTime safely
        lockout_time_raw = entry.lockoutTime.value if 'lockoutTime' in entry else 0
        if hasattr(lockout_time_raw, 'timestamp'):  # If it's a datetime object
            lockout_time = 0
        else:
            try:
                lockout_time = int(lockout_time_raw)
            except Exception:
                lockout_time = 0

        # Determine if account is locked
        account_locked = lockout_time not in (0, 9223372036854775807)

        # Determine if account is enabled (userAccountControl)
        try:
            uac = int(entry.userAccountControl.value)
            ACCOUNTDISABLE = 2
            account_enabled = (uac & ACCOUNTDISABLE) == 0
        except Exception:
            account_enabled = False

        user_data = {
            'username': entry.sAMAccountName.value,
            'name': entry.cn.value,
            'email': entry.mail.value,
            'title': entry.title.value,
            'department': entry.department.value,
            'phone': entry.telephoneNumber.value,
            'dn': entry.distinguishedName.value,
            'manager': getattr(entry, 'manager', None),
            'groups': group_pairs,
            'account_enabled': account_enabled,
            'account_locked': account_locked,
        }
        

        conn.unbind()
        return user_data
    else:
        conn.unbind()
        return None
    
from datetime import datetime, timedelta

def filetime_to_datetime(filetime):
    try:
        # Already a datetime? Validate it.
        if isinstance(filetime, datetime):
            return filetime if 1601 <= filetime.year <= 9999 else "Never"

        # Handle None, 0, or max values
        if not filetime:
            return "Never"

        # Cast to int safely
        filetime = int(filetime)

        # Reserved or invalid values
        if filetime in (0, 9223372036854775807):
            return "Never"

        # Too big to convert (beyond year ~9999)
        if filetime > 265046774399000000:
            return "Never"

        # Convert to datetime
        dt = datetime(1601, 1, 1) + timedelta(microseconds=filetime // 10)

        # Validate again
        return dt if 1601 <= dt.year <= 9999 else "Never"
    except Exception:
        return "Never"



def ad_user_detail(request, username):
    user = fetch_ldap_user_by_username(username)
    if not user:
        messages.error(request, f"No LDAP user found with username: {username}")
        return redirect('ADManager:ldap_employee_list')

    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, authentication=SIMPLE, auto_bind=True)

    # Fetch extra user attributes
    conn.search(user['dn'], '(objectClass=*)', attributes=['accountExpires', 'pwdLastSet', 'userAccountControl'])
    entry = conn.entries[0] if conn.entries else None

    # Safe conversion
    raw_account_expires = getattr(entry, 'accountExpires', None)
    account_expires = filetime_to_datetime(raw_account_expires.value if raw_account_expires else None)
# After: account_expires = filetime_to_datetime(entry.accountExpires.value)

    try:
        if isinstance(account_expires, datetime):
            # This will raise if the date is out of range for timezone.localtime
            _ = timezone.localtime(account_expires)
        else:
            raise ValueError("Not a datetime")
    except Exception:
        account_expires = "Never"

    pwd_last_set = filetime_to_datetime(entry.pwdLastSet.value if 'pwdLastSet' in entry else None)
    uac = int(entry.userAccountControl.value) if 'userAccountControl' in entry else 0

    # Decode flags
    ACCOUNTDISABLE = 2
    LOCKOUT = 16
    DONT_EXPIRE_PASSWORD = 65536

    is_disabled = bool(uac & ACCOUNTDISABLE)
    is_locked = bool(uac & LOCKOUT)
    password_never_expires = bool(uac & DONT_EXPIRE_PASSWORD)

    # POST actions
    if request.method == 'POST':
        action = request.POST.get('action')
        group_dn = request.POST.get('group_dn') or request.POST.get('new_group')
        try:
            if action == 'add_group':
                success = conn.modify(group_dn, {'member': [(MODIFY_ADD, [user['dn']])]})
                messages.success(request, "✅ Added to group" if success else f"❌ Add failed: {conn.result['message']}")
            elif action == 'remove_group':
                success = conn.modify(group_dn, {'member': [(MODIFY_DELETE, [user['dn']])]})
                messages.success(request, "✅ Removed from group" if success else f"❌ Remove failed: {conn.result['message']}")
            elif action in ('enable_account', 'disable_account'):
                conn.search(user['dn'], '(objectClass=*)', attributes=['userAccountControl'])
                if not conn.entries:
                    messages.error(request, "❌ Could not fetch userAccountControl attribute.")
                    conn.unbind()
                    return redirect('ADManager:ad_user_detail', username=username)
                current_uac = int(conn.entries[0].userAccountControl.value)
                new_uac = (current_uac & ~ACCOUNTDISABLE) if action == 'enable_account' else (current_uac | ACCOUNTDISABLE)
                success = conn.modify(user['dn'], {'userAccountControl': [(MODIFY_REPLACE, [new_uac])]})
                messages.success(request, f"✅ Account {'enabled' if action == 'enable_account' else 'disabled'}."
                                 if success else f"❌ Failed to update account status: {conn.result['message']}")
            elif action == 'enable_password_expiry':
                try:
                    new_uac = uac & ~DONT_EXPIRE_PASSWORD
                    uac_result = conn.modify(user['dn'], {'userAccountControl': [(MODIFY_REPLACE, [new_uac])]})
                    pwd_last_set_result = conn.modify(user['dn'], {'pwdLastSet': [(MODIFY_REPLACE, ['-1'])]})
                    conn.search(user['dn'], '(objectClass=person)', attributes=['pwdLastSet'])
                    pwd_last_set_value = conn.entries[0].pwdLastSet.value
                    pwd_last_set_dt = filetime_to_datetime(pwd_last_set_value)
                    future_date = pwd_last_set_dt + timedelta(days=90)
                    filetime = int((future_date - datetime(1601, 1, 1)).total_seconds() * 10**7)
                    account_expire_result = conn.modify(user['dn'], {'accountExpires': [(MODIFY_REPLACE, [str(filetime)])]})
                    if uac_result and pwd_last_set_result and account_expire_result:
                        messages.success(request, "✅ Password expiration enabled and account expiration set 90 days after last password set.")
                    else:
                        errors = [conn.result['message'] for result in [uac_result, pwd_last_set_result, account_expire_result] if not result]
                        messages.error(request, f"❌ Partial failure: {' | '.join(errors)}")
                except Exception as e:
                    messages.error(request, f"❌ Error enabling password expiry: {e}")
            else:
                messages.error(request, "❌ Invalid action.")
        except Exception as e:
            messages.error(request, f"❌ LDAP Error: {e}")
        conn.unbind()
        return redirect('ADManager:ad_user_detail', username=username)

    # Fetch groups
    try:
        conn.search(BASE_DN, '(objectClass=group)', SUBTREE, attributes=['cn', 'distinguishedName'])
    
        all_groups = sorted(
            [(entry.cn.value, entry.distinguishedName.value) for entry in conn.entries],
            key=lambda x: x[0].lower()
        )
    
    except Exception as e:
        messages.error(request, f"❌ Failed to fetch groups: {e}")
        all_groups = []

    conn.unbind()

    # Refresh user info
    user = fetch_ldap_user_by_username(username)

    # User Group Sort
    if user.get('groups'):
        user['groups'] = sorted(
            user['groups'],
            key=lambda x: x[0].lower()
        )
    
    password_expires = pwd_last_set + timedelta(days=90) if isinstance(pwd_last_set, datetime) else "Never"

    dn = user.get('dn', '')
    ou_parts = [part.replace("OU=", "") for part in dn.split(',') if part.startswith("OU=")]
    ou_path = " / ".join(reversed(ou_parts)) if ou_parts else "N/A"


    return render(request, 'ADManager/ad_user_detail.html', {
        'user': user,
        'all_groups': all_groups,
        'user_account_control': uac,
        'is_disabled': is_disabled,
        'is_locked': is_locked,
        'password_never_expires': password_never_expires,
        'account_expires': account_expires,
        'pwd_last_set': pwd_last_set,
        'password_expires': password_expires,
        'ou_path': ou_path,
    })



    return render(request, 'ADManager/ad_user_detail.html', {
        'user': user,
        'all_groups': all_groups,
    })

def get_sub_ous(parent_dn='OU=Users,DC=aurarcm,DC=org'):
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, authentication=SIMPLE, auto_bind=True)

    # Fetch OUs one level under Users OU
    search_filter = '(objectClass=organizationalUnit)'
    conn.search(parent_dn, search_filter, SUBTREE, attributes=['ou', 'distinguishedName'])

    ous = [(entry.ou.value, entry.distinguishedName.value) for entry in conn.entries]

    conn.unbind()
    return ous

from ldap3 import MODIFY_REPLACE
import base64
from ldap3 import Server, Connection, ALL, SIMPLE, SUBTREE, MODIFY_REPLACE
from django.contrib import messages
from django.shortcuts import render, redirect

from django.shortcuts import render

def create_ldap_user(request):
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, authentication=SIMPLE, auto_bind=True)

    # Load Organizational Units under BASE_DN
    conn.search(
        search_base=BASE_DN,
        search_filter='(objectClass=organizationalUnit)',
        search_scope=SUBTREE,
        attributes=['distinguishedName']
    )
    ous = []
    for entry in conn.entries:
        dn = entry.distinguishedName.value
        name = dn.split(',')[0].replace('OU=', '')
        ous.append((name, dn))


    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        selected_ou = request.POST.get('ou_dn')

        user_dn = f"CN={first_name} {last_name},{selected_ou}"

        attributes = {
            'objectClass': ['top', 'person', 'organizationalPerson', 'user'],
            'cn': f"{first_name} {last_name}",
            'sAMAccountName': username,
            'userPrincipalName': f"{username}@aurarcm.org",
            'givenName': first_name,
            'sn': last_name,
            'displayName': f"{first_name} {last_name}",
        }

        try:
            conn.add(dn=user_dn, attributes=attributes)
            if conn.result['description'] != 'success':
                raise Exception(conn.result['message'])

            conn.extend.microsoft.modify_password(user_dn, password)
            conn.modify(user_dn, {'userAccountControl': [(MODIFY_REPLACE, [512])]})

            messages.success(request, f"✅ User {first_name} {last_name} created successfully.")
        except Exception as e:
            messages.error(request, f"❌ Failed to create user: {e}")
        finally:
            conn.unbind()

        return redirect('ADManager:aduser')

    conn.unbind()
    return render(request, 'ADManager/ADUser_list.html', {'ous': ous})


def delete_ldap_user(request, username):
    user = fetch_ldap_user_by_username(username)
    if not user:
        messages.error(request, f"No such user found: {username}")
        return redirect('ADManager:aduser')

    user_dn = user['dn']
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, authentication=SIMPLE, auto_bind=True)

    try:
        result = conn.delete(user_dn)
        if result:
            messages.success(request, f"✅ User {username} deleted successfully.")
        else:
            messages.error(request, f"❌ Failed to delete user: {conn.result['message']}")
    except Exception as e:
        messages.error(request, f"❌ Exception during deletion: {e}")

    conn.unbind()
    return redirect('ADManager:aduser')

def export_ldap_users(request, filetype='csv'):
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(
        server,
        user=LDAP_USER,
        password=LDAP_PASSWORD,
        authentication=SIMPLE,
        auto_bind=True
    )

    search_filter = (
        '(&(objectClass=user)'
        '(!(objectClass=computer))'
        '(!(userAccountControl:1.2.840.113556.1.4.803:=2))'
        ')'
    )
    attributes = [
        'givenName', 'sn',
        'sAMAccountName', 'mail', 'title', 'department',
        'telephoneNumber', 'distinguishedName', 'memberOf',
        'userAccountControl', 'lockoutTime'
    ]

    conn.search(BASE_DN, search_filter, SUBTREE, attributes=attributes)

    header = [
        'First Name', 'Last Name', 'Username', 'Email', 'Designation',
        'Department', 'Phone', 'DN', 'Groups',
        'Account Enabled', 'Account Locked'
    ]

    rows = []

    for entry in conn.entries:
        groups = entry.memberOf.values if 'memberOf' in entry else []
        group_names = "; ".join(
            [dn.split(',')[0].replace('CN=', '') for dn in groups]
        )

        # Determine if account is locked
        lockout_time_raw = entry.lockoutTime.value if 'lockoutTime' in entry else 0
        try:
            lockout_time = int(lockout_time_raw)
        except Exception:
            lockout_time = 0
        account_locked = lockout_time not in (0, 9223372036854775807)

        # Determine if account is enabled
        try:
            uac = int(entry.userAccountControl.value)
            ACCOUNTDISABLE = 2
            account_enabled = (uac & ACCOUNTDISABLE) == 0
        except Exception:
            account_enabled = False

        first_name = entry.givenName.value or ''
        last_name = entry.sn.value or ''

        row = [
            first_name,
            last_name,
            entry.sAMAccountName.value or '',
            entry.mail.value or '',
            entry.title.value or '',
            entry.department.value or '',
            entry.telephoneNumber.value or '',
            entry.distinguishedName.value or '',
            group_names,
            "Yes" if account_enabled else "No",
            "Yes" if account_locked else "No",
        ]

        rows.append(row)

    conn.unbind()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=ldap_users.csv'

    writer = csv.writer(response)
    writer.writerow(header)
    writer.writerows(rows)

    return response




import winrm

def get_logged_in_user(hostname, username, password):
    try:
        session = winrm.Session(hostname, auth=(username, password))
        result = session.run_ps('Get-CimInstance -ClassName Win32_ComputerSystem | Select-Object -ExpandProperty UserName')
        if result.status_code == 0:
            return result.std_out.strip().decode()
        else:
            return f"Error: {result.std_err.strip().decode()}"
    except Exception as e:
        return f"Exception: {e}"


def adcomputers(request):
    computer_data = []

    try:
        server = Server(LDAP_SERVER, get_info=ALL)
        conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, auto_bind=True)

        conn.search(
            search_base=BASE_DN,
            search_filter='(objectClass=computer)',
            attributes=['cn', 'dNSHostName', 'operatingSystem', 'whenCreated']
        )

        for entry in conn.entries:
            computer_data.append({
                'name': str(entry.cn),
                'hostname': str(entry.dNSHostName) if 'dNSHostName' in entry else '',
                'os': str(entry.operatingSystem) if 'operatingSystem' in entry else '',
                'created': str(entry.whenCreated) if 'whenCreated' in entry else '',
            })

        # ✅ Sort by hostname (case-insensitive)
        computer_data.sort(key=lambda x: x['hostname'].lower() if x['hostname'] else '')

    except Exception as e:
        return render(request, 'ADManager/view_computers.html', {
            'error': f'Error fetching computers: {e}',
            'computers': []
        })
    

    return render(request, 'ADManager/ADComputers.html', {
        'computers': computer_data
    })


import pandas as pd
from django.http import HttpResponse
from ldap3 import Server, Connection, ALL

def export_computers_excel(request):
    computer_data = []

    try:
        server = Server(LDAP_SERVER, get_info=ALL)
        conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, auto_bind=True)

        conn.search(
            search_base=BASE_DN,
            search_filter='(objectClass=computer)',
            attributes=['cn', 'dNSHostName', 'operatingSystem', 'whenCreated']
        )

        for entry in conn.entries:
            computer_data.append({
                'Name': str(entry.cn),
                'Hostname': str(entry.dNSHostName) if 'dNSHostName' in entry else '',
                'Operating System': str(entry.operatingSystem) if 'operatingSystem' in entry else '',
                'Created': str(entry.whenCreated) if 'whenCreated' in entry else '',
            })

        # Sort by Hostname
        computer_data.sort(key=lambda x: x['Hostname'].lower() if x['Hostname'] else '')

        # Create a pandas DataFrame
        df = pd.DataFrame(computer_data)

        # Create an Excel file in memory
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="ad_computers.xlsx"'

        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Computers', index=False)

        return response

    except Exception as e:
        return HttpResponse(f'Error exporting computers: {e}', status=500)


# ===============================
# LDAP helper for other apps ( use this function to other apps to fetch all Security Group )
# ===============================

def get_user_ldap_group_dns(username):
    """
    Returns list of LDAP group DNs for a user.
    Used by PasswordVault for live access control.
    """
    user = fetch_ldap_user_by_username(username)
    if not user:
        return []

    # user["groups"] = [(group_name, group_dn), ...]
    return [dn for _, dn in user.get("groups", [])]


from django.conf import settings

def get_all_ldap_groups():
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, user=LDAP_USER, password=LDAP_PASSWORD, auto_bind=True)

    conn.search(
        BASE_DN,
        '(objectClass=group)',
        SUBTREE,
        attributes=['cn', 'distinguishedName']
    )

    excluded = set(
        name.lower()
        for name in getattr(settings, "PASSWORDVAULT_EXCLUDED_LDAP_GROUPS", [
        "users",
        "guests",

        ])
    )

    groups = []
    for entry in conn.entries:
        name = entry.cn.value
        dn = entry.distinguishedName.value

        if name.lower() in excluded:
            continue

        groups.append((name, dn))

    conn.unbind()
    return groups



def sync_security_groups(request):

    result = sync_ad_security_groups()

    messages.success(
        request,
        f"""
AD Synchronization Completed Successfully

Users Synced      : {result['users_synced']}
New Groups        : {result['groups_created']}
Relationships     : {result['relationships']}
Users Not Found   : {len(result['users_not_found'])}
"""
    )

    return redirect("ADManager:aduser")