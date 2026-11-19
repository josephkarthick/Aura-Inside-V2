
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.db.models import Prefetch
from django.utils import timezone
from django.urls import reverse
from .models import (
    FormHeading,
    FormScenario,
    FormQuestion,
    QuestionOption,
    InsuranceCompany,
    CallNotesTemplate,
    CallNote,
)


def get_user_field(user, field_names):
    """Return the first available non-empty user field."""
    for field_name in field_names:
        value = getattr(user, field_name, None)

        if value not in (None, ""):
            return value

    return "-"


@login_required
@require_http_methods(["GET", "POST"])
def create_form(request):

    if request.method == "POST":

        # CREATE NEW HEADING FROM POPUP
        if request.POST.get("action") == "create_heading":

            heading_title = request.POST.get("new_heading", "").strip()
            description = request.POST.get("new_description", "").strip()

            if not heading_title:
                messages.error(request, "Please enter a heading title.")
                return redirect("CallFlow:callflow_create_form")

            heading, created = FormHeading.objects.get_or_create(
                title=heading_title,
                defaults={
                    "description": description,
                    "created_by": request.user,
                    "display_order": FormHeading.objects.count() + 1,
                }
            )

            if not created:
                if not heading.is_active:
                    messages.error(request, "This heading already exists but is inactive.")
                    return redirect("CallFlow:callflow_create_form")

                messages.info(request, "This heading already exists.")

            else:
                messages.success(request, "New heading created successfully.")

            return redirect(
                f"{reverse('CallFlow:callflow_create_form')}?heading_id={heading.id}"
            )

        # CREATE SCENARIO UNDER SELECTED HEADING
        heading_id = request.POST.get("heading_id", "").strip()
        scenario_title = request.POST.get("scenario", "").strip()

        if not heading_id or not scenario_title:
            messages.error(
                request,
                "Please select a heading and enter a scenario."
            )
            return redirect("CallFlow:callflow_create_form")

        heading = get_object_or_404(
            FormHeading,
            id=heading_id,
            is_active=True
        )

        scenario = FormScenario.objects.create(
            heading=heading,
            title=scenario_title,
            created_by=request.user,
            is_active=True,
            is_published=False,
        )

        messages.success(request, "CallFlow scenario created successfully.")

        return redirect(
            "CallFlow:callflow_form_builder",
            scenario_id=scenario.id
        )

    # GET
    headings = FormHeading.objects.filter(
        is_active=True
    ).order_by("display_order", "title")

    selected_heading_id = request.GET.get("heading_id", "")

    return render(
        request,
        "callflow/Admin/create_form.html",
        {
            "headings": headings,
            "selected_heading_id": selected_heading_id,
        }
    )




