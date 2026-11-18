
import hashlib

from django.db.models import Count

from ITDesk.models import VoipRecord
from Employee.models import Calendar_Event
from Assets.models import DesktopAsset
from Assets.models import DesktopAsset, Monitor

def vendor_color(name):
    """Generate a stable, readable color for any vendor name."""
    name = str(name or "Unknown")
    h = int(hashlib.md5(name.encode()).hexdigest()[:6], 16)

    r = max((h >> 16) & 255, 80)
    g = max((h >> 8) & 255, 80)
    b = max(h & 255, 80)

    return f"rgb({r},{g},{b})"


def is_windows_activated(status):
    """
    Identify activated Windows license statuses.
    Adjust this function if your database uses different status values.
    """
    status = str(status or "").strip().lower()

    if not status:
        return False

    negative_terms = (
        "not activated",
        "not licensed",
        "unlicensed",
        "unactivated",
        "inactive",
        "expired",
        "grace",
    )

    if any(term in status for term in negative_terms):
        return False

    return (
        "activated" in status
        or status == "licensed"
        or status == "genuine"
    )

from django.db.models import Count, Q
import re
from collections import Counter


import re

def normalize_processor_name(processor):
    processor = str(processor or "").strip()

    if not processor:
        return "Unknown Processor"

    value = processor.lower()

    # Intel Core Ultra (3, 5, 7, 9)
    match = re.search(r'core.*?ultra\s*([3579])', value)
    if match:
        return f"Intel Core Ultra {match.group(1)}"

    # Intel Core i3, i5, i7, i9
    match = re.search(r'\bi([3579])\b', value)
    if match:
        return f"Intel Core i{match.group(1)}"

    # Intel Xeon
    if "xeon" in value:
        return "Intel Xeon"

    # Intel Pentium
    if "pentium" in value:
        return "Intel Pentium"

    # Intel Celeron
    if "celeron" in value:
        return "Intel Celeron"

    # AMD Ryzen (3, 5, 7, 9)
    match = re.search(r'ryzen\s*([3579])', value)
    if match:
        return f"AMD Ryzen {match.group(1)}"

    # AMD Athlon
    if "athlon" in value:
        return "AMD Athlon"

    # AMD EPYC
    if "epyc" in value:
        return "AMD EPYC"

    # Preserve original processor name if not recognized
    return processor

def get_it_dashboard_data():

    # --------------------------------
    # VOIP STATISTICS
    # --------------------------------
    
    vendor_counts = list(
        VoipRecord.objects
        .values("vendor__name")
        .annotate(
            total=Count("id"),
            used=Count("id", filter=Q(is_free=False)),
            free=Count("id", filter=Q(is_free=True)),
        )
        .order_by("-total")
    )
    
    for vendor in vendor_counts:
        vendor["color"] = vendor_color(vendor["vendor__name"])
    
    # Overall statistics
    overall_count = VoipRecord.objects.count()
    
    overall_used = VoipRecord.objects.filter(
        is_free=False
    ).count()
    
    overall_free = VoipRecord.objects.filter(
        is_free=True
    ).count()

    # --------------------------------
    # COMPUTER STATISTICS
    # --------------------------------

    computers = DesktopAsset.objects.all()

    total_computers = computers.count()

    desktop_count = computers.filter(
        asset_type__iexact="DESKTOP"
    ).count()

    laptop_count = computers.filter(
        asset_type__iexact="LAPTOP"
    ).count()

    server_count = computers.filter(
        asset_type__iexact="SERVER"
    ).count()

    # --------------------------------
    # PROCESSOR-WISE STATISTICS
    # --------------------------------

    processor_counter = Counter()

    processor_list = computers.values_list(
        'processor',
        flat=True
    )

    for processor in processor_list:
        processor_name = normalize_processor_name(processor)
        processor_counter[processor_name] += 1

    processor_distribution = [
        {
            "name": name,
            "total": total,
        }
        for name, total in processor_counter.most_common()
    ]

    processor_chart_labels = [
        item["name"] for item in processor_distribution
    ]

    processor_chart_values = [
        item["total"] for item in processor_distribution
    ]

    processor_total = sum(processor_chart_values)

    # --------------------------------
    # Monitor Count
    # --------------------------------   
    
    monitor_count = Monitor.objects.filter(
        monitor_type="EXTERNAL"
    ).count()

    # --------------------------------
    # WINDOWS ACTIVATION STATISTICS
    # --------------------------------    
    
    license_statuses = (
        computers
        .values("windows_license_status")
        .annotate(total=Count("id"))
    )

    activated_count = 0

    for item in license_statuses:
        if is_windows_activated(item["windows_license_status"]):
            activated_count += item["total"]

    not_activated_count = total_computers - activated_count

    # --------------------------------
    # IT REMINDERS
    # --------------------------------

    it_reminders = (
        Calendar_Event.objects
        .filter(
            type="reminder",
            cancelled=False,
            owner__department__name__in=["IT", "Admin"]
        )
        .distinct()
        .order_by("start")
    )


    # Windows activation statistics by device type

    license_statuses = (
        computers
        .values("asset_type", "windows_license_status")
        .annotate(total=Count("id"))
    )

    activation_stats = {
        "DESKTOP": {"activated": 0, "not_activated": 0},
        "LAPTOP": {"activated": 0, "not_activated": 0},
        "SERVER": {"activated": 0, "not_activated": 0},
    }

    for item in license_statuses:
        device_type = str(item["asset_type"] or "").upper()

        if device_type not in activation_stats:
            continue

        if is_windows_activated(item["windows_license_status"]):
            activation_stats[device_type]["activated"] += item["total"]
        else:
            activation_stats[device_type]["not_activated"] += item["total"]

    desktop_activated = activation_stats["DESKTOP"]["activated"]
    desktop_not_activated = activation_stats["DESKTOP"]["not_activated"]

    laptop_activated = activation_stats["LAPTOP"]["activated"]
    laptop_not_activated = activation_stats["LAPTOP"]["not_activated"]

    server_activated = activation_stats["SERVER"]["activated"]
    server_not_activated = activation_stats["SERVER"]["not_activated"]

    total_activated = sum(
        item["activated"] for item in activation_stats.values()
    )

    total_not_activated = sum(
        item["not_activated"] for item in activation_stats.values()
    )


    # --------------------------------
    # DASHBOARD CONTEXT
    # --------------------------------

    return {
        "vendor_counts": vendor_counts,
        "overall_count": overall_count,
        "overall_used": overall_used,
        "overall_free": overall_free,

        "total_computers": total_computers,
        "desktop_count": desktop_count,
        "laptop_count": laptop_count,
        "server_count": server_count,

        "activated_count": activated_count,
        "not_activated_count": not_activated_count,
        
        "monitor_count": monitor_count,

        "it_reminders": it_reminders,

        "desktop_activated": desktop_activated,
        "desktop_not_activated": desktop_not_activated,
        
        "laptop_activated": laptop_activated,
        "laptop_not_activated": laptop_not_activated,
        
        "server_activated": server_activated,
        "server_not_activated": server_not_activated,
        
        "total_activated": total_activated,
        "total_not_activated": total_not_activated, 

        "processor_distribution": processor_distribution,
        "processor_chart_labels": processor_chart_labels,
        "processor_chart_values": processor_chart_values,
        "processor_total": processor_total,        
    }
