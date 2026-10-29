
import wmi
import socket
import subprocess
import json
import getpass
import requests
import re


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://192.168.5.249/itdesk/api/receive-asset/"


# ============================================================
# WINDOWS PRODUCT KEY
# ============================================================

def get_windows_key_last_5():
    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "(Get-CimInstance -ClassName SoftwareLicensingService).OA3xOriginalProductKey"
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        key = result.stdout.strip()

        if key and len(key) >= 5:
            return key[-5:]

        return "N/A"

    except Exception as e:
        return f"Error: {e}"


# ============================================================
# WINDOWS LICENSE STATUS
# ============================================================

def get_windows_license_status():
    try:
        result = subprocess.run(
            ["powershell", "-Command",
             "(Get-CimInstance -ClassName SoftwareLicensingProduct | Where-Object { $_.PartialProductKey }).LicenseStatus"],
            capture_output=True,
            text=True
        )

        code = result.stdout.strip()
        if code == "1":
            return "Activated"
        elif code == "0":
            return "Unlicensed"
        elif code == "2":
            return "Out of Tolerance"
        elif code == "3":
            return "Tampered"
        elif code == "4":
            return "Notification"
        elif code == "5":
            return "Extended Grace"
        else:
            return f"Unknown ({code})"
    except Exception as e:
        return f"Error: {e}"


# ============================================================
# BYTE ARRAY DECODER
# ============================================================

def decode_byte_array(byte_array):
    try:
        return ''.join(
            chr(b)
            for b in byte_array
            if b > 0
        ).strip()
    except Exception:
        return ""


# ============================================================
# MONITOR INFORMATION
# ============================================================

def get_monitor_info():

    monitors = []

    # --------------------------------------------------------
    # METHOD 1:
    # WMI root\wmi - WmiMonitorID
    # --------------------------------------------------------

    try:

        w = wmi.WMI(namespace="root\\wmi")

        monitor_ids = w.WmiMonitorID()

        for monitor in monitor_ids:

            manufacturer = decode_byte_array(
                monitor.ManufacturerName
            )

            model = decode_byte_array(
                monitor.UserFriendlyName
            )

            serial_number = decode_byte_array(
                monitor.SerialNumberID
            )

            monitors.append({
                "monitor_number": len(monitors) + 1,
                "manufacturer": manufacturer or "Unknown",
                "model": model or "Unknown",
                "serial_number": serial_number or "Unknown",
                "resolution": "Unknown",
                "refresh_rate": None
            })

    except Exception as e:

        print(
            "Monitor identification WMI error:",
            e
        )

    # --------------------------------------------------------
    # METHOD 2:
    # Get display resolutions
    # --------------------------------------------------------

    resolutions = []

    try:

        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                """
                Get-CimInstance Win32_VideoController |
                Where-Object {
                    $_.CurrentHorizontalResolution -and
                    $_.CurrentVerticalResolution
                } |
                ForEach-Object {
                    "$($_.CurrentHorizontalResolution)x$($_.CurrentVerticalResolution)"
                }
                """
            ],
            capture_output=True,
            text=True,
            timeout=10
        )

        for line in result.stdout.splitlines():

            line = line.strip()

            if re.match(
                r"^\d+x\d+$",
                line
            ):
                resolutions.append(line)

    except Exception as e:

        print(
            "Resolution detection error:",
            e
        )

    # Remove duplicate resolutions
    resolutions = list(
        dict.fromkeys(resolutions)
    )

    # --------------------------------------------------------
    # METHOD 3:
    # PowerShell Get-CimInstance Win32_DesktopMonitor
    #
    # This may provide additional monitor information on
    # systems where WmiMonitorID is unavailable.
    # --------------------------------------------------------

    if not monitors:

        try:

            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    """
                    Get-CimInstance Win32_DesktopMonitor |
                    Select-Object Name, MonitorType, PNPDeviceID |
                    ConvertTo-Json -Compress
                    """
                ],
                capture_output=True,
                text=True,
                timeout=10
            )

            output = result.stdout.strip()

            if output:

                desktop_monitors = json.loads(output)

                if isinstance(
                    desktop_monitors,
                    dict
                ):
                    desktop_monitors = [
                        desktop_monitors
                    ]

                for item in desktop_monitors:

                    name = (
                        item.get("Name")
                        or "Unknown"
                    )

                    pnp_id = (
                        item.get("PNPDeviceID")
                        or "Unknown"
                    )

                    monitors.append({
                        "monitor_number": len(monitors) + 1,
                        "manufacturer": "Unknown",
                        "model": name,
                        "serial_number": pnp_id,
                        "resolution": "Unknown",
                        "refresh_rate": None
                    })

        except Exception as e:

            print(
                "Desktop monitor detection error:",
                e
            )

    # --------------------------------------------------------
    # FALLBACK:
    # If no monitor identification was possible,
    # create records from detected resolutions.
    # --------------------------------------------------------

    if not monitors and resolutions:

        for resolution in resolutions:

            monitors.append({
                "monitor_number": len(monitors) + 1,
                "manufacturer": "Unknown",
                "model": "Unknown",
                "serial_number": "Unknown",
                "resolution": resolution,
                "refresh_rate": None
            })

    # --------------------------------------------------------
    # ADD RESOLUTION TO IDENTIFIED MONITORS
    # --------------------------------------------------------

    for index, monitor in enumerate(
        monitors
    ):

        if (
            monitor.get("resolution") == "Unknown"
            and index < len(resolutions)
        ):
            monitor["resolution"] = (
                resolutions[index]
            )

    return monitors


# ============================================================
# DISK INFORMATION
# ============================================================