@login_required
def form_builder(request, scenario_id):

    scenario = get_object_or_404(
        FormScenario.objects.select_related("heading"),
        id=scenario_id
    )

    # -----------------------------------------
    # PUBLISH FORM
    # -----------------------------------------
    if request.POST.get("action") == "save_publish_status":

        scenario.is_published = (
            request.POST.get("is_published") == "on"
        )

        scenario.save(update_fields=["is_published", "updated_at"])

        messages.success(
            request,
            "Publish status updated successfully."
        )

        return redirect(
            "CallFlow:callflow_form_builder",
            scenario_id=scenario.id
        )

    # -----------------------------------------
    # SAVE CALL NOTES TEMPLATE
    # -----------------------------------------
    if (
        request.method == "POST"
        and request.POST.get("action") == "save_notes_template"
    ):

        template_text = request.POST.get(
            "template_text", ""
        ).strip()

        if not template_text:
            messages.error(
                request,
                "Please enter the call notes template."
            )

        else:
            CallNotesTemplate.objects.update_or_create(
                scenario=scenario,
                defaults={
                    "template_text": template_text,
                    "is_active": True,
                    "updated_by": request.user,
                }
            )
        
            # Save Publish Status
            scenario.is_published = (
                request.POST.get("is_published") == "on"
            )
        
            scenario.save(update_fields=[
                "is_published",
                "updated_at"
            ])
        
            messages.success(
                request,
                "Call Notes Template and Publish Status saved successfully."
            )

            messages.success(
                request,
                "Call Notes Template saved successfully."
            )

        return redirect(
            "CallFlow:callflow_form_builder",
            scenario_id=scenario.id
        )


    # -----------------------------------------
    # SAVE QUESTION
    # -----------------------------------------
    if request.method == "POST":

        question_text = request.POST.get(
            "question_text", ""
        ).strip()

        question_type = request.POST.get(
            "question_type", ""
        ).strip()

        placeholder = request.POST.get(
            "placeholder", ""
        ).strip()

        options = request.POST.getlist("options")

        is_active = request.POST.get("is_active") == "on"

        save_action = request.POST.get(
            "save_action", "save"
        )

        valid_types = ["TEXT", "NUMBER", "SINGLE", "MULTIPLE"]

        valid_options = [
            option.strip()
            for option in options
            if option.strip()
        ]

        if not question_text:

            messages.error(
                request,
                "Please enter the question title."
            )

        elif question_type not in valid_types:

            messages.error(
                request,
                "Please select a valid question type."
            )

        elif question_type in ["SINGLE", "MULTIPLE"] and len(valid_options) < 2:

            messages.error(
                request,
                "Please enter at least two answer options."
            )

        else:

            try:

                with transaction.atomic():

                    next_order = (
                        FormQuestion.objects
                        .filter(scenario=scenario)
                        .count()
                    )

                    question = FormQuestion.objects.create(
                        scenario=scenario,
                        question_text=question_text,
                        question_type=question_type,
                        placeholder=(
                            placeholder
                            if question_type in ["TEXT", "NUMBER"]
                            else ""
                        ),
                        is_active=is_active,
                        display_order=next_order
                    )

                    # Save answer options
                    if question_type in ["SINGLE", "MULTIPLE"]:

                        option_objects = [
                            QuestionOption(
                                question=question,
                                option_text=option_text,
                                is_active=True,
                                display_order=index
                            )
                            for index, option_text in enumerate(valid_options)
                        ]

                        QuestionOption.objects.bulk_create(
                            option_objects
                        )

                messages.success(
                    request,
                    "Question saved successfully."
                )

                builder_url = reverse(
                    "CallFlow:callflow_form_builder",
                    kwargs={
                        "scenario_id": scenario.id
                    }
                )

                if save_action == "add_another":
                    return redirect(builder_url + "?add=1")

                return redirect(builder_url)

            except Exception as e:

                messages.error(
                    request,
                    f"Unable to save question: {str(e)}"
                )

    # -----------------------------------------
    # EMPLOYEE DETAILS
    # -----------------------------------------
    user = request.user

    employee_details = {
        "employee_id": get_user_field(
            user,
            ["employee_id", "empid", "employee_code", "username"]
        ),

        "employee_name": (
            user.get_full_name() or user.username
        ),

        "department": get_user_field(
            user,
            ["department"]
        ),

        "designation": get_user_field(
            user,
            ["designation"]
        ),
    }

    # -----------------------------------------
    # QUESTIONS
    # -----------------------------------------
    questions = (
        FormQuestion.objects
        .filter(scenario=scenario)
        .prefetch_related("options")
        .order_by("display_order", "id")
    )

    # -----------------------------------------
    # INSURANCE COMPANIES
    # -----------------------------------------
    insurance_companies = (
        InsuranceCompany.objects
        .filter(is_active=True)
        .order_by("display_order", "name")
    )

    # -----------------------------------------
    # CALL NOTES TEMPLATE
    # -----------------------------------------
    notes_template = CallNotesTemplate.objects.filter(
        scenario=scenario
    ).first()

    # -----------------------------------------
    # COMMON PLACEHOLDERS
    # -----------------------------------------
    common_tokens = [
        {
            "label": "Employee ID",
            "token": "{{employee_id}}"
        },
        {
            "label": "Employee Name",
            "token": "{{employee_name}}"
        },
        {
            "label": "Department",
            "token": "{{department}}"
        },
        {
            "label": "Designation",
            "token": "{{designation}}"
        },
        {
            "label": "Insurance Company",
            "token": "{{insurance_company}}"
        },
        {
            "label": "Called Number",
            "token": "{{called_number}}"
        },
        {
            "label": "Call Date",
            "token": "{{call_date}}"
        },
        {
            "label": "Call Time",
            "token": "{{call_time}}"
        },
    ]

    # -----------------------------------------
    # QUESTION PLACEHOLDERS
    # -----------------------------------------
    question_tokens = [
        {
            "label": question.question_text,
            "token": "{{q_" + str(question.id) + "}}"
        }
        for question in questions
    ]


    # -----------------------------------------
    # CONTEXT
    # -----------------------------------------
    context = {
        "scenario": scenario,
        "questions": questions,
        "employee_details": employee_details,
        "insurance_companies": insurance_companies,
        "notes_template": notes_template,
        "common_tokens": common_tokens,
        "question_tokens": question_tokens,
    }

    return render(
        request,
        "callflow/Admin/form_builder.html",
        context
    )


    
    
