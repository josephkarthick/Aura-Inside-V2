from django.contrib import messages
from django.shortcuts import get_object_or_404,render, redirect
from django.contrib.auth.decorators import login_required
from .models import InternalJobPosting
from datetime import date
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .models import IJPApplication
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from Accounts.models import (
    Department,
    Designation,
    AuraInsideUser,
    EmployeeAttendance,
    EmployeeAppraisal,
)


@login_required(login_url="root-login")
def create_ijp(request):

    if request.method == "POST":

        # ======================================================
        # Multiple Departments
        # ======================================================

        department_ids = request.POST.getlist("department")

        # ======================================================
        # Multiple Designations
        # ======================================================

        designation_ids = request.POST.getlist("designation")

        # ------------------------------------------------------
        # Validate
        # ------------------------------------------------------

        if not department_ids:

            messages.error(
                request,
                "Please select at least one department."
            )

            return redirect("IJP:create_ijp")

        if not designation_ids:

            messages.error(
                request,
                "Please select at least one designation."
            )

            return redirect("IJP:create_ijp")

        # ======================================================
        # Create IJP
        # ======================================================

        ijp = InternalJobPosting.objects.create(
            title=request.POST.get("title"),

            vacancies=request.POST.get("vacancies"),

            minimum_experience_months=request.POST.get(
                "minimum_experience_months"
            ),

            minimum_appraisal_rating=request.POST.get(
                "minimum_appraisal_rating"
            ),

            appraisal_year=request.POST.get(
                "appraisal_year"
            ),

            minimum_attendance_rating=request.POST.get(
                "minimum_attendance_rating"
            ),

            attendance_year=request.POST.get(
                "attendance_year"
            ),

            description=request.POST.get(
                "description"
            ),

            application_start_date=request.POST.get(
                "application_start_date"
            ),

            application_end_date=request.POST.get(
                "application_end_date"
            ),

            status=request.POST.get(
                "status"
            ),
        )

        # ======================================================
        # Save Departments
        # ======================================================

        ijp.departments.set(
            department_ids
        )

        # ======================================================
        # Save Designations
        # ======================================================

        ijp.designations.set(
            designation_ids
        )

        # ======================================================
        # Success
        # ======================================================

        messages.success(
            request,
            "Internal Job Posting created successfully."
        )

        return redirect(
            "IJP:create_ijp"
        )

    # ==========================================================
    # GET
    # ==========================================================

    departments = (
        Department.objects
        .all()
        .order_by("name")
    )

    # ==========================================================
    # Build Department → Designations
    # From existing employee data
    # ==========================================================

    employees = (
        AuraInsideUser.objects
        .filter(
            is_active=True,
            department__isnull=False,
            designation__isnull=False,
        )
        .select_related(
            "department",
            "designation",
        )
    )

    department_designations = {}

    for employee in employees:

        department_id = str(
            employee.department_id
        )

        designation_id = employee.designation_id

        if department_id not in department_designations:

            department_designations[
                department_id
            ] = []

        # Prevent duplicate designations
        if not any(
            item["id"] == designation_id
            for item in department_designations[
                department_id
            ]
        ):

            department_designations[
                department_id
            ].append(
                {
                    "id": designation_id,
                    "title": employee.designation.title,
                }
            )

    # ==========================================================
    # Context
    # ==========================================================

    context = {
        "departments": departments,
        "department_designations": department_designations,
    }

    return render(
        request,
        "IJP/Admin/create_form.html",
        context
    )
    
@login_required(login_url="root-login")
def edit_ijp(request, ijp_id):

    ijp = get_object_or_404(
        InternalJobPosting,
        id=ijp_id
    )

    if request.method == "POST":

        ijp.title = request.POST.get("title")
        ijp.department_id = request.POST.get("department")
        ijp.designation_id = request.POST.get("designation")
        ijp.vacancies = request.POST.get("vacancies")
        ijp.minimum_experience_months = request.POST.get(
            "minimum_experience_months"
        )
        ijp.minimum_appraisal_rating = request.POST.get(
            "minimum_appraisal_rating"
        )
        ijp.appraisal_year = request.POST.get(
            "appraisal_year"
        )
        ijp.minimum_attendance_rating = request.POST.get(
            "minimum_attendance_rating"
        )
        ijp.attendance_year = request.POST.get(
            "attendance_year"
        )
        ijp.description = request.POST.get(
            "description"
        )
        ijp.application_start_date = request.POST.get(
            "application_start_date"
        )
        ijp.application_end_date = request.POST.get(
            "application_end_date"
        )
        ijp.status = request.POST.get("status")

        ijp.save()

        messages.success(
            request,
            "Internal Job Posting updated successfully."
        )

        return redirect("IJP:hr_ijp_list")

    context = {
        "ijp": ijp,
        "departments": Department.objects.all().order_by("name"),
        "designations": Designation.objects.all().order_by("title"),
    }

    return render(
        request,
        "IJP/Admin/edit_form.html",
        context
    )    


