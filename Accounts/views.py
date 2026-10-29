from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.http import JsonResponse

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse, NoReverseMatch


User = get_user_model()

# views.py

from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy

User = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    template_name = 'Accounts/password_reset.html'
    email_template_name = 'Accounts/password_reset_email.html'
    subject_template_name = 'Accounts/password_reset_subject.txt'
    success_url = reverse_lazy('Accounts:password_reset_done')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            messages.error(request, "Please enter a valid email address associated with your account.")
            return self.form_invalid(self.get_form())
        return super().post(request, *args, **kwargs)



def login_required_page(request):
    return render(request, 'Accounts/login_required.html')


def login_view(request):
    # If already logged in
    if request.user.is_authenticated:
        return redirect("Intranet:home")

    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        username = request.POST.get("username", "").strip().lower()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome {user.first_name or user.username}!")

            if next_url:
                return redirect(next_url)

            # fallback to home page
            return redirect("Intranet:home")

        messages.error(request, "Invalid username or password.")

    return render(request, "Accounts/login.html", {"next": next_url})



def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("Intranet:home")

@login_required
def custom_password_change(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Get the currently logged-in user (using the custom user model)
        user = request.user

        # Check if old password is correct
        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return render(request, 'Accounts/password_change.html')

        # Check if the new password and confirm password match
        if new_password1 != new_password2:
            messages.error(request, "New password and confirmation password do not match.")
            return render(request, 'Accounts/password_change.html')

        # Set the new password and save the user
        user.set_password(new_password1)
        user.save()

        # Log the user out after successful password change
        logout(request)

        # Redirect to the login page with a success message
        messages.success(request, "Your password has been successfully changed. Please log in again.")
        return redirect('Accounts:login')

    return render(request, 'Accounts/password_change.html')

def access_warning(request):
    return render(request, "Accounts/access_warning.html")