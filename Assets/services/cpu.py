
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from ..models import ComputerUserHistory
from ..models import Asset, AssetCategory, DesktopAsset


INVALID_SERIALS = {
    "",
    "NONE",
    "NULL",
    "UNKNOWN",
    "DEFAULT STRING",
    "SYSTEM SERIAL NUMBER",
    "TO BE FILLED BY O.E.M.",
    "TO BE FILLED BY OEM",
    "NOT SPECIFIED",
    "NOT AVAILABLE",
    "00000000",
    "123456789",
}

DEVICE_TYPES = {
    "DESKTOP",
    "LAPTOP",
    "SERVER",
    "MAC_DESKTOP",
    "MACBOOK",
    "WORKSTATION",
    "MINI_PC",
    "UNKNOWN",
}

CATEGORY_NAMES = {
    "DESKTOP": "Desktop",
    "LAPTOP": "Laptop",
    "SERVER": "Server",
    "MAC_DESKTOP": "Mac Desktop",
    "MACBOOK": "MacBook",
    "WORKSTATION": "Workstation",
    "MINI_PC": "Mini PC",
    "UNKNOWN": "Other IT",
}


def valid_serial(value):
    serial = str(value or "").strip()
    return serial if serial.upper() not in INVALID_SERIALS else None


@transaction.atomic
def sync_desktop_info(data):

    hostname = str(data.get("hostname") or "").strip()

    if not hostname:
        raise ValueError("Hostname is required.")

    serial_number = valid_serial(data.get("serial_number"))

    # ---------------------------------------------------------
    # DEVICE TYPE
    # ---------------------------------------------------------

    asset_type = str(
        data.get("asset_type") or "UNKNOWN"
    ).strip().upper()

    if asset_type not in DEVICE_TYPES:
        asset_type = "UNKNOWN"

    category_name = CATEGORY_NAMES[asset_type]

    category = AssetCategory.objects.filter(
        name__iexact=category_name,
        category_type="IT",
        is_active=True
    ).first()

    if not category:
        category = AssetCategory.objects.create(
            name=category_name,
            category_type="IT",
            is_active=True
        )

    # ---------------------------------------------------------
    # COMMON ASSET FIELDS
    # ---------------------------------------------------------

    asset_fields = [
        "asset_name",
        "manufacturer",
        "model",
        "serial_number",
    ]

    # ---------------------------------------------------------
    # COMPUTER HARDWARE FIELDS
    # ---------------------------------------------------------

    desktop_fields = [
        "hostname",
        "asset_type",
        "processor",
        "processor_cores",
        "processor_threads",
        "processor_speed_mhz",
        "ram_gb",
        "hdd_gb",
        "free_disk_gb",
        "bios_version",
        "bios_serial_number",
        "motherboard",
        "graphics_card",
        "os_installed",
        "os_version",
        "os_build",
        "windows_key_last5",
        "windows_license_status",
        "license_type",
        "logged_in_user",
        "ip_address",
        "mac_address",
        "system_type",
        "domain_name",
    ]

    desktop = None
    sync_action = "CREATED"

    # ---------------------------------------------------------
    # 1. FIND BY HOSTNAME
    # ---------------------------------------------------------

    hostname_matches = list(
        DesktopAsset.objects.select_for_update()
        .select_related("asset")
        .filter(hostname__iexact=hostname)
    )

    if len(hostname_matches) > 1:
        raise ValueError(
            f"Multiple computer records found for hostname: {hostname}"
        )

    if hostname_matches:

        candidate = hostname_matches[0]

        existing_serial = valid_serial(
            candidate.asset.serial_number
        )

        # Same hostname but different valid serial:
        # treat it as a different physical computer.
        if (
            serial_number
            and existing_serial
            and serial_number.upper() != existing_serial.upper()
        ):
            desktop = None

        else:
            desktop = candidate
            sync_action = "UPDATED"

    # ---------------------------------------------------------
    # 2. FIND BY SERIAL NUMBER
    # ---------------------------------------------------------

    if desktop is None and serial_number:

        serial_matches = list(
            DesktopAsset.objects.select_for_update()
            .select_related("asset")
            .filter(asset__serial_number__iexact=serial_number)
        )

        if len(serial_matches) == 1:
            desktop = serial_matches[0]
            sync_action = "UPDATED"

        elif len(serial_matches) > 1:
            raise ValueError(
                f"Multiple computer records found for serial: {serial_number}"
            )

    # ---------------------------------------------------------
    # 3. CREATE NEW ASSET IF NOT FOUND
    # ---------------------------------------------------------

    if desktop is None:

        asset = Asset.objects.create(
            asset_name=data.get("asset_name") or hostname,
            category=category,
            status="IN_STOCK"
        )

        desktop = DesktopAsset.objects.create(
            asset=asset,
            hostname=hostname,
            asset_type=asset_type
        )

        sync_action = "CREATED"

    else:
        asset = desktop.asset

    # ---------------------------------------------------------
    # 4. UPDATE COMMON ASSET INFORMATION
    # ---------------------------------------------------------

    for field in asset_fields:

        value = data.get(field)

        if value is None or not str(value).strip():
            continue

        if field == "serial_number":
            value = serial_number

            if not value:
                continue

        setattr(asset, field, value)

    # Update category whenever device type changes.
    asset.category = category

    asset.save()

    # ---------------------------------------------------------
    # 5. UPDATE COMPUTER HARDWARE INFORMATION
    # ---------------------------------------------------------

    for field in desktop_fields:

        if field == "asset_type":
            value = asset_type

        elif field == "hostname":
            value = hostname

        else:
            value = data.get(field)

        if value is None or not str(value).strip():
            continue

        setattr(desktop, field, value)

    desktop.last_sync = timezone.now()
    desktop.save()

    # Synchronize detected Windows user history
    sync_computer_user_history(
        desktop,
        desktop.logged_in_user
    )
    
    # ---------------------------------------------------------
    # 6. RESPONSE
    # ---------------------------------------------------------

    return {
        "success": True,
        "message": "Computer information synchronized successfully.",
        "sync_action": sync_action,
        "asset_id": asset.id,
        "desktop_id": desktop.id,
        "asset_created": sync_action == "CREATED",
        "desktop_created": sync_action == "CREATED",
        "hostname": hostname,
        "asset_type": desktop.asset_type,
        "category": category.name,
        "serial_number": serial_number,
        "last_sync": desktop.last_sync.isoformat(),
    }


