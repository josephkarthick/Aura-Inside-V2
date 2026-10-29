from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db.models import Sum, Max
from datetime import datetime
from django.db.models import Q
import pytz
from django.contrib import messages
from .models import Survey, Response, Answer, Question, Option
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from Accounts.models import AuraInsideUser  # adjust import if path differs
from django.http import JsonResponse
from dateutil import parser
import json
from .models import SystemEvent,JobPosting, JobApplication
from django.core.mail import send_mail
from django.conf import settings

ist = pytz.timezone('Asia/Kolkata')

@login_required
def create_survey_and_questions(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        survey = Survey.objects.create(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            created_by=request.user
        )

        questions = request.POST.getlist('question_text')
        question_types = request.POST.getlist('question_type')

        allow_uploads = request.POST.getlist('allow_file_upload')
        
        for i, q_text in enumerate(questions):
            q_type = question_types[i]
        
            allow_upload = str(i) in allow_uploads
        
            question = survey.questions.create(
                text=q_text,
                question_type=q_type,
                allow_file_upload=allow_upload
            )
        
            option_key = f'option_{i}[]'
            options = request.POST.getlist(option_key)
        
            for opt_text in options:
                if opt_text.strip():
                    question.options.create(text=opt_text)
        

        return redirect('HRDesk:survey_list')

    return render(request, 'hrdesk/survey/create_survey.html')


@login_required
def survey_list(request):
    surveys = Survey.objects.all()
    return render(request, "hrdesk/survey/survey_list.html", {"surveys": surveys})



@login_required
def survey_user_view(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    existing_response = Response.objects.filter(survey=survey, user=request.user).first()

    # If the user has already submitted, redirect to the response page immediately
    if existing_response:
        return redirect('HRDesk:survey_user_response', survey_id=survey.id)

    if request.method == "POST":
        # Double-check again on POST
        if existing_response:
            return redirect('HRDesk:survey_user_response', survey_id=survey.id)

        # Create new response
        response = Response.objects.create(
            survey=survey,
            user=request.user,
            remarks=""
        )

        for question in survey.questions.all():
            input_name = f"question_{question.id}"
            file_input_name = f"file_{question.id}"
        
            uploaded_file = request.FILES.get(file_input_name)
        
            if question.question_type == "text":
                text_answer = request.POST.get(input_name, "").strip()
        
                Answer.objects.create(
                    response=response,
                    question=question,
                    text_answer=text_answer if text_answer else None,
                    uploaded_file=uploaded_file
                )
        
            elif question.question_type == "radio":
                option_id = request.POST.get(input_name)
                option = Option.objects.filter(id=option_id, question=question).first() if option_id else None
        
                Answer.objects.create(
                    response=response,
                    question=question,
                    option=option,
                    uploaded_file=uploaded_file
                )
        
            elif question.question_type == "checkbox":
                option_ids = request.POST.getlist(input_name)
        
                for oid in option_ids:
                    option = Option.objects.filter(id=oid, question=question).first()
                    if option:
                        Answer.objects.create(
                            response=response,
                            question=question,
                            option=option,
                            uploaded_file=uploaded_file
                        )
        

        messages.success(request, "Survey submitted successfully.")
        # Redirect to the response page after submission
        return redirect('HRDesk:survey_user_response', survey_id=survey.id)

    # Render the form if not already submitted
    return render(request, "hrdesk/survey/survey_user_view.html", {
        "survey": survey,
        "existing_response": existing_response
    })


@login_required
def survey_user_response_view(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    existing_response = get_object_or_404(Response, survey=survey, user=request.user)
    return render(request, "hrdesk/survey/survey_user_response.html", {
        "survey": survey,
        "existing_response": existing_response
    })

@login_required
def delete_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)

    # Optional: Only allow the creator or staff to delete
    if request.user != survey.created_by and not request.user.is_staff:
        messages.error(request, "You do not have permission to delete this survey.")
        return redirect('HRDesk:survey_list')

    if request.method == 'POST':
        survey.delete()
        messages.success(request, "Survey deleted successfully.")
        return redirect('HRDesk:survey_list')

    # If GET request, show confirm page or redirect
    return redirect('HRDesk:survey_list')



from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Survey, Option, Answer, Response, AuraInsideUser



def survey_results(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)

    results = []

    # --- Question-based results ---
    for question in survey.questions.all():

        # ==============================
        # RADIO / CHECKBOX QUESTIONS
        # ==============================
        if question.question_type in ["radio", "checkbox"]:

            options = (
                Option.objects
                .filter(question=question)
                .annotate(user_count=Count('answer__response__user', distinct=True))
                .order_by('-user_count')
            )

            for opt in options:
                results.append({
                    "question": question.text,
                    "question_id": question.id,
                    "answer": opt.text,
                    "answer_id": opt.id,
                    "count": opt.user_count,
                    "usernames": None,
                    "file_url": None
                })

        # ==============================
        # TEXT QUESTIONS
        # ==============================
        elif question.question_type == "text":

            text_answers = (
                Answer.objects
                .filter(question=question)
                .exclude(text_answer__isnull=True)
                .exclude(text_answer="")
                .select_related('response__user')
            )

            for ans in text_answers:
                results.append({
                    "question": question.text,
                    "question_id": question.id,
                    "answer": ans.text_answer,
                    "answer_id": None,
                    "count": None,
                    "usernames": [ans.response.user.username] if ans.response.user else [],
                    "file_url": None
                })

        # ==============================
        # FILE UPLOADS (ALL TYPES)
        # ==============================

        file_answers = (
            Answer.objects
            .filter(question=question)
            .select_related('response__user')
        )
        
        for ans in file_answers:
            # SAFE CHECK
            if ans.uploaded_file and ans.uploaded_file.name:
                results.append({
                    "question": question.text,
                    "question_id": question.id,
                    "answer": "File Uploaded",
                    "answer_id": None,
                    "count": 1,
                    "usernames": [ans.response.user.username] if ans.response.user else [],
                    "file_url": ans.uploaded_file.url
                })
        

    # ==============================
    # USER STATISTICS
    # ==============================

    all_users = AuraInsideUser.objects.all()
    responded_user_ids = Response.objects.filter(survey=survey).values_list("user_id", flat=True)

    responded_users = AuraInsideUser.objects.filter(id__in=responded_user_ids)
    pending_users = all_users.exclude(id__in=responded_user_ids)

    day_responded = responded_users.filter(shift__name="Day")
    night_responded = responded_users.filter(shift__name="Night")
    day_pending = pending_users.filter(shift__name="Day")
    night_pending = pending_users.filter(shift__name="Night")

    context = {
        "survey": survey,
        "results": results,
        "user_stats": {
            "total_users": all_users.count(),
            "responded": responded_users.count(),
            "pending": pending_users.count(),
            "day_shift": day_responded.count(),
            "night_shift": night_responded.count(),
            "day_pending_count": day_pending.count(),
            "night_pending_count": night_pending.count(),
            "responded_users": responded_users,
            "pending_users": pending_users,
            "day_responded": day_responded,
            "night_responded": night_responded,
            "day_pending": day_pending,
            "night_pending": night_pending,
        }
    }

    return render(request, 'hrdesk/survey/survey_results.html', context)

import csv
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def export_survey_results_csv(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response.write('\ufeff')  # UTF-8 BOM for Excel
    response['Content-Disposition'] = (
        f'attachment; filename="{survey.title}_results.csv"'
    )

    writer = csv.writer(response)

    # Header
    writer.writerow([
        "Username",
        "First Name",
        "Last Name",
        "Shift",
        "Status",
        "Question",
        "Answer",
    ])

    users = AuraInsideUser.objects.select_related("shift").order_by("username")

    for user in users:

        survey_response = (
            Response.objects
            .filter(survey=survey, user=user)
            .prefetch_related("answers__question", "answers__option")
            .first()
        )

        # -----------------------
        # Pending User
        # -----------------------
        if not survey_response:
            writer.writerow([
                user.username,
                user.first_name,
                user.last_name,
                user.shift.name if user.shift else "",
                "Pending",
                "",
                "",
            ])
            continue

        # -----------------------
        # Completed User
        # -----------------------
        status = "Complete"

        answers = survey_response.answers.all()

        # Safety: response exists but no answers
        if not answers.exists():
            writer.writerow([
                user.username,
                user.first_name,
                user.last_name,
                user.shift.name if user.shift else "",
                status,
                "",
                "",
            ])
            continue

        for answer in answers:

            if answer.option:
                value = answer.option.text

            elif answer.text_answer:
                value = answer.text_answer

            elif answer.uploaded_file:
                value = request.build_absolute_uri(answer.uploaded_file.url)

            else:
                value = ""

            writer.writerow([
                user.username,
                user.first_name,
                user.last_name,
                user.shift.name if user.shift else "",
                status,
                answer.question.text,
                value,
            ])

    return response

def survey_user_list(request, survey_id, user_type):
    survey = get_object_or_404(Survey, id=survey_id)

    responded_user_ids = Response.objects.filter(survey=survey).values_list("user_id", flat=True)
    responded_users = AuraInsideUser.objects.filter(id__in=responded_user_ids)
    pending_users = AuraInsideUser.objects.exclude(id__in=responded_user_ids)

    # Determine which users to show
    if user_type == "responded":
        users = responded_users
        page_title = "Responded Users"
    elif user_type == "pending":
        users = pending_users
        page_title = "Pending Users"
    elif user_type == "day_responded":
        users = responded_users.filter(shift__name="Day")
        page_title = "Day Shift Responded Users"
    elif user_type == "night_responded":
        users = responded_users.filter(shift__name="Night")
        page_title = "Night Shift Responded Users"
    elif user_type == "day_pending":
        users = pending_users.filter(shift__name="Day")
        page_title = "Day Shift Pending Users"
    elif user_type == "night_pending":
        users = pending_users.filter(shift__name="Night")
        page_title = "Night Shift Pending Users"
    else:
        users = AuraInsideUser.objects.none()
        page_title = "Users"

    context = {
        "survey": survey,
        "users": users,
        "page_title": page_title,
    }
    return render(request, "hrdesk/survey/survey_user_list.html", context)


def survey_answer_users(request, survey_id, question_id, answer_id):
    survey = get_object_or_404(Survey, id=survey_id)
    users = AuraInsideUser.objects.filter(
        survey_responses__answers__question_id=question_id,
        survey_responses__answers__option_id=answer_id
    ).distinct()

    option = get_object_or_404(Option, id=answer_id)
    page_title = f"Users who selected answer '{option.text}'"

    return render(request, "hrdesk/survey/survey_user_list.html", {
        "survey": survey,
        "users": users,
        "page_title": page_title
    })


def survey_text_answer_users(request, survey_id, question_id):
    text = request.GET.get('text', '')
    survey = get_object_or_404(Survey, id=survey_id)
    users = AuraInsideUser.objects.filter(
        survey_responses__answers__question_id=question_id,
        survey_responses__answers__text_answer=text
    ).distinct()

    page_title = f"Users who answered '{text}'"

    return render(request, "hrdesk/survey/survey_user_list.html", {
        "survey": survey,
        "users": users,
        "page_title": page_title
    })

# =========================================
# 🏢 HR DASHBOARD – LIST JOBS
# =========================================
@login_required
def hr_job_list(request):

    jobs = JobPosting.objects.all().order_by("-id")

    print("====================================")
    print("LOGGED IN USER:", request.user)
    print("USER ID:", request.user.id)
    print("TOTAL JOBS:", jobs.count())

    for job in jobs:
        print(
            "JOB:",
            job.id,
            "| TITLE:",
            job.title,
            "| POSTED BY:",
            getattr(job, "posted_by_id", "NO posted_by FIELD"),
        )

    print("====================================")

    return render(
        request,
        "hrdesk/careers/job_list.html",
        {
            "jobs": jobs,
        },
    )


# =========================================
# ➕ CREATE JOB
# =========================================
@login_required
def job_post(request):

    if request.method == "POST":
        JobPosting.objects.create(
            title=request.POST.get("title"),
            department=request.POST.get("department"),
            location=request.POST.get("location"),
            employment_type=request.POST.get("employment_type"),
            shift=request.POST.get("shift"),
            experience_required=request.POST.get("experience_required"),
            salary_range=request.POST.get("salary_range"),
            openings=request.POST.get("openings"),
            last_date=request.POST.get("last_date"),
            description=request.POST.get("description"),
            responsibilities=request.POST.get("responsibilities"),
            skills_required=request.POST.get("skills_required"),
            qualification=request.POST.get("qualification"),
            posted_by=request.user
        )

        messages.success(request, "Job Posted Successfully ✅")
        return redirect("HRDesk:hr_job_list")

    return render(request, "hrdesk/careers/job_post.html")


# =========================================
# 👀 VIEW APPLICANTS PER JOB
# =========================================
@login_required
def job_applicants(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    applications = JobApplication.objects.filter(job=job).order_by("-applied_at")

    return render(request, "hrdesk/careers/job_applicants.html", {
        "job": job,
        "applications": applications,
    })


# =========================================
# 📝 CANDIDATE APPLY
# =========================================


@login_required
def job_apply(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)

    # 🔒 Prevent duplicate applications
    if JobApplication.objects.filter(job=job, applied_by=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect("Intranet:home")

    if request.method == "POST":

        application = JobApplication.objects.create(
            job=job,
            applied_by=request.user,
            full_name=request.user.get_full_name(),
            email=request.user.email,
            phone=request.POST.get("phone"),
            experience=request.POST.get("experience"),
            current_company=request.POST.get("current_company"),
            expected_salary=request.POST.get("expected_salary"),
            resume=request.FILES.get("resume"),
            cover_letter=request.POST.get("cover_letter"),
        )

        # 📩 EMAIL ONLY TO HR
        subject = f"New Internal Application - {job.title}"

        message = f"""
New internal application submitted.

Job: {job.title}

Employee Name: {request.user.get_full_name()}
Login ID: {request.user.username}
Department: {request.user.department}
Shift: {request.user.shift}

Phone: {application.phone}
Experience: {application.experience}
Expected Salary: {application.expected_salary}

Applied On: {application.applied_at}
"""
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [
                "karthick.t@aurabpo.com",
                
            ],
            fail_silently=True,
        )
        

        messages.success(request, "Application submitted successfully.")
        return redirect("Intranet:home")

    return render(request, "hrdesk/careers/job_apply.html", {"job": job})


from datetime import date
from django.shortcuts import render
from HRDesk.models import RecognitionPoster
from datetime import date
from django.shortcuts import get_object_or_404

from datetime import date
from django.shortcuts import render, get_object_or_404
from HRDesk.models import RecognitionPoster

def Reg_view(request):
    posters = (
        RecognitionPoster.objects
        .filter(is_active=True)
        .prefetch_related("employees")
        .order_by("id")
    )

    poster_id = request.GET.get("id")

    if poster_id:
        recognition_poster = get_object_or_404(
            posters, id=poster_id
        )
    else:
        recognition_poster = posters.first()

    if not recognition_poster:
        return render(
            request,
            "HRDesk/recognition/poster_view.html",
            {
                "recognition_poster": None,
                "next_poster": None,
                "prev_poster": None,
            },
        )

    poster_list = list(posters)
    current_index = next(
        i for i, poster in enumerate(poster_list)
        if poster.pk == recognition_poster.pk
    )

    return render(
        request,
        "HRDesk/recognition/poster_view.html",
        {
            "recognition_poster": recognition_poster,
            "prev_poster": (
                poster_list[current_index - 1]
                if current_index > 0 else None
            ),
            "next_poster": (
                poster_list[current_index + 1]
                if current_index < len(poster_list) - 1 else None
            ),
        },
    )
    
def recognition_create(request):

    employees = AuraInsideUser.objects.filter(is_active=True)

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        poster = RecognitionPoster.objects.create(

            title=title,

            description=description,

            background=request.FILES["background"],

            start_date=start_date,

            end_date=end_date,

            is_active="is_active" in request.POST,

            created_by=request.user

        )

        poster.employees.set(request.POST.getlist("employees"))

        return redirect("HRDesk:recognition_list")

    return render(

        request,

        "HRDesk/recognition/create_poster.html",

        {

            "employees":employees

        }

    )    
    
def recognition_list(request):

    posters = RecognitionPoster.objects.prefetch_related(
        "employees"
    ).select_related(
        "created_by"
    ).order_by("-created_at")

    return render(
        request,
        "HRDesk/recognition/poster_list.html",
        {
            "posters": posters
        }
    )  
    
from django.shortcuts import get_object_or_404

def recognition_edit(request, pk):

    poster = get_object_or_404(
        RecognitionPoster,
        pk=pk
    )

    employees = AuraInsideUser.objects.filter(
        is_active=True
    ).order_by("employee_id")

    if request.method == "POST":

        poster.title = request.POST.get("title")
        poster.description = request.POST.get("description")
        poster.start_date = request.POST.get("start_date")
        poster.end_date = request.POST.get("end_date")
        poster.is_active = "is_active" in request.POST

        if request.FILES.get("background"):
            poster.background = request.FILES["background"]

        poster.save()

        poster.employees.set(
            request.POST.getlist("employees")
        )

        return redirect("HRDesk:recognition_list")

    return render(
        request,
        "HRDesk/recognition/create_poster.html",
        {
            "poster": poster,
            "employees": employees,
            "edit": True,
        }
    )

from django.contrib import messages

def recognition_delete(request, pk):

    poster = get_object_or_404(
        RecognitionPoster,
        pk=pk
    )

    if poster.background:
        poster.background.delete(save=False)

    poster.delete()

    messages.success(
        request,
        "Recognition poster deleted successfully."
    )

    return redirect("HRDesk:recognition_list")    