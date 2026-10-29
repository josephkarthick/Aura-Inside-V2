from django.urls import path
from . import views  # Import the views module

app_name = 'HRDesk'

urlpatterns = [


    # Survey CRUD
    path('survey/create/', views.create_survey_and_questions, name='create_survey'),
    path('surveys/', views.survey_list, name='survey_list'),
    path('survey/<int:survey_id>/take/', views.survey_user_view, name='survey_user_view'),
    path('survey/<int:survey_id>/delete/', views.delete_survey, name='delete_survey'),

    # Survey results & responses
    path('survey/<int:survey_id>/results/', views.survey_results, name='survey_results'),
    path('survey/<int:survey_id>/response/', views.survey_user_response_view, name='survey_user_response'),

    # User list filters
    path('survey/<int:survey_id>/users/<str:user_type>/', views.survey_user_list, name='survey_user_list'),

    # Users who selected a specific answer (radio/checkbox)
    path(
        'survey/<int:survey_id>/answer_users/<int:question_id>/<int:answer_id>/',
        views.survey_answer_users,
        name='survey_answer_users'
    ),

    # Users who gave a specific text answer
    path(
        'survey/<int:survey_id>/text_answer_users/<int:question_id>/',
        views.survey_text_answer_users,
        name='survey_text_answer_users'
    ),
    
    path(
        "survey/<int:survey_id>/export-csv/",
        views.export_survey_results_csv,
        name="export_survey_results_csv",
    ),    
    
    path("jobs/", views.hr_job_list, name="hr_job_list"),
    path("jobs/create/", views.job_post, name="job_post"),
    path("jobs/<int:job_id>/applicants/", views.job_applicants, name="job_applicants"),
    path("apply/<int:job_id>/", views.job_apply, name="job_apply"),   

    path("recognition/", views.Reg_view, name="recognition_poster"),  
    path("recognition/create/",views.recognition_create,name="recognition_create"),  
    path("recognition_list/",views.recognition_list,name="recognition_list"),    
    
    path(
        "recognition/<int:pk>/edit/",
        views.recognition_edit,
        name="recognition_edit"
    ),
    
    path(
        "recognition/<int:pk>/delete/",
        views.recognition_delete,
        name="recognition_delete"
    ),    
    
    
]
