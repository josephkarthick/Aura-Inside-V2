from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from datetime import date
from decimal import Decimal, InvalidOperation
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import (
    WorkflowMainMenu,
    WorkflowSubMenu,
    WorkflowForm,
    FormQuestion,
    QuestionOption,
    WorkflowSubmission,
    WorkflowAnswer,
)


# =====================================================
# COMMON HELPERS
# =====================================================

def get_display_order(value, default=0):
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return default


# =====================================================
# 1. MENU BUILDER
# =====================================================

@login_required
@require_http_methods(["GET", "POST"])
def menu_builder(request):

    if request.method == "POST":

        action = request.POST.get("action", "").strip()

        # ---------------------------------------------
        # CREATE MAIN MENU
        # ---------------------------------------------

        if action == "create_main_menu":

            title = request.POST.get("title", "").strip()
            description = request.POST.get("description", "").strip()

            if not title:
                messages.error(request, "Please enter the Main Menu name.")
                return redirect("Workflow:menu_builder")

            WorkflowMainMenu.objects.create(
                title=title,
                description=description,
                display_order=get_display_order(
                    request.POST.get("display_order"),
                    WorkflowMainMenu.objects.count() + 1
                ),
                created_by=request.user,
                is_active=True,
            )

            messages.success(request, "Main Menu created successfully.")
            return redirect("Workflow:menu_builder")

        # ---------------------------------------------
        # UPDATE MAIN MENU
        # ---------------------------------------------

        elif action == "update_main_menu":

            menu = get_object_or_404(
                WorkflowMainMenu,
                pk=request.POST.get("menu_id")
            )

            title = request.POST.get("title", "").strip()

            if not title:
                messages.error(request, "Main Menu name is required.")
                return redirect("Workflow:menu_builder")

            menu.title = title
            menu.description = request.POST.get(
                "description", ""
            ).strip()

            menu.display_order = get_display_order(
                request.POST.get("display_order"),
                menu.display_order
            )

            # Preserve the existing active status when editing only
            # the menu name and description.
            if "is_active" in request.POST:
                menu.is_active = request.POST.get("is_active") == "1"
            menu.save()

            messages.success(request, "Main Menu updated successfully.")
            return redirect("Workflow:menu_builder")

        # ---------------------------------------------
        # CREATE SUBMENU
        # ---------------------------------------------

        elif action == "create_submenu":

            menu_id = request.POST.get("main_menu_id")
            title = request.POST.get("title", "").strip()

            if not menu_id or not title:
                messages.error(
                    request,
                    "Please select a Main Menu and enter the Submenu name."
                )
                return redirect("Workflow:menu_builder")

            main_menu = get_object_or_404(
                WorkflowMainMenu,
                pk=menu_id
            )

            try:
                with transaction.atomic():

                    WorkflowSubMenu.objects.create(
                        main_menu=main_menu,
                        title=title,
                        description=request.POST.get(
                            "description", ""
                        ).strip(),
                        display_order=get_display_order(
                            request.POST.get("display_order"),
                            WorkflowSubMenu.objects.filter(
                                main_menu=main_menu
                            ).count() + 1
                        ),
                        created_by=request.user,
                        is_active=True,
                    )

                messages.success(
                    request,
                    "Submenu created successfully."
                )

            except IntegrityError:
                messages.error(
                    request,
                    "This Submenu already exists under the selected Main Menu."
                )

            return redirect("Workflow:menu_builder")

        # ---------------------------------------------
        # UPDATE SUBMENU
        # ---------------------------------------------

        elif action == "update_submenu":

            submenu = get_object_or_404(
                WorkflowSubMenu.objects.select_related("main_menu"),
                pk=submenu_id
            )

            title = request.POST.get("title", "").strip()

            if not title:
                messages.error(request, "Submenu name is required.")
                return redirect("Workflow:menu_builder")

            submenu.title = title
            submenu.description = request.POST.get(
                "description", ""
            ).strip()

            submenu.display_order = get_display_order(
                request.POST.get("display_order"),
                submenu.display_order
            )

            # Preserve the existing active status when editing only
            # the submenu name and description.
            if "is_active" in request.POST:
                submenu.is_active = request.POST.get("is_active") == "1"

            try:
                submenu.save()
                messages.success(
                    request,
                    "Submenu updated successfully."
                )

            except IntegrityError:
                messages.error(
                    request,
                    "A Submenu with this name already exists under this Main Menu."
                )

            return redirect("Workflow:menu_builder")

        # ---------------------------------------------
        # CREATE FORM UNDER SUBMENU
        # ---------------------------------------------

        elif action == "create_form":

            submenu_id = request.POST.get("submenu_id")
            title = request.POST.get("title", "").strip()

            if not submenu_id or not title:
                messages.error(
                    request,
                    "Please select a Submenu and enter the Form name."
                )
                return redirect("Workflow:menu_builder")

            submenu = get_object_or_404(
                WorkflowSubMenu,
                pk=submenu_id,
                is_active=True,
                main_menu__is_active=True
            )

            with transaction.atomic():

                workflow_form = WorkflowForm.objects.create(
                    submenu=submenu,
                    title=title,
                    description=request.POST.get(
                        "description", ""
                    ).strip(),
                    display_order=get_display_order(
                        request.POST.get("display_order"),
                        WorkflowForm.objects.filter(
                            submenu=submenu
                        ).count() + 1
                    ),
                    created_by=request.user,
                    is_active=True,
                    is_published=False,
                )

            messages.success(
                request,
                "Form created successfully. You can now configure its questions."
            )

            return redirect(
                "Workflow:form_edit",
                form_id=workflow_form.pk
            )

        # ---------------------------------------------
        # UPDATE FORM DETAILS
        # ---------------------------------------------

        elif action == "update_form":

            workflow_form = get_object_or_404(
                WorkflowForm,
                pk=request.POST.get("form_id")
            )

            title = request.POST.get("title", "").strip()

            if not title:
                messages.error(request, "Form name is required.")
                return redirect("Workflow:menu_builder")

            workflow_form.title = title
            workflow_form.description = request.POST.get(
                "description", ""
            ).strip()

            workflow_form.display_order = get_display_order(
                request.POST.get("display_order"),
                workflow_form.display_order
            )

            workflow_form.is_active = request.POST.get("is_active") == "1"
            workflow_form.save()

            messages.success(request, "Form updated successfully.")
            return redirect("Workflow:menu_builder")

        # ---------------------------------------------
        # UNKNOWN ACTION
        # ---------------------------------------------

        else:
            messages.error(request, "Invalid Menu Builder action.")
            return redirect("Workflow:menu_builder")

    # =================================================
    # GET DATA
    # =================================================

    form_queryset = WorkflowForm.objects.order_by(
        "display_order", "title"
    )

    submenu_queryset = (
        WorkflowSubMenu.objects
        .prefetch_related(
            Prefetch(
                "forms",
                queryset=form_queryset
            )
        )
        .order_by("display_order", "title")
    )

    menus = (
        WorkflowMainMenu.objects
        .prefetch_related(
            Prefetch(
                "submenus",
                queryset=submenu_queryset
            )
        )
        .order_by("display_order", "title")
    )

    # Active parent options for creation dropdowns
    active_menus = WorkflowMainMenu.objects.filter(
        is_active=True
    ).order_by("display_order", "title")

    active_submenus = (
        WorkflowSubMenu.objects
        .filter(
            is_active=True,
            main_menu__is_active=True
        )
        .select_related("main_menu")
        .order_by(
            "main_menu__display_order",
            "display_order",
            "title"
        )
    )

    context = {
        "menus": menus,
        "active_menus": active_menus,
        "active_submenus": active_submenus,

        "main_menu_count": WorkflowMainMenu.objects.count(),
        "submenu_count": WorkflowSubMenu.objects.count(),
        "form_count": WorkflowForm.objects.count(),

        # Keep old names available if another template uses them
        "total_menus": WorkflowMainMenu.objects.count(),
        "total_submenus": WorkflowSubMenu.objects.count(),
        "total_forms": WorkflowForm.objects.count(),
    }

    return render(
        request,
        "Workflow/Admin/menu_builder.html",
        context
    )