@login_required
def form_list(request):

    headings = FormHeading.objects.prefetch_related(
        "scenarios"
    ).filter(
        is_active=True
    ).order_by("display_order", "title")

    return render(
        request,
        "callflow/Admin/form_list.html",
        {"headings": headings}
    )    
    
    
from django.db.models import Prefetch

from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def employee_callflow_home(request):

    # 1. Fetch published scenarios
    published_scenarios = list(
        FormScenario.objects
        .filter(
            is_active=True,
            is_published=True,
            heading__is_active=True,
        )
        .select_related("heading")
        .order_by("display_order", "title")
    )

    # 2. Fetch only the logged-in employee's call records
    employee_notes = (
        CallNote.objects
        .filter(
            employee=request.user,
            scenario__in=published_scenarios,
        )
        .select_related("scenario", "insurance")
        .order_by("-created_at")
    )

    # 3. Group records by scenario ID
    notes_by_scenario = defaultdict(list)

    for note in employee_notes:
        notes_by_scenario[note.scenario_id].append(note)

    # 4. Attach previous records to their respective scenarios
    for scenario in published_scenarios:
        scenario.employee_call_notes = notes_by_scenario.get(
            scenario.id, []
        )

    # 5. Group scenarios by heading ID
    scenarios_by_heading = defaultdict(list)

    for scenario in published_scenarios:
        scenarios_by_heading[scenario.heading_id].append(scenario)

    # 6. Fetch active headings
    headings = (
        FormHeading.objects
        .filter(is_active=True)
        .order_by("display_order", "title")
    )

    # 7. Attach published scenarios to each heading
    for heading in headings:
        heading.published_scenarios = scenarios_by_heading.get(
            heading.id, []
        )

    return render(
        request,
        "callflow/User/callflow_home.html",
        {
            "headings": headings,
        }
    )

from django.db.models import Prefetch

from django.db.models import Prefetch

from collections import defaultdict
from django.contrib.auth.decorators import login_required

