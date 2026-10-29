from django.shortcuts import (render,redirect,get_object_or_404)
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from ADManager.views import get_all_ldap_groups
from django.db.models import Q

from .models import (
    TestPaper,
    TestQuestion,
    TestOption,
    TestPaperGroup,
    UserTestAttempt,
    UserAnswer
)
from ADManager.views import (
    get_all_ldap_groups,
    get_user_ldap_group_dns
)

@login_required
def create_test(request):

    if request.method == "POST":

        start_datetime = request.POST.get(
            "start_datetime"
        )

        end_datetime = request.POST.get(
            "end_datetime"
        )

        test = TestPaper.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            duration_minutes=int(
                request.POST.get("duration_minutes", 30)
            ),
            passing_marks=int(
                request.POST.get("passing_marks", 0)
            ),
            active=request.POST.get("active") == "1",
            max_attempts=int(
                request.POST.get("max_attempts", 1)
            ),
            start_datetime=parse_datetime(start_datetime)
            if start_datetime else None,
            end_datetime=parse_datetime(end_datetime)
            if end_datetime else None,
            created_by=request.user
        )

        group_dns = request.POST.getlist(
            "group_dn[]"
        )

        for group_dn in group_dns:

            if group_dn:

                TestPaperGroup.objects.create(
                    test_paper=test,
                    group_dn=group_dn
                )

        questions = request.POST.getlist(
            "question_text"
        )

        question_types = request.POST.getlist(
            "question_type"
        )

        marks_list = request.POST.getlist(
            "marks"
        )

        for i, question_text in enumerate(
            questions
        ):

            if not question_text.strip():
                continue

            question = TestQuestion.objects.create(
                test=test,
                question_text=question_text,
                question_type=question_types[i],
                marks=int(
                    marks_list[i]
                ) if i < len(marks_list) else 1
            )

            options = request.POST.getlist(
                f"option_{i}[]"
            )

            correct_answers = request.POST.getlist(
                f"correct_{i}[]"
            )

            for option_index, option_text in enumerate(
                options
            ):

                if not option_text.strip():
                    continue

                TestOption.objects.create(
                    question=question,
                    option_text=option_text,
                    is_correct=str(option_index)
                    in correct_answers
                )

        return redirect(
            "Assessment:view_assessments"
        )

    return render(
        request,
        "assessment/create_test.html",
        {
            "ldap_groups": get_all_ldap_groups()
        }
    )
    
@login_required
def qst_paper(request):

    if "ldap_groups" not in request.session:
        request.session["ldap_groups"] = get_user_ldap_group_dns(
            request.user.username
        )

    user_groups = request.session.get(
        "ldap_groups",
        []
    )

    tests = TestPaper.objects.filter(
        active=True,
        group_access__group_dn__in=user_groups
    ).distinct().order_by("-id")

    now = timezone.now()

    for test in tests:
    
        attempt = UserTestAttempt.objects.filter(
            user=request.user,
            test=test,
            status="completed"
        ).first()
    
        test.user_attempt = attempt
    
        test.assessment_status = "inactive"
    
        if not test.active:
            test.assessment_status = "inactive"
    
        elif test.start_datetime and now < test.start_datetime:
            test.assessment_status = "upcoming"
    
        elif (
            test.start_datetime and
            test.end_datetime and
            test.start_datetime <= now <= test.end_datetime
        ):
            test.assessment_status = "active"
    
        elif test.end_datetime and now > test.end_datetime:
            test.assessment_status = "missed"

    context = {
        "tests": tests
    }

    return render(
        request,
        "assessment/qst_paper.html",
        context
    )
    
@login_required
def start_assessment(request, test_id):

    test = get_object_or_404(
        TestPaper,
        id=test_id,
        active=True
    )

    questions = test.questions.prefetch_related(
        "options"
    ).all()

    return render(
        request,
        "assessment/start_assessment.html",
        {
            "test": test,
            "questions": questions
        }
    )

@login_required
def submit_assessment(request, test_id):

    if request.method != "POST":
        return redirect("Assessment:qst_paper")

    test = get_object_or_404(
        TestPaper,
        id=test_id
    )

    attempt = UserTestAttempt.objects.create(
        user=request.user,
        test=test,
        started_at=timezone.now(),
        submitted_at=timezone.now()
    )

    total_marks = 0
    obtained_marks = 0

    questions = test.questions.all()

    for question in questions:

        total_marks += question.marks

        selected_option_id = request.POST.get(
            f"question_{question.id}"
        )

        if not selected_option_id:
            continue

        try:

            selected_option = TestOption.objects.get(
                id=selected_option_id,
                question=question
            )

            is_correct = selected_option.is_correct

            marks = question.marks if is_correct else 0

            if is_correct:
                obtained_marks += marks

            UserAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_option=selected_option,
                is_correct=is_correct,
                obtained_marks=marks
            )

        except TestOption.DoesNotExist:
            pass

    percentage = 0

    if total_marks > 0:
        percentage = (
            obtained_marks / total_marks
        ) * 100

    attempt.total_marks = total_marks
    attempt.obtained_marks = obtained_marks
    attempt.percentage = percentage
    attempt.is_passed = (
        percentage >= test.passing_marks
    )

    attempt.save()

    return redirect(
        "Assessment:assessment_result",
        attempt_id=attempt.id
    )

@login_required
def assessment_result(request, attempt_id):

    attempt = get_object_or_404(
        UserTestAttempt,
        id=attempt_id,
        user=request.user
    )

    answers = UserAnswer.objects.filter(
        attempt=attempt
    ).select_related(
        "question",
        "selected_option"
    )

    total_questions = attempt.test.questions.count()

    correct_count = answers.filter(
        is_correct=True
    ).count()

    wrong_count = total_questions - correct_count

    context = {
        "attempt": attempt,
        "answers": answers,
        "total_questions": total_questions,
        "correct_count": correct_count,
        "wrong_count": wrong_count,
    }

    return render(
        request,
        "assessment/assessment_result.html",
        context
    )  

@login_required
def view_assessments(request):

    tests = TestPaper.objects.all().order_by("-id")

    return render(
        request,
        "assessment/view_assessments.html",
        {
            "tests": tests
        }
    )    
    
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404


@login_required
def assessment_report(request, test_id):

    test = get_object_or_404(
        TestPaper,
        id=test_id
    )

    attempts = UserTestAttempt.objects.filter(
        test=test,
        status="completed"
    ).select_related("user")

    total_users = attempts.count()

    passed_count = attempts.filter(
        is_passed=True
    ).count()

    failed_count = attempts.filter(
        is_passed=False
    ).count()

    avg_score = attempts.aggregate(
        Avg("percentage")
    )["percentage__avg"] or 0

    top_users = attempts.order_by(
        "-percentage"
    )[:3]

    context = {
        "test": test,
        "attempts": attempts,
        "total_users": total_users,
        "passed_count": passed_count,
        "failed_count": failed_count,
        "avg_score": round(avg_score, 2),
        "top_users": top_users,
    }

    return render(
        request,
        "assessment/assessment_report.html",
        context
    )    