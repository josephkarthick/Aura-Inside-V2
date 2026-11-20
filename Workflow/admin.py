
from django.contrib import admin
from .models import (
    WorkflowMainMenu,
    WorkflowSubMenu,
    WorkflowForm,
    FormQuestion,
    QuestionOption,
    WorkflowSubmission,
    WorkflowAnswer,
)


@admin.register(WorkflowMainMenu)
class WorkflowMainMenuAdmin(admin.ModelAdmin):
    list_display = ("title", "display_order", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title",)
    ordering = ("display_order", "title")


@admin.register(WorkflowSubMenu)
class WorkflowSubMenuAdmin(admin.ModelAdmin):
    list_display = (
        "title", "main_menu", "display_order", "is_active"
    )
    list_filter = ("main_menu", "is_active")
    search_fields = ("title", "main_menu__title")
    ordering = ("main_menu", "display_order")


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 1


@admin.register(FormQuestion)
class FormQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "question_text",
        "form",
        "question_type",
        "is_required",
        "is_active",
        "display_order",
    )
    list_filter = ("question_type", "is_required", "is_active")
    search_fields = ("question_text", "form__title")
    inlines = [QuestionOptionInline]
    ordering = ("form", "display_order")


@admin.register(WorkflowForm)
class WorkflowFormAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "submenu",
        "display_order",
        "is_active",
        "is_published",
    )
    list_filter = ("submenu", "is_active", "is_published")
    search_fields = ("title", "submenu__title")
    ordering = ("submenu", "display_order")


class WorkflowAnswerInline(admin.TabularInline):
    model = WorkflowAnswer
    extra = 0
    readonly_fields = ("question", "answer_value", "created_at")
    can_delete = False


@admin.register(WorkflowSubmission)
class WorkflowSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "reference_number",
        "form",
        "submitted_by",
        "status",
        "created_at",
        "submitted_at",
    )
    list_filter = ("status", "form", "created_at")
    search_fields = (
        "reference_number",
        "submitted_by__username",
        "form__title",
    )
    readonly_fields = (
        "reference_number",
        "submitted_at",
        "reviewed_at",
        "created_at",
        "updated_at",
    )
    inlines = [WorkflowAnswerInline]


@admin.register(WorkflowAnswer)
class WorkflowAnswerAdmin(admin.ModelAdmin):
    list_display = ("submission", "question", "created_at")
    search_fields = (
        "submission__reference_number",
        "question__question_text",
    )
