from django.db import models
from Accounts.models import AuraInsideUser
from django.utils import timezone


class TestPaper(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True, null=True)

    duration_minutes = models.PositiveIntegerField(default=30)

    passing_marks = models.PositiveIntegerField(default=0)

    shuffle_questions = models.BooleanField(default=True)

    active = models.BooleanField(default=True)

    start_datetime = models.DateTimeField(
        null=True,
        blank=True
    )

    end_datetime = models.DateTimeField(
        null=True,
        blank=True
    )    

    max_attempts = models.PositiveIntegerField(
        default=1
    )    

    created_by = models.ForeignKey(
        AuraInsideUser,
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)


class TestPaperGroup(models.Model):

    test_paper = models.ForeignKey(
        TestPaper,
        on_delete=models.CASCADE,
        related_name="group_access"
    )

    group_dn = models.CharField(max_length=500)

    def __str__(self):
        return self.group_dn        
        
class TestQuestion(models.Model):

    QUESTION_TYPES = [
        ('single', 'Single Choice'),
        ('multiple', 'Multiple Choice'),
    ]

    test = models.ForeignKey(
        TestPaper,
        related_name="questions",
        on_delete=models.CASCADE
    )

    question_text = models.TextField()

    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        default='single'
    )

    marks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.question_text[:100]        
        
class TestOption(models.Model):

    question = models.ForeignKey(
        TestQuestion,
        related_name="options",
        on_delete=models.CASCADE
    )

    option_text = models.CharField(max_length=500)

    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text        

class UserTestAttempt(models.Model):

    user = models.ForeignKey(
        AuraInsideUser,
        on_delete=models.CASCADE
    )

    test = models.ForeignKey(
        TestPaper,
        on_delete=models.CASCADE
    )

    started_at = models.DateTimeField(
        default=timezone.now
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    total_marks = models.PositiveIntegerField(default=0)

    obtained_marks = models.PositiveIntegerField(default=0)

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    is_passed = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        default='completed'
    )

    def __str__(self):
        return f"{self.user} - {self.test.title}"    

class UserAnswer(models.Model):

    attempt = models.ForeignKey(
        UserTestAttempt,
        related_name='answers',
        on_delete=models.CASCADE
    )

    question = models.ForeignKey(
        TestQuestion,
        on_delete=models.CASCADE
    )

    selected_option = models.ForeignKey(
        TestOption,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    is_correct = models.BooleanField(default=False)

    obtained_marks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.attempt.user} - {self.question.id}"        