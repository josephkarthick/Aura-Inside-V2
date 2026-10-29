from django.urls import path,include
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from .views import login_view, logout_view, custom_password_change,login_required_page,access_warning
from .views import CustomPasswordResetView

app_name = 'Accounts' 

urlpatterns = [
    # --- Auth Core ---
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path("access-warning/", access_warning, name="access_warning"),    
    path('change_password/', custom_password_change, name='change_password'),
    path('login-required/', login_required_page, name='login_required_page'),
    

    # --- Password Reset Flow ---
    path(
        'password-reset/',
        CustomPasswordResetView.as_view(),
        name='password_reset'
    ),
    
    path(
        'password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='Accounts/password_reset_done.html'), 
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='Accounts/password_reset_confirm.html',
            success_url=reverse_lazy('Accounts:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    
    path(
        'reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='Accounts/password_reset_complete.html'), 
        name='password_reset_complete'
    ),
]

