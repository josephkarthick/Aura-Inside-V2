
from django.contrib import admin
from .models import (
    FormHeading,
    FormScenario,
    FormQuestion,
    QuestionOption,
    InsuranceCompany,
    CallNotesTemplate,
    CallNote,
)


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 1


@admin.register(FormQuestion)
class FormQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "question_text",
        "scenario",
        "question_type",
        "is_active",
        "display_order",
    )
    list_filter = ("question_type", "is_active")
    search_fields = ("question_text", "scenario__title")
    inlines = [QuestionOptionInline]


@admin.register(FormHeading)
class FormHeadingAdmin(admin.ModelAdmin):
    list_display = ("title", "display_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)


@admin.register(FormScenario)
class FormScenarioAdmin(admin.ModelAdmin):
    list_display = ("title", "heading", "is_active", "is_published")
    list_filter = ("heading", "is_active", "is_published")
    search_fields = ("title", "heading__title")


@admin.register(InsuranceCompany)
class InsuranceCompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(CallNotesTemplate)
class CallNotesTemplateAdmin(admin.ModelAdmin):
    list_display = ("scenario", "is_active", "updated_at")
    list_filter = ("is_active",)


@admin.register(CallNote)
class CallNoteAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "scenario",
        "insurance",
        "status",
        "created_at",
    )
    list_filter = ("status", "insurance", "scenario")
    search_fields = ("called_number", "employee__username")
