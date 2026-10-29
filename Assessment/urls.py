from django.urls import path
from . import views

app_name = "Assessment"

urlpatterns = [

    path(
        "test/create/",
        views.create_test,
        name="create_test"
    ),

    path(
        "qst-paper/",
        views.qst_paper,
        name="qst_paper"
    ),

    path(
        "qst-paper/<int:test_id>/start/",
        views.start_assessment,
        name="start_assessment"
    ),

    path(
        "qst-paper/<int:test_id>/submit/",
        views.submit_assessment,
        name="submit_assessment"
    ),

    path(
        "result/<int:attempt_id>/",
        views.assessment_result,
        name="assessment_result"
    ),

    path(
        "view-assessments/",
        views.view_assessments,
        name="view_assessments"
    ),
    
    path(
        "assessment-report/<int:test_id>/",
        views.assessment_report,
        name="assessment_report"
    ),

]