@login_required(login_url="root-login")
def hr_ijp_list(request):

    ijps = InternalJobPosting.objects.all().order_by("-created_at")

    return render(
        request,
        "IJP/Admin/ijp_list.html",
        {
            "ijps": ijps,
        },
    )
    
from datetime import date
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import InternalJobPosting, IJPApplication
from Accounts.models import EmployeeAttendance, EmployeeAppraisal


@login_required(login_url="root-login")
def ijp_results(request, ijp_id):

    ijp = get_object_or_404(
        InternalJobPosting,
        id=ijp_id
    )

    # ==========================================================
    # APPROVE / REJECT APPLICATION
    # ==========================================================

    if request.method == "POST":

        application_id = request.POST.get("application_id")
        action = request.POST.get("action")
        remarks = request.POST.get("remarks", "").strip()

        application = get_object_or_404(
            IJPApplication.objects.select_related(
                "employee",
                "ijp",
                "ijp__department",
                "ijp__designation",
            ),
            id=application_id,
            ijp=ijp
        )

        # ------------------------------------------------------
        # Validate action
        # ------------------------------------------------------

        if action not in ["approve", "reject"]:

            messages.error(
                request,
                "Invalid application action."
            )

            return redirect(
                "IJP:ijp_results",
                ijp_id=ijp.id
            )

        # ------------------------------------------------------
        # Remarks required
        # ------------------------------------------------------

        if not remarks:

            messages.error(
                request,
                "Please enter remarks before submitting."
            )

            return redirect(
                "IJP:ijp_results",
                ijp_id=ijp.id
            )

        # ------------------------------------------------------
        # Prevent processing already processed application
        # ------------------------------------------------------

        if application.status != "Pending":

            messages.warning(
                request,
                "This application has already been processed."
            )

            return redirect(
                "IJP:ijp_results",
                ijp_id=ijp.id
            )

        # ------------------------------------------------------
        # Update application status
        # ------------------------------------------------------

        if action == "approve":
            application.status = "Approved"
        else:
            application.status = "Rejected"

        application.decision_remarks = remarks
        application.decided_by = request.user

        application.save(
            update_fields=[
                "status",
                "decision_remarks",
                "decided_by",
            ]
        )

        # ======================================================
        # SEND EMAIL TO EMPLOYEE
        # ======================================================

        employee = application.employee
        employee_email = employee.email

        # Person who approved/rejected
        decided_user = application.decided_by

        decided_user_name = (
            decided_user.get_full_name()
            or decided_user.username
        )

        decided_user_email = decided_user.email

        if employee_email:

            status = application.status

            # --------------------------------------------------
            # Email subject and introduction
            # --------------------------------------------------

            if status == "Approved":

                subject = (
                    f"IJP Application Approved - {ijp.title}"
                )

                email_intro = (
                    f"{decided_user_name} has approved your "
                    "Internal Job Posting application."
                )

            else:

                subject = (
                    f"IJP Application Rejected - {ijp.title}"
                )

                email_intro = (
                    f"{decided_user_name} has rejected your "
                    "Internal Job Posting application."
                )

            # --------------------------------------------------
            # Plain text email
            # --------------------------------------------------

            text_message = f"""
            Dear {employee.get_full_name()},
            
            {email_intro}
            
            Job Title   : {ijp.title}
            Department  : {ijp.department}
            Designation : {ijp.designation}
            
            Status      : {status}
            
            Remarks:
            {remarks}
            
            Approved/Rejected By:
            {decided_user_name}
            
            Regards,
            Aura RCM HR
            """

            # --------------------------------------------------
            # HTML email template
            # --------------------------------------------------

            html_message = render_to_string(
                "IJP/Admin/ijp_status.html",
                {
                    "employee": employee,
                    "application": application,
                    "ijp": ijp,
                    "status": status,
                    "remarks": remarks,
                    "email_intro": email_intro,
                    "decided_user": decided_user,
                    "decided_user_name": decided_user_name,
                }
            )

            # --------------------------------------------------
            # CC / BCC
            # --------------------------------------------------

            cc_list = list(
                getattr(
                    settings,
                    "IJP_NOTIFICATION_CC",
                    ["hr@aurarcm",
                     "der_benziger@aurarcm",
                    ]
                )
            )

            bcc_list = list(
                getattr(
                    settings,
                    "IJP_NOTIFICATION_BCC",
                    []
                )
            )

            # --------------------------------------------------
            # Add the person who approved/rejected to CC
            # --------------------------------------------------

            if (
                decided_user_email
                and decided_user_email not in cc_list
                and decided_user_email != employee_email
            ):
                cc_list.append(decided_user_email)

            # --------------------------------------------------
            # Create email
            # --------------------------------------------------

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[employee_email],
                cc=cc_list,
                bcc=bcc_list,
            )

            email.attach_alternative(
                html_message,
                "text/html"
            )

            # --------------------------------------------------
            # Send email
            # --------------------------------------------------

            try:

                email.send(
                    fail_silently=False
                )

                messages.success(
                    request,
                    f"Application {status.lower()} successfully "
                    f"and notification email sent."
                )

            except Exception as e:

                print(
                    f"IJP notification email error: {e}"
                )

                messages.warning(
                    request,
                    f"Application {status.lower()} successfully, "
                    f"but notification email could not be sent."
                )

        else:

            messages.warning(
                request,
                f"Application {application.status.lower()} successfully, "
                f"but employee email address was not found."
            )

        # ------------------------------------------------------
        # Return to IJP Results page
        # ------------------------------------------------------

        return redirect(
            "IJP:ijp_results",
            ijp_id=ijp.id
        )

    # ==========================================================
    # DISPLAY APPLICATIONS
    # ==========================================================


    applications = (
        IJPApplication.objects
        .filter(ijp=ijp)
        .select_related(
            "employee",
            "employee__department",
            "employee__designation",
            "decided_by",
        )
        .order_by("-applied_at")
    )

    today = date.today()

    for application in applications:
        employee = application.employee

        # Date of Joining from accounts_aurainsideuser
        doj = employee.date_joined

        if doj:
            # Convert DateTimeField to DateField if necessary
            if hasattr(doj, "date"):
                doj = doj.date()

            application.doj = doj.strftime("%d-%b-%Y")

            # Calculate completed years and months of service
            years = today.year - doj.year
            months = today.month - doj.month

            if today.day < doj.day:
                months -= 1

            if months < 0:
                years -= 1
                months += 12

            application.length_of_service = (
                f"{years} Years {months} Months"
            )
        else:
            application.doj = "-"
            application.length_of_service = "-"

        # Attendance Rating
        application.attendance_rating = (
            EmployeeAttendance.objects
            .filter(
                employee=employee,
                year=ijp.attendance_year,
            )
            .values_list("rating", flat=True)
            .first()
        )

        if application.attendance_rating is None:
            application.attendance_rating = "-"

        # Appraisal Rating
        application.appraisal_rating = (
            EmployeeAppraisal.objects
            .filter(
                employee=employee,
                year=ijp.appraisal_year,
            )
            .values_list("rating", flat=True)
            .first()
        )

        if application.appraisal_rating is None:
            application.appraisal_rating = "-"


    # ==========================================================
    # CONTEXT
    # ==========================================================

    context = {
        "ijp": ijp,
        "applications": applications,
    }

    return render(
        request,
        "IJP/Admin/result_ijp.html",
        context
    )
    
    
