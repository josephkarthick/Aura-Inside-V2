import os
from django.contrib.auth.models import AbstractUser
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Designation(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title
    
class Shift(models.Model):

    name = models.CharField(
        max_length=50,
        unique=True
    )

    start_time = models.TimeField(
        null=True,
        blank=True
    )

    end_time = models.TimeField(
        null=True,
        blank=True
    )

    timezone = models.CharField(
        max_length=50,
        default="Asia/Kolkata"
    )

    def __str__(self):
        start = (
            self.start_time.strftime("%H:%M")
            if self.start_time
            else "--:--"
        )

        end = (
            self.end_time.strftime("%H:%M")
            if self.end_time
            else "--:--"
        )

        return f"{self.name} ({start} - {end})"
        
# Accounts/models.py

class SecurityGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    project = models.CharField(max_length=255, blank=True, null=True)
    process = models.CharField(max_length=255, blank=True, null=True)
    distinguished_name = models.CharField(max_length=512, unique=True)

    class Meta:
        ordering = ["project", "process", "name"]

    def __str__(self):
        return self.name
        
def employee_photo_path(instance, filename):
    """
    Save employee photo as:
    media/employee_photos/<username>.<extension>

    Example:
    employee_photos/joseph.jpg
    employee_photos/arun.png
    """
    ext = os.path.splitext(filename)[1].lower()
    return f"employee_photos/{instance.username}{ext}"        

class AuraInsideUser(AbstractUser):
    employee_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    # ForeignKey relationships
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.ForeignKey('Designation', on_delete=models.SET_NULL, null=True, blank=True)
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)
    security_groups = models.ManyToManyField(SecurityGroup,blank=True,related_name="users")
    # Additional personal info
    gender = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female")], default="male")
    birthdate = models.DateField(null=True, blank=True)
    
    profile_photo = models.ImageField(
        upload_to=employee_photo_path,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        # Delete old image when uploading a new one
        if self.pk:
            try:
                old = AuraInsideUser.objects.get(pk=self.pk)

                if (
                    old.profile_photo and
                    old.profile_photo != self.profile_photo
                ):
                    old.profile_photo.delete(save=False)

            except AuraInsideUser.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id} - {self.get_full_name()}"    


    def __str__(self):
        return self.username


class EmployeeAppraisal(models.Model):
    employee = models.ForeignKey(
        AuraInsideUser,
        on_delete=models.CASCADE,
        related_name="appraisals"
    )

    year = models.PositiveIntegerField()

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="Overall appraisal rating (e.g. 4.5 out of 5)"
    )

    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "employee_appraisal"
        verbose_name = "Employee Appraisal"
        verbose_name_plural = "Employee Appraisals"
        unique_together = ("employee", "year")
        ordering = ["-year", "employee__employee_id"]

    def __str__(self):
        return f"{self.employee.employee_id} - {self.year} ({self.rating})"

class EmployeeAttendance(models.Model):
    employee = models.ForeignKey(
        AuraInsideUser,
        on_delete=models.CASCADE,
        related_name="attendance_ratings"
    )

    year = models.PositiveIntegerField()

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        help_text="Attendance rating (e.g. 4.8 out of 5)"
    )

    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "employee_attendance"
        verbose_name = "Employee Attendance"
        verbose_name_plural = "Employee Attendance"
        unique_together = ("employee", "year")
        ordering = ["-year", "employee__employee_id"]

    def __str__(self):
        return f"{self.employee.employee_id} - {self.year} ({self.rating})"      