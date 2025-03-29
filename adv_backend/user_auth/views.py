from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from user_auth.models import CustomUser 
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model

User = get_user_model()

def signup(request):
    if request.method == "POST":
        request.session.flush()  # ✅ Clear old session data before signup

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        if not email:
            return render(request, "user_auth/signup.html", {"error": "Email is required"})

        if CustomUser.objects.filter(email=email).exists():
            return redirect("login")  # ✅ Redirect to login if user exists

        user = CustomUser.objects.create(first_name=first_name, last_name=last_name, email=email)
        request.session["user_id"] = user.id  # ✅ Store user ID for password setup

        return redirect("reset-password")  # ✅ Redirect to set password

    return render(request, "user_auth/signup.html")



def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")  # Redirect to Dashboard
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "user_auth/login.html")


def password_reset(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        if not user_id:
            print("Session expired. Redirecting to signup...")
            return redirect("signup")  # ✅ If session expires, go back to signup

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            print("User not found. Redirecting to signup...")
            return redirect("signup")  # ✅ If user doesn't exist, go back to signup

        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            print("Passwords do not match. Redirecting to update_pw_error.html")
            return redirect("update-pw-error")  # ✅ Redirect to password error page

        user.set_password(new_password)  # ✅ Set new password securely
        user.save()
        login(request, user)  # ✅ Log in the user after setting the password

        print("Password updated successfully. Redirecting to dashboard...")
        return redirect("dashboard")  # ✅ Redirect to Dashboard

    return render(request, "user_auth/reset_password.html")


def update_pw_error(request):
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            user_id = request.session.get("user_id")  # ✅ Get user ID from session
            if not user_id:
                return redirect("signup")  # ✅ If session is lost, go back to signup

            user = CustomUser.objects.get(id=user_id)  # ✅ Fetch user by ID
            user.set_password(password1)  # ✅ Update password securely
            user.save()
            login(request, user)  # ✅ Log in after updating password
            return redirect("dashboard")  # ✅ Redirect to Dashboard

        else:
            return render(request, "user_auth/update_pw_error.html", {"error": "Passwords do not match"})

    return render(request, "user_auth/update_pw_error.html")


def create_account(request):
    return render(request, "user_auth/create_account.html")

def dashboard(request):
    return render(request, "user_auth/dashboard.html")