def sync_computer_user_history(desktop, logged_in_user):
    """
    Track the Windows user currently detected on a computer.
    Shift is copied from the matched AuraInside employee.
    """

    username = str(logged_in_user or "").strip()

    if not username:
        return

    # Handle DOMAIN\username format
    if "\\" in username:
        username = username.rsplit("\\", 1)[-1]

    # Handle username@domain format
    if "@" in username:
        username = username.split("@", 1)[0]

    if not username:
        return

    User = get_user_model()

    employee = User.objects.filter(
        username__iexact=username
    ).select_related("shift").first()

    shift_name = (
        employee.shift.name
        if employee and employee.shift
        else None
    )

    # Lock existing current history records for this computer.
    current_records = list(
        ComputerUserHistory.objects.select_for_update().filter(
            computer=desktop,
            is_current=True
        )
    )

    matching_record = next(
        (
            record for record in current_records
            if record.windows_username.casefold() == username.casefold()
        ),
        None
    )

    # Same user: update last seen.
    if matching_record:

        for record in current_records:
            if record.pk != matching_record.pk:
                record.is_current = False
                record.save(update_fields=["is_current"])

        matching_record.last_seen = timezone.now()
        matching_record.employee = employee

        # Keep the shift snapshot from when this usage record started.
        matching_record.save(
            update_fields=["last_seen", "employee"]
        )

        return

    # Different user: close previous detected user records.
    now = timezone.now()

    ComputerUserHistory.objects.filter(
        computer=desktop,
        is_current=True
    ).update(
        is_current=False,
        last_seen=now
    )

    # Create history for the newly detected user.
    ComputerUserHistory.objects.create(
        computer=desktop,
        windows_username=username,
        employee=employee,
        shift=shift_name,
        first_seen=now,
        last_seen=now,
        is_current=True
    )