def get_disk_info():

    total_bytes = 0
    free_bytes = 0

    try:

        w = wmi.WMI()

        disks = w.Win32_LogicalDisk(
            DriveType=3
        )

        for disk in disks:

            if disk.Size:
                total_bytes += int(
                    disk.Size
                )

            if disk.FreeSpace:
                free_bytes += int(
                    disk.FreeSpace
                )

        return {
            "hdd_gb": round(
                total_bytes / (1024 ** 3)
            ),

            "free_disk_gb": round(
                free_bytes / (1024 ** 3)
            )
        }

    except Exception as e:

        print(
            "Disk information error:",
            e
        )

        return {
            "hdd_gb": None,
            "free_disk_gb": None
        }


# ============================================================
# NETWORK INFORMATION
# ============================================================

def get_network_info():

    ip_address = None
    mac_address = None

    # --------------------------------------------------------
    # IP ADDRESS
    # --------------------------------------------------------

    try:

        hostname = socket.gethostname()

        ip_address = socket.gethostbyname(
            hostname
        )

    except Exception:
        pass

    # --------------------------------------------------------
    # MAC ADDRESS
    # --------------------------------------------------------

    try:

        w = wmi.WMI()

        adapters = w.Win32_NetworkAdapterConfiguration(
            IPEnabled=True
        )

        for adapter in adapters:

            if adapter.MACAddress:

                mac_address = (
                    adapter.MACAddress
                )

                break

    except Exception as e:

        print(
            "MAC address detection error:",
            e
        )

    return {
        "ip_address": ip_address,
        "mac_address": mac_address
    }


# ============================================================
# SYSTEM INFORMATION
# ============================================================

def collect_system_info():

    try:

        w = wmi.WMI()

        # ----------------------------------------------------
        # BASIC SYSTEM
        # ----------------------------------------------------

        system_info = (
            w.Win32_ComputerSystem()[0]
        )

        bios_info = (
            w.Win32_BIOS()[0]
        )

        processor_info = (
            w.Win32_Processor()[0]
        )

        os_info = (
            w.Win32_OperatingSystem()[0]
        )

        # ----------------------------------------------------
        # DISK
        # ----------------------------------------------------

        disk_info = get_disk_info()

        # ----------------------------------------------------
        # NETWORK
        # ----------------------------------------------------

        network_info = get_network_info()

        # ----------------------------------------------------
        # MONITORS
        # ----------------------------------------------------

        monitors = get_monitor_info()

        # ----------------------------------------------------
        # MANUFACTURER
        # ----------------------------------------------------

        manufacturer = (
            system_info.Manufacturer
            if system_info.Manufacturer
            else None
        )

        # ----------------------------------------------------
        # MODEL
        # ----------------------------------------------------

        model = (
            system_info.Model
            if system_info.Model
            else None
        )

        # ----------------------------------------------------
        # BIOS VERSION
        # ----------------------------------------------------

        bios_version = None

        try:

            bios_version = (
                bios_info.SMBIOSBIOSVersion
                or bios_info.Version
            )

        except Exception:
            pass

        # ----------------------------------------------------
        # DOMAIN
        # ----------------------------------------------------

        domain_name = None

        try:

            domain_name = system_info.Domain

        except Exception:
            pass

        # ----------------------------------------------------
        # SYSTEM TYPE
        # ----------------------------------------------------

        system_type = None

        try:

            system_type = system_info.SystemType

        except Exception:
            pass

        # ----------------------------------------------------
        # FINAL DATA
        # ----------------------------------------------------

        data = {

            "hostname":
                socket.gethostname(),

            "processor":
                processor_info.Name,

            "ram_gb":
                round(
                    int(
                        system_info.TotalPhysicalMemory
                    ) / (1024 ** 3)
                ),

            "hdd_gb":
                disk_info["hdd_gb"],

            "free_disk_gb":
                disk_info["free_disk_gb"],

            "serial_number":
                (
                    bios_info.SerialNumber.strip()
                    if bios_info.SerialNumber
                    else None
                ),

            "os_installed":
                os_info.Caption,

            "windows_key_last5":
                get_windows_key_last_5(),

            "windows_license_status":
                get_windows_license_status(),

            "license_type":
                None,

            "logged_in_user":
                getpass.getuser(),

            "ip_address":
                network_info["ip_address"],

            "mac_address":
                network_info["mac_address"],

            "manufacturer":
                manufacturer,

            "model":
                model,

            "bios_version":
                bios_version,

            "system_type":
                system_type,

            "domain_name":
                domain_name,

            # =================================================
            # IMPORTANT:
            # Dedicated Monitor table uses this list
            # =================================================

            "monitors":
                monitors
        }

        return data

    except Exception as e:

        return {
            "error": str(e)
        }


# ============================================================
# SEND DATA TO AURAINSIDE
# ============================================================

def send_to_server(info):

    try:

        response = requests.post(
            API_URL,
            json=info,
            timeout=(5, 15)
        )

        return response

    except requests.exceptions.Timeout:

        print(
            "❌ Aurainside server request timed out"
        )

    except requests.exceptions.ConnectionError:

        print(
            "❌ Cannot connect to Aurainside server"
        )

    except Exception as e:

        print(
            "❌ Failed to send:",
            e
        )

    return None


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("▶ Script started")

    info = collect_system_info()

    print(
        json.dumps(
            info,
            indent=4
        )
    )

    if "error" in info:

        print(
            "❌ System information collection failed"
        )

    else:

        response = send_to_server(info)

        if response is not None:

            print(
                "✅ Sent to server:",
                response.status_code,
                response.text
            )

