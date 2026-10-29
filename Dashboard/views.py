from django.shortcuts import render
from django.db.models import Count
from ITDesk.models import VoipRecord
import hashlib
from Employee.models import Calendar_Event


def vendor_color(name):
    """Generate stable, readable color for any vendor name"""
    h = int(hashlib.md5(name.encode()).hexdigest()[:6], 16)
    r = max((h >> 16) & 255, 80)
    g = max((h >> 8) & 255, 80)
    b = max(h & 255, 80)
    return f"rgb({r},{g},{b})"


def IT_Dashboard(request):
    vendor_counts = (
        VoipRecord.objects
        .values('vendor__name')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # attach color dynamically
    for v in vendor_counts:
        v['color'] = vendor_color(v['vendor__name'])

    overall_count = VoipRecord.objects.count()
    
    it_reminders = (
        Calendar_Event.objects
        .filter(
            type='reminder',
            cancelled=False,
            owner__department__name__in=['IT', 'Admin']
        )
        .distinct()
        .order_by('start')
    )

        

    context = {
        'vendor_counts': vendor_counts,
        'overall_count': overall_count,
        "it_reminders": it_reminders,        
    }
    return render(request, 'IT_Dashboard/index.html', context)