# =====================================================
# 2. FORM BUILDER - INITIAL VIEW
# =====================================================

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@login_required
@require_http_methods(["GET", "POST"])
def form_edit(request, form_id):

    workflow_form = get_object_or_404(
        WorkflowForm.objects.select_related(
            "submenu",
            "submenu__main_menu"
        ),
        pk=form_id
    )

    if request.method == "POST":

        action = request.POST.get(
            "action", "save_details"
        ).strip()

        # -------------------------------------------------
        # SAVE BASIC FORM DETAILS
        # -------------------------------------------------

        if action == "save_details":

            title = request.POST.get("title", "").strip()
            description = request.POST.get("description", "").strip()

            if not title:
                return JsonResponse({
                    "success": False,
                    "message": "Please enter a form name."
                }, status=400)

            workflow_form.title = title
            workflow_form.description = description

            workflow_form.save(update_fields=[
                "title",
                "description",
                "updated_at"
            ])

            return JsonResponse({
                "success": True,
                "title": workflow_form.title,
                "message": "Form details saved successfully."
            })


        # -------------------------------------------------
        # SAVE NOTES TEMPLATE
        # -------------------------------------------------

        if action == "save_notes_template":

            workflow_form.notes_template = request.POST.get(
                "notes_template", ""
            ).strip()

            workflow_form.save(update_fields=[
                "notes_template",
                "updated_at"
            ])

            return JsonResponse({
                "success": True,
                "message": "Notes template saved successfully."
            })


        # ==========================================
        # PUBLISH / UNPUBLISH FORM
        # ==========================================
        if action in ("publish_form", "unpublish_form"):

            with transaction.atomic():

                workflow_form = (
                    WorkflowForm.objects
                    .select_for_update()
                    .select_related("submenu", "submenu__main_menu")
                    .get(pk=form_id)
                )

                submenu = workflow_form.submenu
                main_menu = submenu.main_menu

                if action == "publish_form":

                    active_question_count = FormQuestion.objects.filter(
                        form=workflow_form,
                        is_active=True
                    ).count()

                    if active_question_count == 0:
                        messages.error(
                            request,
                            "Add at least one active question before publishing."
                        )
                        return redirect(
                            f"{reverse('Workflow:menu_builder')}?form_id={form_id}"
                        )

                    # Activate form
                    workflow_form.is_active = True
                    workflow_form.is_published = True

                    workflow_form.save(
                        update_fields=[
                            "is_active",
                            "is_published",
                            "updated_at"
                        ]
                    )

                    # Activate parent submenu
                    submenu.is_active = True
                    submenu.save(update_fields=["is_active", "updated_at"])

                    # Activate parent main menu
                    main_menu.is_active = True
                    main_menu.save(update_fields=["is_active", "updated_at"])

                    messages.success(
                        request,
                        "Form published successfully. Main Menu and Submenu activated."
                    )

                else:

                    # Unpublish only this form
                    workflow_form.is_published = False

                    workflow_form.save(
                        update_fields=["is_published", "updated_at"]
                    )

                    # Check whether this submenu has other published forms
                    submenu_has_published_forms = WorkflowForm.objects.filter(
                        submenu=submenu,
                        is_active=True,
                        is_published=True
                    ).exists()

                    if not submenu_has_published_forms:

                        submenu.is_active = False
                        submenu.save(
                            update_fields=["is_active", "updated_at"]
                        )

                    # Check whether this main menu has other published forms
                    main_menu_has_published_forms = WorkflowForm.objects.filter(
                        submenu__main_menu=main_menu,
                        is_active=True,
                        is_published=True
                    ).exists()

                    if not main_menu_has_published_forms:

                        main_menu.is_active = False
                        main_menu.save(
                            update_fields=["is_active", "updated_at"]
                        )

                    messages.success(
                        request,
                        "Form unpublished successfully."
                    )

            return redirect(
                f"{reverse('Workflow:menu_builder')}?form_id={form_id}"
            )


        # -------------------------------------------------
        # ADD / UPDATE QUESTION
        # -------------------------------------------------

        if action in ("add_question", "update_question"):

            question_id = request.POST.get("question_id")

            question_text = request.POST.get(
                "question_text", ""
            ).strip()

            question_type = request.POST.get(
                "question_type", ""
            ).strip().upper()

            is_required = request.POST.get(
                "is_required"
            ) == "1"

            # Dropdown is supported only for SINGLE and MULTIPLE.
            display_as_dropdown = (
                request.POST.get("display_as_dropdown") == "true"
            )

            allowed_types = {
                "TEXT",
                "TEXTAREA",
                "NUMBER",
                "EMAIL",
                "PHONE",
                "DATE",
                "SINGLE",
                "MULTIPLE",
                "YESNO",
            }

            if not question_text:
                return JsonResponse({
                    "success": False,
                    "message": "Please enter the question."
                }, status=400)

            if question_type not in allowed_types:
                return JsonResponse({
                    "success": False,
                    "message": "Invalid question type."
                }, status=400)

            # Prevent dropdown configuration on unsupported types.
            if question_type not in ("SINGLE", "MULTIPLE"):
                display_as_dropdown = False

            # Read and clean answer options.
            option_values = [
                value.strip()
                for value in request.POST.getlist("options")
                if value.strip()
            ]

            # Remove duplicate options while preserving order.
            option_values = list(dict.fromkeys(option_values))

            # Choice questions require at least two options.
            if (
                question_type in ("SINGLE", "MULTIPLE")
                and len(option_values) < 2
            ):
                return JsonResponse({
                    "success": False,
                    "message": "Please add at least two unique answer options."
                }, status=400)

            try:

                with transaction.atomic():

                    if action == "update_question":

                        question = get_object_or_404(
                            FormQuestion.objects.select_for_update(),
                            pk=question_id,
                            form=workflow_form
                        )

                        question.question_text = question_text
                        question.question_type = question_type
                        question.is_required = is_required
                        question.display_as_dropdown = display_as_dropdown

                        question.save(update_fields=[
                            "question_text",
                            "question_type",
                            "is_required",
                            "display_as_dropdown",
                            "updated_at"
                        ])

                        # Replace the configured options.
                        # Existing submitted answers remain stored in
                        # WorkflowAnswer.answer_value.
                        question.options.all().delete()

                    else:

                        next_order = (
                            FormQuestion.objects
                            .filter(form=workflow_form)
                            .count() + 1
                        )

                        question = FormQuestion.objects.create(
                            form=workflow_form,
                            question_text=question_text,
                            question_type=question_type,
                            is_required=is_required,
                            display_as_dropdown=display_as_dropdown,
                            is_active=True,
                            display_order=next_order
                        )

                    # Create options only for choice questions.
                    if question_type in ("SINGLE", "MULTIPLE"):

                        QuestionOption.objects.bulk_create([
                            QuestionOption(
                                question=question,
                                option_text=option,
                                display_order=index,
                                is_active=True
                            )
                            for index, option in enumerate(
                                option_values,
                                start=1
                            )
                        ])

            except IntegrityError:
                return JsonResponse({
                    "success": False,
                    "message": "Unable to save the question. Please check the answer options."
                }, status=400)

            return JsonResponse({
                "success": True,
                "message": (
                    "Question added successfully."
                    if action == "add_question"
                    else "Question updated successfully."
                ),
                "question_id": question.id,
                "display_as_dropdown": question.display_as_dropdown
            })


        # -------------------------------------------------
        # DELETE / DEACTIVATE QUESTION
        # -------------------------------------------------

        if action == "delete_question":

            question = get_object_or_404(
                FormQuestion,
                pk=request.POST.get("question_id"),
                form=workflow_form
            )

            # Preserve questions referenced by submitted answers.
            if question.submitted_answers.exists():

                question.is_active = False

                question.save(update_fields=[
                    "is_active",
                    "updated_at"
                ])

                message = (
                    "Question has responses, so it was deactivated."
                )

            else:

                question.delete()

                message = "Question deleted successfully."

            return JsonResponse({
                "success": True,
                "message": message
            })


        # -------------------------------------------------
        # INVALID ACTION
        # -------------------------------------------------

        return JsonResponse({
            "success": False,
            "message": "Invalid form builder action."
        }, status=400)


    # =================================================
    # LOAD FORM BUILDER DATA
    # =================================================

    questions = (
        FormQuestion.objects
        .filter(
            form=workflow_form,
            is_active=True
        )
        .prefetch_related("options")
        .order_by("display_order", "id")
    )

    context = {
        "workflow_form": workflow_form,
        "questions": questions,
        "submenu": workflow_form.submenu,
        "main_menu": workflow_form.submenu.main_menu,
    }

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":

        return render(
            request,
            "Workflow/Admin/form_builder.html",
            context
        )

    return redirect(
        f"{reverse('Workflow:menu_builder')}?form_id={form_id}"
    )

