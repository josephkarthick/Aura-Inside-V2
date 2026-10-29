
from django.db import models
from Accounts.models import Department, Designation, AuraInsideUser



class InternalJobPosting(models.Model):
    title = models.CharField(
        max_length=200,
        help_text="Job title (e.g. Senior IT Executive)",
    )

    departments = models.ManyToManyField(
        Department,
        blank=True,
        db_table="internal_job_posting_departments",
    )

    designations = models.ManyToManyField(
        Designation,
        blank=True,
        db_table="internal_job_posting_designations",
    )

    vacancies = models.PositiveIntegerField(default=1)

    minimum_experience_months = models.PositiveIntegerField(
        help_text="Minimum experience in Aura Inside (Months)",
    )

    minimum_appraisal_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="Minimum appraisal rating (Out of 5)",
    )

    appraisal_year = models.PositiveIntegerField(
        help_text="Applicable appraisal year",
    )

    minimum_attendance_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="Minimum attendance rating (Out of 5)",
    )

    attendance_year = models.PositiveIntegerField(
        help_text="Applicable attendance year",
    )

    description = models.TextField(blank=True, null=True)

    application_start_date = models.DateField()
    application_end_date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=[
            ("Open", "Open"),
            ("Closed", "Closed"),
        ],
        default="Open",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "internal_job_posting"
        verbose_name = "Internal Job Posting"
        verbose_name_plural = "Internal Job Postings"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title



class IJPApplication(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    employee = models.ForeignKey(
        AuraInsideUser,
        on_delete=models.CASCADE,
        related_name="ijp_applications",
    )

    ijp = models.ForeignKey(
        InternalJobPosting,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    decision_remarks = models.TextField(
        blank=True,
        default="",
    )

    decided_by = models.ForeignKey(
        AuraInsideUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ijp_decisions_made",
    )

    decided_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "ijp_application"
        unique_together = ("employee", "ijp")
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.employee} - {self.ijp.title}"