@login_required(login_url="root-login")
def user_ijp_list(request):

    employee = request.user
    today = date.today()

    # ==========================================================
    # EMPLOYEE EXPERIENCE
    # ==========================================================

    experience = calculate_experience_months(
        employee.date_joined.date()
    )

    # ==========================================================
    # GET ALL OPEN IJPs
    # ==========================================================

    ijps = (
        InternalJobPosting.objects
        .filter(status="Open")
        .prefetch_related(
            "departments",
            "designations",
        )
        .order_by("-created_at")
    )

    # ==========================================================
    # PROCESS EACH IJP
    # ==========================================================

    for ijp in ijps:

        # ------------------------------------------------------
        # Default values
        # ------------------------------------------------------

        ijp.eligible = True
        ijp.reasons = []
        ijp.already_applied = False
        ijp.application_status = "open"

        # ------------------------------------------------------
        # Application Expired
        # ------------------------------------------------------

        if today > ijp.application_end_date:

            ijp.application_status = "expired"
            ijp.eligible = False

            continue

        # ======================================================
        # DEPARTMENT CHECK
        # ======================================================

        department_match = ijp.departments.filter(
            id=employee.department_id
        ).exists()

        if not department_match:

            ijp.eligible = False

            ijp.reasons.append(
                "This position is not suitable for your department."
            )

        # ======================================================
        # DESIGNATION CHECK
        # ======================================================

        designation_match = ijp.designations.filter(
            id=employee.designation_id
        ).exists()

        if not designation_match:

            ijp.eligible = False

            ijp.reasons.append(
                "This position is not suitable for your designation."
            )

        # ======================================================
        # IF DEPARTMENT / DESIGNATION DOES NOT MATCH
        # WE STILL SHOW THE JOB POST BUT DO NOT NEED TO CHECK
        # EXPERIENCE / ATTENDANCE / APPRAISAL
        # ======================================================

        if not department_match or not designation_match:

            ijp.application_status = "not_suitable"

            continue

        # ======================================================
        # EXPERIENCE CHECK
        # ======================================================

        if experience < ijp.minimum_experience_months:

            ijp.eligible = False

            ijp.reasons.append(
                f"Minimum experience required is "
                f"{ijp.minimum_experience_months} months. "
                f"Your experience is {experience} months."
            )

        # ======================================================
        # ATTENDANCE CHECK
        # ======================================================

        attendance = EmployeeAttendance.objects.filter(
            employee=employee,
            year=ijp.attendance_year
        ).first()

        if attendance:

            if (
                attendance.rating
                < ijp.minimum_attendance_rating
            ):

                ijp.eligible = False

                ijp.reasons.append(
                    f"Attendance rating should be "
                    f"{ijp.minimum_attendance_rating}. "
                    f"Your rating is {attendance.rating}."
                )

        else:

            ijp.eligible = False

            ijp.reasons.append(
                f"Attendance rating for "
                f"{ijp.attendance_year} not found."
            )

        # ======================================================
        # APPRAISAL CHECK
        # ======================================================

        appraisal = EmployeeAppraisal.objects.filter(
            employee=employee,
            year=ijp.appraisal_year
        ).first()

        if appraisal:

            if (
                appraisal.rating
                < ijp.minimum_appraisal_rating
            ):

                ijp.eligible = False

                ijp.reasons.append(
                    f"Appraisal rating should be "
                    f"{ijp.minimum_appraisal_rating}. "
                    f"Your rating is {appraisal.rating}."
                )

        else:

            ijp.eligible = False

            ijp.reasons.append(
                f"Appraisal rating for "
                f"{ijp.appraisal_year} not found."
            )

        # ======================================================
        # CHECK ALREADY APPLIED
        # ======================================================

        application = (
            IJPApplication.objects
            .filter(
                employee=employee,
                ijp=ijp
            )
            .first()
        )

        if application:

            ijp.already_applied = True
            ijp.application_status = "applied"

            # Keep eligible information for display,
            # but application button will show Already Applied.

    # ==========================================================
    # CONTEXT
    # ==========================================================

    context = {
        "ijps": ijps,
    }

    return render(
        request,
        "IJP/Users/forms.html",
        context,
    )
    
