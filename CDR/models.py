from django.db import models
from datetime import timedelta
from django.db import models
from Accounts.models import AuraInsideUser
from ITDesk.models import VoipRecord

class Vendor(models.Model):
    name = models.CharField(max_length=50)
    api_token = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
        
class CallLog(models.Model):

    # Vendor
    vendor = models.CharField(
        max_length=30
    )

    # Employee Details (Snapshot)
    employee_id = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    employee_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    # Call Details
    source = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    destination = models.CharField(
        max_length=50,
        blank=True,
        null=True,        
    )

    # Date & Time
    call_date = models.DateField(
        blank=True,
        null=True,
    )

    est_time = models.TimeField(
        blank=True,
        null=True,
    )

    ist_time = models.TimeField(
        blank=True,
        null=True,
    )

    hour = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )

    # Duration
    duration = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    duration_seconds = models.IntegerField(
        default=0
    )

    # Call Status
    call_status = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    # Less Than 1 Min / 1-3 Mins / Greater Than 3 Mins / Hold
    call_category = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "-call_date",
            "-ist_time",
        ]

        indexes = [

            models.Index(fields=["employee_id"]),

            models.Index(fields=["vendor"]),

            models.Index(fields=["call_date"]),

            models.Index(fields=["hour"]),

            models.Index(fields=["call_category"]),

        ]

    def __str__(self):

        return f"{self.employee_name} ({self.employee_id})"       