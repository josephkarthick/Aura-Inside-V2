from datetime import timedelta
from django.utils import timezone

def get_month_ranges():
    now = timezone.now()

    # Current month
    start_current_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_current_month = now

    # Last month
    end_last_month = start_current_month - timedelta(seconds=1)
    start_last_month = end_last_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    return {
        'start_current_month': start_current_month,
        'end_current_month': end_current_month,
        'start_last_month': start_last_month,
        'end_last_month': end_last_month,
    }