def calculate_experience_months(doj):
    today = date.today()

    months = (
        (today.year - doj.year) * 12
        + (today.month - doj.month)
    )

    if today.day < doj.day:
        months -= 1

    return max(months, 0)


@login_required(login_url="root-login")
def apply_ijp(request, ijp_id):

    employee = request.user

    ijp = get_object_or_404(
        InternalJobPosting,
        id=ijp_id,
        status="Open"
    )

    # ==========================================================
    # 1. CHECK DEPARTMENT
    # ==========================================================

    department_match = ijp.departments.filter(
        id=employee.department_id
    ).exists()

    if not department_match:

        messages.error(
            request,
            "You are not eligible for this Internal Job Posting. "
            "This position is not suitable for your department."
        )

        return redirect("IJP:user_ijp_list")

    # ==========================================================
    # 2. CHECK DESIGNATION
    # ==========================================================

    designation_match = ijp.designations.filter(
        id=employee.designation_id
    ).exists()

    if not designation_match:

        messages.error(
            request,
            "You are not eligible for this Internal Job Posting. "
            "This position is not suitable for your designation."
        )

        return redirect("IJP:user_ijp_list")

    # ==========================================================
    # 3. CHECK EXPERIENCE
    # ==========================================================

    experience = calculate_experience_months(
        employee.date_joined.date()
    )

    if experience < ijp.minimum_experience_months:

        messages.error(
            request,
            f"You are not eligible. Minimum experience required is "
            f"{ijp.minimum_experience_months} months. "
            f"Your experience is {experience} months."
        )

        return redirect("IJP:user_ijp_list")

    # ==========================================================
    # 4. CHECK ATTENDANCE
    # ==========================================================

    attendance = EmployeeAttendance.objects.filter(
        employee=employee,
        year=ijp.attendance_year
    ).first()

    if attendance is None:

        messages.error(
            request,
            f"No attendance rating found for "
            f"{ijp.attendance_year}."
        )

        return redirect("IJP:user_ijp_list")

    if attendance.rating < ijp.minimum_attendance_rating:

        messages.error(
            request,
            f"You are not eligible. Required attendance rating is "
            f"{ijp.minimum_attendance_rating}. "
            f"Your rating is {attendance.rating}."
        )

        return redirect("IJP:user_ijp_list")

    # ==========================================================
    # 5. CHECK APPRAISAL
    # ==========================================================

    appraisal = EmployeeAppraisal.objects.filter(
        employee=employee,
        year=ijp.appraisal_year
    ).first()

    if appraisal is None:

        messages.error(
            request,
            f"No appraisal found for "
            f"{ijp.appraisal_year}."
        )

        return redirect("IJP:user_ijp_list")

    if appraisal.rating < ijp.minimum_appraisal_rating:

        messages.error(
            request,
            f"You are not eligible. Required appraisal rating is "
            f"{ijp.minimum_appraisal_rating}. "
            f"Your rating is {appraisal.rating}."
        )

        return redirect("IJP:user_ijp_list")

    # ==========================================================
    # 6. PREVENT DUPLICATE APPLICATION
    # ==========================================================

    application, created = IJPApplication.objects.get_or_create(
        employee=employee,
        ijp=ijp,
    )

    if not created:

        messages.warning(
            request,
            "You have already applied for this Internal Job Posting."
        )

        return redirect("IJP:user_ijp_list")

    # ==========================================================
    # 7. CONFIRMATION EMAIL TO EMPLOYEE
    # ==========================================================

    employee_subject = (
        f"IJP Application Submitted - {ijp.title}"
    )

    # Get selected departments/designations for email
    department_names = ", ".join(
        ijp.departments.values_list(
            "name",
            flat=True
        )
    )

    designation_names = ", ".join(
        ijp.designations.values_list(
            "title",
            flat=True
        )
    )

    employee_message = f"""
Dear {employee.first_name},

Your application has been submitted successfully.

Job Title   : {ijp.title}


Applied On  : {application.applied_at.strftime('%d-%m-%Y %I:%M %p')}

Our HR team will review your application.

Regards,
Aura RCM HR
"""

    send_mail(
        employee_subject,
        employee_message,
        settings.DEFAULT_FROM_EMAIL,
        [employee.email],
        fail_silently=False,
    )

    # ==========================================================
    # 8. NOTIFICATION EMAIL TO HR / MANAGEMENT
    # ==========================================================

    hr_subject = (
        f"New IJP Application Received - {ijp.title}"
    )

    hr_message = f"""
A new Internal Job Posting application has been received.

Applicant Details
-----------------
Employee Name : {employee.get_full_name()}
Employee ID   : {employee.employee_id}
Email         : {employee.email}

Job Details
-----------
Job Title     : {ijp.title}

Applied On    : {application.applied_at.strftime('%d-%m-%Y %I:%M %p')}

Please review the application in the HR portal.

Regards,
Aura RCM HR System
"""

    send_mail(
        hr_subject,
        hr_message,
        settings.DEFAULT_FROM_EMAIL,
        [
            "der_benziger@aurarcm.com",
            "hr@aurarcm.com",
        ],
        fail_silently=False,
    )

    # ==========================================================
    # SUCCESS
    # ==========================================================

    messages.success(
        request,
        "Congratulations! Your application has been submitted successfully."
    )

    return redirect(
        "IJP:user_ijp_list"
    )


