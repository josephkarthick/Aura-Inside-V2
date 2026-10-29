from django.db import models
from django.utils.timezone import localtime
from Accounts.models import AuraInsideUser  # your custom user table
from django.db import models
from django.core.exceptions import ValidationError
import os

def validate_file_type(value):
    ext = os.path.splitext(value.name)[1].lower()
    allowed = ['.pdf', '.jpeg', '.jpg', '.png', '.doc']
    if ext not in allowed:
        raise ValidationError("Only PDF, JPEG, JPG, PNG, DOC files are allowed.")
        
class SystemEvent(models.Model):
    session_start = models.DateTimeField()
    username = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    from_time = models.DateTimeField()
    to_time = models.DateTimeField()
    idle_minutes = models.PositiveIntegerField(default=0)

    # NEW FIELD
    last_activity = models.DateTimeField(null=True, blank=True)  

    class Meta:
        ordering = ['-session_start', '-from_time']
        verbose_name = 'Idle Session'
        verbose_name_plural = 'Idle Sessions'
        unique_together = ("username", "hostname", "from_time", "to_time")  # 🚫 prevents duplicate rows
        indexes = [
            models.Index(fields=["username", "hostname", "from_time", "to_time"]),  # ⚡ speeds up lookups
        ]

class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(
        AuraInsideUser, on_delete=models.SET_NULL, null=True, related_name="surveys_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    QUESTION_TYPES = [
        ('radio', 'Single Choice'),
        ('checkbox', 'Multiple Choice'),
        ('text', 'Text Answer'),
    ]
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    allow_file_upload = models.BooleanField(default=False)     

    def __str__(self):
        return self.text

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Response(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user = models.ForeignKey(
        AuraInsideUser, on_delete=models.SET_NULL, null=True, related_name="survey_responses"
    )
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, null=True, blank=True, on_delete=models.SET_NULL)
    text_answer = models.TextField(blank=True, null=True)
    uploaded_file = models.FileField(
        upload_to="survey_uploads/",
        validators=[validate_file_type],
        blank=True,
        null=True
    )    

class JobPosting(models.Model):

    SHIFT_CHOICES = [
        ('general', 'General Shift (9AM - 6PM)'),
        ('morning', 'Morning Shift'),
        ('evening', 'Evening Shift'),
        ('night', 'Night Shift'),
        ('rotational', 'Rotational Shift'),
        ('flexible', 'Flexible Shift'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('hold', 'On Hold'),
    ]

    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True)

    employment_type = models.CharField(
        max_length=50,
        choices=EMPLOYMENT_TYPE_CHOICES
    )

    # ✅ Shift Added Here
    shift = models.CharField(
        max_length=20,
        choices=SHIFT_CHOICES,
        default='general'
    )

    experience_required = models.CharField(max_length=50)
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    openings = models.IntegerField()

    last_date = models.DateField(null=True)

    description = models.TextField(null=True)
    responsibilities = models.TextField(null=True)
    skills_required = models.TextField(null=True)
    qualification = models.TextField(null=True)

    posted_by = models.ForeignKey(AuraInsideUser, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):

    WORKING_STATUS_CHOICES = [
        ('working', 'Currently Working'),
        ('not_working', 'Not Working'),
    ]

    NOTICE_STATUS_CHOICES = [
        ('serving', 'Serving Notice'),
        ('not_serving', 'Not Serving'),
    ]

    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    experience = models.CharField(max_length=50)
    current_company = models.CharField(max_length=200, blank=True, null=True)

    # ✅ Working Status
    working_status = models.CharField(
        max_length=20,
        choices=WORKING_STATUS_CHOICES,
        default='not_working'
    )

    # ✅ Notice Period Status
    notice_status = models.CharField(
        max_length=20,
        choices=NOTICE_STATUS_CHOICES,
        blank=True,
        null=True
    )

    # ✅ Notice Period Days
    notice_period_days = models.IntegerField(
        blank=True,
        null=True,
        help_text="Enter notice period in days (e.g., 30, 60, 90)"
    )

    expected_salary = models.CharField(max_length=100)
    resume = models.FileField(upload_to="resumes/")
    cover_letter = models.TextField(blank=True, null=True)

    applied_at = models.DateTimeField(auto_now_add=True)
    
    applied_by = models.ForeignKey(
        AuraInsideUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )    

    def __str__(self):
        return f"{self.full_name} - {self.job.title}"



from django.db import models
from Accounts.models import AuraInsideUser

class RecognitionPoster(models.Model):
    title = models.CharField(max_length=200)

    background = models.ImageField(
        upload_to="recognition_posters/"
    )

    employees = models.ManyToManyField(
        AuraInsideUser,
        blank=True
    )

    start_date = models.DateField()
    end_date = models.DateField()

    is_active = models.BooleanField(default=True)
    
    description = models.TextField(
    blank=True,
    null=True,
    help_text="Short message displayed below the title.")

    created_by = models.ForeignKey(
        AuraInsideUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="recognition_posters"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title