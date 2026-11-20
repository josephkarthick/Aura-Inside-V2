from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.db.models import Prefetch
from django.utils import timezone
from django.urls import reverse
from collections import defaultdict




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
def form_builder(request):
    """Single CallFlow admin page: list headings/scenarios and edit the selected form."""

    builder_url = reverse("CallFlow:callflow_form_builder")
    action = request.POST.get("action", "") if request.method == "POST" else ""
    # --------------------------------------------------
    # CREATE SCENARIO (optionally create its heading too)
    # --------------------------------------------------
    if request.method == "POST" and request.POST.get("action") == "create_scenario":
        heading_id = request.POST.get("heading_id", "").strip()
        scenario_title = request.POST.get("scenario", "").strip()
        scenario_description = request.POST.get("scenario_description", "").strip()

        if not scenario_title:
            messages.error(request, "Please enter a scenario name.")
            return redirect(builder_url)

        if heading_id == "__new__":
            heading_title = request.POST.get("new_heading", "").strip()
            heading_description = request.POST.get("new_description", "").strip()
            if not heading_title:
                messages.error(request, "Please enter the new heading name.")
                return redirect(builder_url)

            heading, created = FormHeading.objects.get_or_create(
                title=heading_title,
                defaults={
                    "description": heading_description,
                    "created_by": request.user,
                    "display_order": FormHeading.objects.count() + 1,
                    "is_active": True,
                },
            )
            if not created and not heading.is_active:
                messages.error(request, "This heading already exists but is inactive.")
                return redirect(builder_url)
        else:
            heading = get_object_or_404(FormHeading, id=heading_id, is_active=True)

        scenario = FormScenario.objects.create(
            heading=heading,
            title=scenario_title,
            description=scenario_description,
            created_by=request.user,
            is_active=True,
            is_published=False,
            display_order=FormScenario.objects.filter(heading=heading).count() + 1,
        )
        messages.success(request, "New form created successfully.")
        return redirect(f"{builder_url}?scenario_id={scenario.pk}")

    # --------------------------------------------------
    # SELECTED SCENARIO
    # --------------------------------------------------
    selected_id = request.POST.get("scenario_id") or request.GET.get("scenario_id")
    selected_scenario = None
    if selected_id:
        selected_scenario = get_object_or_404(
            FormScenario.objects.select_related("heading"),
            pk=selected_id, is_active=True, heading__is_active=True,
        )

    # --------------------------------------------------
    # SAVE QUESTION / NOTES TEMPLATE / PUBLISH STATUS
    # --------------------------------------------------
    if request.method == "POST":
        if selected_scenario is None:
            messages.error(request, "Select a scenario before editing its form.")
            return redirect(builder_url)

        action = request.POST.get("action", "")
        return_url = f"{builder_url}?scenario_id={selected_scenario.pk}"

        if action == "save_publish_status":
        
            selected_scenario.is_published = (
                request.POST.get("is_published") == "1"
            )
        
            selected_scenario.save(
                update_fields=["is_published", "updated_at"]
            )
        
            messages.success(
                request,
                "Form published successfully."
                if selected_scenario.is_published
                else "Form moved to Draft successfully."
            )
        
            return redirect(return_url)

        if action == "save_notes_template":
            template_text = request.POST.get("template_text", "").strip()
        
            if not template_text:
                messages.error(request, "Please enter the call notes template.")
            else:
                CallNotesTemplate.objects.update_or_create(
                    scenario=selected_scenario,
                    defaults={
                        "template_text": template_text,
                        "is_active": True,
                        "updated_by": request.user,
                    },
                )
                messages.success(
                    request,
                    "Call Notes Template saved successfully."
                )
        
            return redirect(return_url)

        # Default POST action is adding a question.
        question_text = request.POST.get("question_text", "").strip()
        question_type = request.POST.get("question_type", "").strip()
        placeholder = request.POST.get("placeholder", "").strip()
        options = [value.strip() for value in request.POST.getlist("options") if value.strip()]
        is_active = request.POST.get("is_active") == "on"
        save_action = request.POST.get("save_action", "save")
        valid_types = {"TEXT", "NUMBER", "SINGLE", "MULTIPLE"}

        if not question_text:
            messages.error(request, "Please enter the question title.")
            return redirect(return_url)
        if question_type not in valid_types:
            messages.error(request, "Please select a valid question type.")
            return redirect(return_url)
        if question_type in {"SINGLE", "MULTIPLE"} and len(options) < 2:
            messages.error(request, "Please enter at least two answer options.")
            return redirect(return_url)

        try:
            with transaction.atomic():
                next_order = FormQuestion.objects.filter(scenario=selected_scenario).count()
                question = FormQuestion.objects.create(
                    scenario=selected_scenario,
                    question_text=question_text,
                    question_type=question_type,
                    placeholder=placeholder if question_type in {"TEXT", "NUMBER"} else "",
                    is_active=is_active,
                    display_order=next_order,
                )
                if question_type in {"SINGLE", "MULTIPLE"}:
                    QuestionOption.objects.bulk_create([
                        QuestionOption(question=question, option_text=value, is_active=True, display_order=index)
                        for index, value in enumerate(options)
                    ])
            messages.success(request, "Question saved successfully.")
            if save_action == "add_another":
                return redirect(return_url + "&add=1")
            return redirect(return_url)
        except Exception:
            logger.exception("CallFlow question save failed for scenario %s", selected_scenario.pk)
            messages.error(request, "Unable to save the question. Please check the entered details.")
            return redirect(return_url)

    # --------------------------------------------------
    # SIDEBAR DATA
    # --------------------------------------------------
    headings = list(
        FormHeading.objects.filter(is_active=True).order_by("display_order", "title")
    )
    scenarios = FormScenario.objects.filter(
        heading__in=headings, is_active=True
    ).select_related("heading").order_by("display_order", "title")
    scenarios_by_heading = defaultdict(list)
    for item in scenarios:
        scenarios_by_heading[item.heading_id].append(item)
    for heading in headings:
        heading.admin_scenarios = scenarios_by_heading.get(heading.pk, [])

    # --------------------------------------------------
    # BUILDER DATA
    # --------------------------------------------------
    context = {"headings": headings, "selected_scenario": selected_scenario, "scenario": selected_scenario}
    if selected_scenario:
        questions = list(
            FormQuestion.objects.filter(scenario=selected_scenario)
            .prefetch_related("options").order_by("display_order", "id")
        )
        user = request.user
        context.update({
            "questions": questions,
            "employee_details": {
                "employee_id": get_user_field(user, ["employee_id", "empid", "employee_code", "username"]),
                "employee_name": user.get_full_name() or user.username,
                "department": get_user_field(user, ["department"]),
                "designation": get_user_field(user, ["designation"]),
            },
            "insurance_companies": InsuranceCompany.objects.filter(is_active=True).order_by("display_order", "name"),
            "notes_template": CallNotesTemplate.objects.filter(scenario=selected_scenario).first(),
            "common_tokens": [
                {"label": "Employee ID", "token": "{{employee_id}}"},
                {"label": "Employee Name", "token": "{{employee_name}}"},
                {"label": "Department", "token": "{{department}}"},
                {"label": "Designation", "token": "{{designation}}"},
                {"label": "Insurance Company", "token": "{{insurance_company}}"},
                {"label": "Called Number", "token": "{{called_number}}"},
                {"label": "Call Date", "token": "{{call_date}}"},
                {"label": "Call Time", "token": "{{call_time}}"},
            ],
            "question_tokens": [
                {"label": q.question_text, "token": "{{q_" + str(q.pk) + "}}"}
                for q in questions
            ],
        })

    return render(request, "callflow/Admin/form_builder.html", context)


    
    
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
    