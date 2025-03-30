from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
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

        if User.objects.filter(email=email).exists():
            messages.error(request, "User already exists. Please log in.")
            return redirect("login")  # ✅ Redirect to login if user exists

        # ✅ Create user without password (password will be set in reset-password)
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email)
        request.session["user_id"] = user.id  # ✅ Store user ID for password setup

        return redirect("reset-password")  # ✅ Redirect to set password

    return render(request, "user_auth/signup.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        print(f"DEBUG: Attempting login for {email} with password {password}")
        
        user = authenticate(request, username=email, password=password)

        if user is not None:
            print(f"DEBUG: Authentication successful for {email}")
            login(request, user)
            return redirect("dashboard")  # or redirect wherever you need
        else:
            print(f"DEBUG: Authentication failed for {email}")
            messages.error(request, "Invalid login credentials")
            return redirect("login")
    return render(request, "user_auth/login.html")




def password_reset(request):
    """
    This view handles password reset after signup.
    Users are redirected here after signing up to set their password.
    """
    if request.method == "POST":
        user_id = request.session.get("user_id")

        if not user_id:
            messages.error(request, "Session expired. Please sign up again.")
            return redirect("signup")  # ✅ Redirect to signup if session expires

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, "User not found. Please sign up again.")
            return redirect("signup")  # ✅ Redirect to signup if user not found

        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            request.session["password_reset_failed"] = True  # ✅ Store error in session
            return redirect("update-pw-error")  # ✅ Redirect to error page

        user.set_password(new_password)
        user.save()
        login(request, user)  # ✅ Log in user after password reset

        return redirect("dashboard")  # ✅ Redirect to Dashboard

    return render(request, "user_auth/reset_password.html")


def update_pw_error(request):
    user_id = request.session.get("user_id")

    if not user_id:
        messages.error(request, "Session expired. Please sign up again.")
        return redirect("signup")

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect("update-pw-error")

        try:
            user = User.objects.get(id=user_id)

            user.set_password(password1)
            user.save()
            request.session.flush()
            messages.success(request, "Password updated successfully! Please log in.")
            return redirect("login")

        except User.DoesNotExist:
            messages.error(request, "User not found. Please sign up again.")
            return redirect("signup")

    return render(request, "user_auth/update_pw_error.html")




def forgot_password(request):
    """
    This view handles 'Forgot Password' functionality.
    Users will enter their email and receive an OTP to reset their password.
    """
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            request.session["reset_email"] = email  # ✅ Store email in session
            return redirect("reset-password")  # ✅ Redirect to reset-password form
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect("forgot-password")  # ✅ Stay on forgot-password page

    return render(request, "user_auth/forgot_password.html")


def dashboard(request):
    return render(request, "user_auth/dashboard.html")