# =====================================================
# 3. EMPLOYEE WORKFLOW
# =====================================================

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.db.models import Prefetch
from django.utils import timezone


@login_required
@require_http_methods(["GET"])
def employee_page(request):
    """
    Employee landing page.
    Displays only active menus and published forms.
    """

    published_forms = (
        WorkflowForm.objects
        .filter(
            is_active=True,
            is_published=True,
            submenu__is_active=True,
            submenu__main_menu__is_active=True
        )
        .order_by("display_order", "title")
    )

    submenus = (
        WorkflowSubMenu.objects
        .filter(
            is_active=True,
            main_menu__is_active=True
        )
        .prefetch_related(
            Prefetch("forms", queryset=published_forms)
        )
        .order_by("display_order", "title")
    )

    menus = (
        WorkflowMainMenu.objects
        .filter(is_active=True)
        .prefetch_related(
            Prefetch("submenus", queryset=submenus)
        )
        .order_by("display_order", "title")
    )

    return render(
        request,
        "Workflow/Employee/employee_page.html",
        {
            "menus": menus,
        }
    )


# =====================================================
# LOAD FORM / SAVE DRAFT / SUBMIT FORM
# =====================================================



@login_required
@require_http_methods(["GET", "POST"])
def employee_form(request, form_id):

    workflow_form = get_object_or_404(
        WorkflowForm.objects.select_related(
            "submenu",
            "submenu__main_menu"
        ),
        pk=form_id,
        is_active=True,
        is_published=True,
        submenu__is_active=True,
        submenu__main_menu__is_active=True
    )

    questions = list(
        FormQuestion.objects
        .filter(form=workflow_form, is_active=True)
        .prefetch_related(
            Prefetch(
                "options",
                queryset=QuestionOption.objects.filter(is_active=True)
            )
        )
        .order_by("display_order", "id")
    )

    # ---------------------------------------------
    # EMPLOYEE DETAILS
    # ---------------------------------------------

    employee_name = (
        request.user.get_full_name()
        or request.user.username
    )

    employee_id = (
        getattr(request.user, "employee_id", None)
        or request.user.username
    )

    department = getattr(request.user, "department", None)
    designation = getattr(request.user, "designation", None)
    shift = getattr(request.user, "shift", None)

    department = str(department) if department else "-"
    designation = str(designation) if designation else "-"
    shift = str(shift) if shift else "-"

    # ---------------------------------------------
    # LATEST DRAFT
    # ---------------------------------------------

    draft = (
        WorkflowSubmission.objects
        .filter(
            form=workflow_form,
            submitted_by=request.user,
            status="DRAFT"
        )
        .order_by("-created_at")
        .first()
    )

    existing_answers = {}

    if draft:
        existing_answers = {
            answer.question_id: answer.answer_value
            for answer in draft.answers.all()
        }

    # Attach saved answers to questions
    for question in questions:
        question.current_answer = existing_answers.get(
            question.id, ""
        )

    # ---------------------------------------------
    # POST: SAVE DRAFT / SUBMIT FORM
    # ---------------------------------------------

    if request.method == "POST":

        action = request.POST.get("action", "").strip()

        if action not in ("save_draft", "submit_form"):
            return JsonResponse({
                "success": False,
                "message": "Invalid submission action."
            }, status=400)

        if (
            action == "save_draft"
            and not workflow_form.allow_draft
        ):
            return JsonResponse({
                "success": False,
                "message": "Draft saving is not enabled."
            }, status=400)

        answers_to_save = []
        validation_errors = []

        # -----------------------------------------
        # PROCESS EACH QUESTION
        # -----------------------------------------

        for question in questions:

            field_name = f"answer_{question.id}"
            question_type = question.question_type

            # GET ANSWER
            if question_type == "MULTIPLE":

                value = [
                    item.strip()
                    for item in request.POST.getlist(field_name)
                    if item.strip()
                ]

            else:

                value = request.POST.get(
                    field_name, ""
                ).strip()

            # -------------------------------------
            # YES / NO
            # -------------------------------------

            if question_type == "YESNO":

                if value and value.lower() not in ("yes", "no"):
                    validation_errors.append(
                        f"Invalid answer for {question.question_text}."
                    )

            # -------------------------------------
            # SINGLE CHOICE
            # -------------------------------------

            elif question_type == "SINGLE":

                allowed = {
                    option.option_text
                    for option in question.options.all()
                }

                if value and value not in allowed:
                    validation_errors.append(
                        f"Invalid option for {question.question_text}."
                    )

            # -------------------------------------
            # MULTIPLE CHOICE
            # -------------------------------------

            elif question_type == "MULTIPLE":

                allowed = {
                    option.option_text
                    for option in question.options.all()
                }

                if (
                    not set(value).issubset(allowed)
                    or len(value) != len(set(value))
                ):
                    validation_errors.append(
                        f"Invalid options for {question.question_text}."
                    )

            # -------------------------------------
            # EMAIL
            # -------------------------------------

            elif question_type == "EMAIL" and value:

                try:
                    validate_email(value)

                except ValidationError:
                    validation_errors.append(
                        f"Enter a valid email address for {question.question_text}."
                    )

            # -------------------------------------
            # NUMBER
            # -------------------------------------

            elif question_type == "NUMBER" and value:

                try:
                    Decimal(value)

                except (InvalidOperation, ValueError):
                    validation_errors.append(
                        f"Enter a valid number for {question.question_text}."
                    )

            # -------------------------------------
            # PHONE - EXACTLY 10 DIGITS
            # -------------------------------------

            elif question_type == "PHONE" and value:

                if not re.fullmatch(r"\d{10}", value):
                    validation_errors.append(
                        f"{question.question_text} must contain exactly 10 digits."
                    )

            # -------------------------------------
            # DATE
            # -------------------------------------

            elif question_type == "DATE" and value:

                try:
                    date.fromisoformat(value)

                except ValueError:
                    validation_errors.append(
                        f"Enter a valid date for {question.question_text}."
                    )

            # -------------------------------------
            # SHORT TEXT - MAXIMUM 100 WORDS
            # -------------------------------------

            elif question_type == "TEXT" and value:

                word_count = len(value.split())

                if word_count > 100:
                    validation_errors.append(
                        f"{question.question_text} cannot exceed 100 words."
                    )

            # -------------------------------------
            # LONG TEXT - MAXIMUM 250 WORDS
            # -------------------------------------

            elif question_type == "TEXTAREA" and value:

                word_count = len(value.split())

                if word_count > 250:
                    validation_errors.append(
                        f"{question.question_text} cannot exceed 250 words."
                    )

            # -------------------------------------
            # REQUIRED FIELD VALIDATION
            # Only mandatory during final submission
            # -------------------------------------

            is_empty = (
                not value
                if isinstance(value, str)
                else len(value) == 0
            )

            if (
                action == "submit_form"
                and question.is_required
                and is_empty
            ):
                validation_errors.append(
                    f"{question.question_text} is required."
                )

            answers_to_save.append((question, value))

        # -----------------------------------------
        # RETURN VALIDATION ERRORS
        # -----------------------------------------

        if validation_errors:

            return JsonResponse({
                "success": False,
                "message": "Please correct the following:",
                "errors": validation_errors
            }, status=400)

        # -----------------------------------------
        # GENERATED AND FINAL NOTES
        # -----------------------------------------

        generated_notes = request.POST.get(
            "generated_notes", ""
        ).strip()

        final_notes = request.POST.get(
            "final_notes", ""
        ).strip()

        # -----------------------------------------
        # SAVE TRANSACTION
        # -----------------------------------------

        with transaction.atomic():

            submission = (
                WorkflowSubmission.objects
                .select_for_update()
                .filter(
                    form=workflow_form,
                    submitted_by=request.user,
                    status="DRAFT"
                )
                .order_by("-created_at")
                .first()
            )

            if not submission:

                submission = WorkflowSubmission.objects.create(
                    form=workflow_form,
                    submitted_by=request.user,
                    status="DRAFT"
                )

            # SAVE ANSWERS
            for question, value in answers_to_save:

                WorkflowAnswer.objects.update_or_create(
                    submission=submission,
                    question=question,
                    defaults={
                        "answer_value": value
                    }
                )

            # PRESERVE METADATA
            metadata = submission.metadata or {}

            metadata.update({
                "generated_notes": generated_notes,
                "final_notes": final_notes,
            })

            submission.metadata = metadata

            submission.save(update_fields=[
                "metadata",
                "updated_at"
            ])

            # -------------------------------------
            # FINAL SUBMISSION
            # -------------------------------------

            if action == "submit_form":

                submission.mark_submitted()

                if not submission.reference_number:

                    submission.reference_number = (
                        f"WF-{submission.pk:06d}"
                    )

                    submission.save(update_fields=[
                        "reference_number",
                        "updated_at"
                    ])

                message = "Form submitted successfully."

            else:

                message = "Draft saved successfully."

        return JsonResponse({
            "success": True,
            "message": message,
            "reference_number": submission.reference_number or "",
            "status": submission.status
        })

    # ---------------------------------------------
    # GET CONTEXT
    # ---------------------------------------------

    context = {
        "form": workflow_form,
        "workflow_form": workflow_form,
        "questions": questions,
        "draft": draft,
        "existing_answers": existing_answers,

        "employee_name": employee_name,
        "employee_id": employee_id,
        "department": department,
        "designation": designation,
        "shift": shift,

        "today": timezone.now(),
    }

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":

        return render(
            request,
            "Workflow/Employee/form_fill.html",
            context
        )

    return redirect("Workflow:employee_page")




