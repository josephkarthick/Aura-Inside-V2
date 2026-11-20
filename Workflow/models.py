
from django.conf import settings
from django.db import models
from django.utils import timezone


# =====================================================
# 1. WORKFLOW MAIN MENU
# =====================================================

class WorkflowMainMenu(models.Model):

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workflow_main_menus"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "title"]
        verbose_name = "Main Menu"
        verbose_name_plural = "Main Menus"

    def __str__(self):
        return self.title


# =====================================================
# 2. WORKFLOW SUBMENU
# =====================================================

class WorkflowSubMenu(models.Model):

    main_menu = models.ForeignKey(
        WorkflowMainMenu,
        on_delete=models.CASCADE,
        related_name="submenus"
    )

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workflow_submenus"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "title"]
        verbose_name = "Submenu"
        verbose_name_plural = "Submenus"
        constraints = [
            models.UniqueConstraint(
                fields=["main_menu", "title"],
                name="unique_workflow_submenu"
            )
        ]

    def __str__(self):
        return f"{self.main_menu.title} - {self.title}"


# =====================================================
# 3. WORKFLOW FORM
# =====================================================

class WorkflowForm(models.Model):

    submenu = models.ForeignKey(
        WorkflowSubMenu,
        on_delete=models.CASCADE,
        related_name="forms"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    notes_template = models.TextField(blank=True, default="")

    display_order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    allow_draft = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workflow_forms_created"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "title"]
        verbose_name = "Workflow Form"
        verbose_name_plural = "Workflow Forms"

    def __str__(self):
        return self.title


# =====================================================
# 4. FORM QUESTIONS
# =====================================================

class FormQuestion(models.Model):

    QUESTION_TYPES = [
        ("TEXT", "Short Text"),
        ("TEXTAREA", "Long Text"),
        ("NUMBER", "Number"),
        ("EMAIL", "Email"),
        ("PHONE", "Phone Number"),
        ("DATE", "Date"),
        ("SINGLE", "Single Choice"),
        ("MULTIPLE", "Multiple Choice"),
        ("YESNO", "Yes / No"),
    ]

    form = models.ForeignKey(
        WorkflowForm,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    
    display_as_dropdown = models.BooleanField(default=False)

    question_text = models.CharField(max_length=500)

    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        default="TEXT"
    )

    placeholder = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    help_text = models.TextField(blank=True, null=True)

    is_required = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    display_order = models.PositiveIntegerField(default=0)

    # Optional validation configuration
    validation_rules = models.JSONField(
        default=dict,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Form Question"
        verbose_name_plural = "Form Questions"

    def __str__(self):
        return self.question_text


# =====================================================
# 5. QUESTION OPTIONS
# =====================================================

class QuestionOption(models.Model):

    question = models.ForeignKey(
        FormQuestion,
        on_delete=models.CASCADE,
        related_name="options"
    )

    option_text = models.CharField(max_length=255)

    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "Question Option"
        verbose_name_plural = "Question Options"

    def __str__(self):
        return self.option_text


# =====================================================
# 6. WORKFLOW SUBMISSION
# =====================================================

class WorkflowSubmission(models.Model):

    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("SUBMITTED", "Submitted"),
        ("IN_REVIEW", "In Review"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("CANCELLED", "Cancelled"),
    ]

    form = models.ForeignKey(
        WorkflowForm,
        on_delete=models.PROTECT,
        related_name="submissions"
    )

    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="workflow_submissions"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="DRAFT"
    )

    reference_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )

    # Additional process-specific information
    metadata = models.JSONField(
        default=dict,
        blank=True
    )

    remarks = models.TextField(blank=True, null=True)

    submitted_at = models.DateTimeField(
        blank=True,
        null=True
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="workflow_reviews"
    )

    reviewed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Workflow Submission"
        verbose_name_plural = "Workflow Submissions"

    def __str__(self):
        return self.reference_number or f"Submission #{self.pk}"

    def mark_submitted(self):
        self.status = "SUBMITTED"
        self.submitted_at = timezone.now()
        self.save(update_fields=[
            "status",
            "submitted_at",
            "updated_at"
        ])


# =====================================================
# 7. WORKFLOW ANSWERS
# =====================================================

class WorkflowAnswer(models.Model):

    submission = models.ForeignKey(
        WorkflowSubmission,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    question = models.ForeignKey(
        FormQuestion,
        on_delete=models.PROTECT,
        related_name="submitted_answers"
    )

    # Supports text, number, date, single choice,
    # multiple choice and other answer formats.
    answer_value = models.JSONField(
        default=dict,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["question__display_order"]
        verbose_name = "Workflow Answer"
        verbose_name_plural = "Workflow Answers"

        constraints = [
            models.UniqueConstraint(
                fields=["submission", "question"],
                name="unique_workflow_submission_answer"
            )
        ]

    def __str__(self):
        return f"{self.submission} - {self.question}"