# ============================================================
# EMPLOYEE: MY APPLICATIONS
# ============================================================

@login_required(login_url="root-login")
def my_ijp_applications(request):
    applications = (
        IJPApplication.objects
        .filter(employee=request.user)
        .select_related("ijp", "decided_by")
        .prefetch_related("ijp__departments", "ijp__designations")
        .order_by("-applied_at")
    )

    pending_count = applications.filter(status="Pending").count()
    completed_count = applications.filter(status__in=["Approved", "Rejected"]).count()

    return render(
        request,
        "IJP/Users/my_applications.html",
        {
            "applications": applications,
            "pending_count": pending_count,
            "completed_count": completed_count,
        },
    )


# ============================================================
# HR: RESULTS + APPROVE / REJECT
# ============================================================

@login_required(login_url="root-login")
def ijp_results(request, ijp_id):
    ijp = get_object_or_404(InternalJobPosting, id=ijp_id)

    if request.method == "POST":
        application_id = request.POST.get("application_id")
        action = request.POST.get("action")
        remarks = request.POST.get("remarks", "").strip()

        application = get_object_or_404(
            IJPApplication.objects.select_related("employee", "ijp"),
            id=application_id,
            ijp=ijp,
        )

        if action not in ("approve", "reject"):
            messages.error(request, "Invalid application action.")
            return redirect("IJP:ijp_results", ijp_id=ijp.id)

        if not remarks:
            messages.error(request, "Please enter remarks before submitting.")
            return redirect("IJP:ijp_results", ijp_id=ijp.id)

        if application.status != "Pending":
            messages.warning(request, "This application has already been processed.")
            return redirect("IJP:ijp_results", ijp_id=ijp.id)

        application.status = "Approved" if action == "approve" else "Rejected"
        application.decision_remarks = remarks
        application.decided_by = request.user

        update_fields = ["status", "decision_remarks", "decided_by"]
        if hasattr(application, "decided_at"):
            application.decided_at = timezone.now()
            update_fields.append("decided_at")

        application.save(update_fields=update_fields)

        _send_application_decision_email(application, request)

        messages.success(
            request,
            f"Application {application.status.lower()} successfully.",
        )
        return redirect("IJP:ijp_results", ijp_id=ijp.id)

    applications = (
        IJPApplication.objects
        .filter(ijp=ijp)
        .select_related("employee", "decided_by")
        .order_by("-applied_at")
    )

    # Populate ratings for HR result display when those values are present.
    for application in applications:
        application.attendance_rating = EmployeeAttendance.objects.filter(
            employee=application.employee,
            year=ijp.attendance_year,
        ).values_list("rating", flat=True).first()

        application.appraisal_rating = EmployeeAppraisal.objects.filter(
            employee=application.employee,
            year=ijp.appraisal_year,
        ).values_list("rating", flat=True).first()

    return render(
        request,
        "IJP/Admin/result_ijp.html",
        {
            "ijp": ijp,
            "applications": applications,
        },
    )


# ============================================================
# EMPLOYEE: APPROVED TRAINING PDF
# ============================================================

from pathlib import Path
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
@login_required(login_url="root-login")
def download_ijp_training_pdf(request, application_id):
    application = get_object_or_404(
        IJPApplication,
        id=application_id,
        employee=request.user,
    )

    if application.status not in ["Pending", "Approved"]:
        raise Http404(
            f"Training PDF is unavailable for status: {application.status}"
        )

    pdf_path = (
        Path(settings.MEDIA_ROOT)
        / "IJP"
        / "Training PDF"
        / "Basic Medical billing training.pdf"
    )

    if not pdf_path.is_file():
        raise Http404("The training PDF could not be found on the server.")

    return FileResponse(
        open(pdf_path, "rb"),
        content_type="application/pdf",
        as_attachment=False,
        filename=pdf_path.name,
    )