# =====================================================
# EMPLOYEE SUBMITTED FORMS
# =====================================================

@login_required
@require_http_methods(["GET"])
def employee_submissions(request, form_id):

    workflow_form = get_object_or_404(
        WorkflowForm,
        pk=form_id,
        is_active=True,
        is_published=True,
        submenu__is_active=True,
        submenu__main_menu__is_active=True
    )

    submissions = (
        WorkflowSubmission.objects
        .filter(
            form=workflow_form,
            submitted_by=request.user,
            status__in=[
                "SUBMITTED",
                "IN_REVIEW",
                "APPROVED",
                "REJECTED"
            ]
        )
        .order_by("-submitted_at", "-created_at")
    )

    return render(
        request,
        "Workflow/Employee/submitted_forms.html",
        {
            "workflow_form": workflow_form,
            "submissions": submissions,
        }
    )


# =====================================================
# VIEW SUBMISSION - READ ONLY
# =====================================================

@login_required
@require_http_methods(["GET"])
def employee_submission_detail(request, submission_id):

    submission = get_object_or_404(
        WorkflowSubmission.objects.select_related(
            "form",
            "form__submenu",
            "form__submenu__main_menu"
        ).prefetch_related(
            "answers__question"
        ),
        pk=submission_id,
        submitted_by=request.user,
        status__in=[
            "SUBMITTED",
            "IN_REVIEW",
            "APPROVED",
            "REJECTED"
        ]
    )

    return render(
        request,
        "Workflow/Employee/submission_detail.html",
        {
            "submission": submission,
            "answers": submission.answers.select_related(
                "question"
            ).order_by("question__display_order")
        }
    )