@login_required
def employee_new_form(request):

    # 1. Get active headings
    headings = list(
        FormHeading.objects
        .filter(is_active=True)
        .order_by("display_order", "title")
    )

    # 2. Get published scenarios
    scenarios = list(
        FormScenario.objects
        .filter(
            is_active=True,
            is_published=True,
            heading__is_active=True
        )
        .select_related("heading")
        .order_by("display_order", "title")
    )

    # 3. Get employee's call records
    employee_notes = (
        CallNote.objects
        .filter(
            employee=request.user,
            scenario_id=scenario.id
        )
        .select_related("insurance", "scenario")
        .order_by("-created_at")
    )

    # 4. Group call records by scenario ID
    notes_by_scenario = defaultdict(list)

    for note in employee_notes:
        notes_by_scenario[note.scenario_id].append(note)

    # 5. Attach employee records to each scenario
    scenarios_by_heading = defaultdict(list)

    for scenario in scenarios:

        scenario.employee_call_notes = notes_by_scenario.get(
            scenario.id, []
        )

        scenarios_by_heading[scenario.heading_id].append(scenario)

    # 6. Attach scenarios to their respective headings
    for heading in headings:

        heading.published_scenarios = scenarios_by_heading.get(
            heading.id, []
        )

    return render(
        request,
        "callflow/User/new_form.html",
        {
            "headings": headings,
        }
    )
 
    

@login_required
def employee_fill_form(request, scenario_id):

    scenario = get_object_or_404(
        FormScenario.objects.select_related("heading"),
        id=scenario_id,
        is_active=True,
        is_published=True,
        heading__is_active=True,
    )

    questions = (
        scenario.questions
        .filter(is_active=True)
        .prefetch_related("options")
        .order_by("display_order", "id")
    )

    insurance_companies = InsuranceCompany.objects.filter(
        is_active=True
    ).order_by("display_order", "name")

    notes_template = ""

    if hasattr(scenario, "notes_template"):
        if scenario.notes_template.is_active:
            notes_template = scenario.notes_template.template_text

    # Employee details
    employee_name = (
        request.user.get_full_name()
        or request.user.username
    )

    employee_id = (
        getattr(request.user, "employee_id", None)
        or request.user.username
    )

    department = (
        getattr(request.user, "department", None)
        or "-"
    )

    designation = (
        getattr(request.user, "designation", None)
        or "-"
    )

    if request.method == "POST":

        insurance_id = request.POST.get("insurance")
        called_number = request.POST.get("called_number", "").strip()

        insurance = None

        if insurance_id:
            insurance = InsuranceCompany.objects.filter(
                id=insurance_id,
                is_active=True
            ).first()

            if not insurance:
                messages.error(
                    request,
                    "Please select a valid insurance company."
                )

                return redirect(
                    "CallFlow:employee_fill_form",
                    scenario_id=scenario.id
                )

        # Collect answers using question IDs
        answers = {}

        for question in questions:

            field_name = f"answer_{question.id}"

            if question.question_type == "MULTIPLE":
                answer = request.POST.getlist(field_name)
            else:
                answer = request.POST.get(field_name, "").strip()

            answers[str(question.id)] = {
                "question": question.question_text,
                "type": question.question_type,
                "answer": answer,
            }

        generated_notes = request.POST.get(
            "generated_notes", ""
        ).strip()

        final_notes = request.POST.get(
            "final_notes", ""
        ).strip()

        if not final_notes:
            messages.error(
                request,
                "Please review and enter the final call notes."
            )

        else:
            CallNote.objects.create(
                employee=request.user,
                scenario=scenario,
                insurance=insurance,
                called_number=called_number,
                answers=answers,
                generated_notes=generated_notes,
                final_notes=final_notes,
                status=CallNote.Status.SUBMITTED,
                call_date=timezone.now(),
                submitted_at=timezone.now(),
            )

            messages.success(
                request,
                "Your call details have been submitted successfully."
            )

            return redirect("CallFlow:employee_callflow_home")

    context = {
        "scenario": scenario,
        "heading": scenario.heading,
        "questions": questions,
        "insurance_companies": insurance_companies,
        "notes_template": notes_template,
        "employee_name": employee_name,
        "employee_id": employee_id,
        "department": department,
        "designation": designation,
        "today": timezone.now(),
    }

    return render(
        request,
        "callflow/User/fill_form.html",
        context
    )
    