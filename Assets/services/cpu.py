
from django.db import transaction
from django.utils import timezone

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


def valid_serial(value):
    serial = str(value or "").strip()
    return serial if serial.upper() not in INVALID_SERIALS else None


@transaction.atomic
def sync_desktop_info(data):

    hostname = str(data.get("hostname") or "").strip()
    serial_number = valid_serial(data.get("serial_number"))

    if not hostname:
        raise ValueError("Hostname is required.")

    asset_fields = [
        "asset_name",
        "manufacturer",
        "model",
        "serial_number",
    ]

    desktop_fields = [
        "hostname",
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

    # 1. Get Desktop category
    category = AssetCategory.objects.filter(
        name__iexact="Desktop",
        category_type="IT",
        is_active=True
    ).first()

    if not category:
        category = AssetCategory.objects.create(
            name="Desktop",
            category_type="IT",
            is_active=True
        )

    desktop = None
    sync_action = "CREATED"

    # 2. Find by hostname
    hostname_matches = list(
        DesktopAsset.objects.select_for_update()
        .select_related("asset")
        .filter(hostname__iexact=hostname)
    )

    if len(hostname_matches) > 1:
        raise ValueError(
            f"Multiple desktop records found for hostname: {hostname}"
        )

    if hostname_matches:
        candidate = hostname_matches[0]

        existing_serial = valid_serial(
            candidate.asset.serial_number
        )

        # Same hostname but different valid hardware serial:
        # do not merge the two physical computers.
        if (
            serial_number
            and existing_serial
            and serial_number.upper() != existing_serial.upper()
        ):
            desktop = None
        else:
            desktop = candidate
            sync_action = "UPDATED"

    # 3. If hostname did not match, try a valid serial number.
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
            # Ambiguous serial: do not merge existing computers.
            desktop = None

    # 4. Create a new Asset if no safe match exists.
    if desktop is None:

        asset = Asset.objects.create(
            asset_name=data.get("asset_name") or hostname,
            category=category,
            status="IN_STOCK"
        )

        desktop = DesktopAsset.objects.create(
            asset=asset,
            hostname=hostname
        )

        sync_action = "CREATED"

    else:
        asset = desktop.asset

    # 5. Update common asset information.
    for field in asset_fields:

        value = data.get(field)

        if value is None or not str(value).strip():
            continue

        if field == "serial_number":
            value = serial_number

            if not value:
                continue

        setattr(asset, field, value)

    asset.save()

    # 6. Update desktop hardware information.
    for field in desktop_fields:

        value = data.get(field)

        if value is None or not str(value).strip():
            continue

        if field == "hostname":
            value = hostname

        setattr(desktop, field, value)

    desktop.last_sync = timezone.now()
    desktop.save()

    # 7. Return synchronization details.
    return {
        "success": True,
        "message": "Desktop information synchronized successfully.",
        "sync_action": sync_action,
        "asset_id": asset.id,
        "desktop_id": desktop.id,
        "asset_created": sync_action == "CREATED",
        "desktop_created": sync_action == "CREATED",
        "hostname": hostname,
        "serial_number": serial_number,
        "last_sync": desktop.last_sync.isoformat(),
    }
