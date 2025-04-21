from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
import random
from django.core.mail import send_mail
from .models import AdRequest
from .forms import AdRequestForm
import logging
import os
from django.conf import settings 
import subprocess

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
            return redirect("sign_in_error")
            
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
            return redirect("signup")  # Redirect to signup if session expires

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, "User not found. Please sign up again.")
            return redirect("signup")  # Redirect to signup if user not found

        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            request.session["password_reset_failed"] = True  
            return redirect("update-pw-error")  # Redirect to error page

        # Reset Password
        user.set_password(new_password)
        user.save()

        # Explicitly set authentication backend if multiple backends exist
        user.backend = "django.contrib.auth.backends.ModelBackend"

        # Log in user after password reset
        login(request, user, backend=user.backend)

        return redirect("login")  # Redirect to login instead of signup

    return render(request, "user_auth/reset_password.html")


def update_pw_error(request):
    """
    This view handles the password reset when users enter mismatched passwords.
    It allows them to retry without restarting the process.
    """
    user_id = request.session.get("user_id") 

    if not user_id:
        messages.error(request, "Session expired. Please request a new OTP.")
        return redirect("forgot-password")  

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect("update-pw-error")  

        try:
            user = User.objects.get(id=user_id)

            # Reset Password
            user.set_password(password1)
            user.save()

            # Do NOT flush session immediately (retain messages)
            messages.success(request, "Password updated successfully! Please log in.")
            
            return redirect("login")  # Redirect to login page instead of signup

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
            otp = random.randint(100000, 999999)
            request.session["otp"] = otp
            request.session["reset_email"] = email  

            subject = "🔐 Reset Your Password - ADvantage"
            message = f"""
                Dear {user.first_name},

                We received a request to reset your password for your ADvantage account. 
                Please use the One-Time Password (OTP) below to proceed:

                🔢 YOUR OTP: {otp} 

                This OTP is valid for the next 10 minutes. If you did not request a password reset, 
                please ignore this email, and your account will remain secure.

                About ADvantage:  
                ADvantage is an AI-powered ad generation platform that helps businesses create 
                engaging and personalized advertisements using the latest trends and data.  

                If you have any questions, feel free to reach out to our support team.

                Best regards,  
                The ADvantage Team  
                advantage.bluemelon@gmail.com  
            """


            send_mail(
                subject,
                message,
                "advantage.bluemelon@gmail.com",  # Your sender email
                [email],
                fail_silently=False,
            )

            return redirect("forgotpw-otp")  # ✅ Redirect to reset-password form
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect("forgotpw-email-error")  

    return render(request, "user_auth/forgot_password.html")


def forgotpw_emailerror(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)
            request.session["otp"] = otp
            request.session["reset_email"] = email  

            print(f"DEBUG: Email found, OTP {otp} stored for {email}")  # ✅ Check if session is stored

            subject = "🔐 Reset Your Password - ADvantage"
            message = f"""
                Dear {user.first_name},

                We received a request to reset your password for your ADvantage account. 
                Please use the One-Time Password (OTP) below to proceed:

                🔢 YOUR OTP: {otp} 

                This OTP is valid for the next 10 minutes. If you did not request a password reset, 
                please ignore this email, and your account will remain secure.

                About ADvantage:  
                ADvantage is an AI-powered ad generation platform that helps businesses create 
                engaging and personalized advertisements using the latest trends and data.  

                If you have any questions, feel free to reach out to our support team.

                Best regards,  
                The ADvantage Team  
                advantage.bluemelon@gmail.com  
            """

            send_mail(
                subject,
                message,
                "advantage.bluemelon@gmail.com",  
                [email],
                fail_silently=False,
            )

            print("DEBUG: Email sent successfully")  # ✅ Check if email is sent

            return redirect("forgotpw-otp")  # ✅ Redirect to OTP page

        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            print("DEBUG: No account found for email")  # ✅ Debug missing user
            return render(request, "user_auth/forgotpw_emailerror.html")  

    return render(request, "user_auth/forgotpw_emailerror.html")




def forgotpw_otp(request):
    if request.method == "POST":
        otp_entered = ''.join([request.POST.get(f"otp{i}") for i in range(1, 7)])
        stored_otp = str(request.session.get("otp"))
        email = request.session.get("reset_email")  

        if otp_entered == stored_otp:
            try:
                user = User.objects.get(email=email)
                request.session["user_id"] = user.id  # ✅ Store user ID in session
                return redirect("reset-password")  # ✅ Redirect to password reset page
            except User.DoesNotExist:
                messages.error(request, "User not found. Please sign up again.")
                return redirect("signup")

        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("otp-error")  

    return render(request, "user_auth/forgotpw_otp.html")


def otp_error(request):
    if request.method == "POST":
        otp_entered = ''.join([request.POST.get(f"otp{i}") for i in range(1, 7)])
        stored_otp = str(request.session.get("otp"))
        email = request.session.get("reset_email")  

        if otp_entered == stored_otp:
            try:
                user = User.objects.get(email=email)
                request.session["user_id"] = user.id  # ✅ Store user ID in session
                return redirect("reset-password")  # ✅ Redirect to password reset
            except User.DoesNotExist:
                messages.error(request, "User not found. Please sign up again.")
                return redirect("signup")
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("otp-error")  # ✅ Stay on the same page if incorrect

    return render(request, "user_auth/otp_error.html")




def resend_otp(request):
    """
    Resends OTP without requiring the user to re-enter their email.
    """
    email = request.session.get("reset_email")

    if not email:
        return redirect("forgot-password")  # Redirect if session expired

    try:
        user = User.objects.get(email=email)
        otp = random.randint(100000, 999999)
        request.session["otp"] = otp  # Store new OTP

        subject = "🔐 New OTP for Password Reset - ADvantage"
        message = f"""
                Dear {user.first_name},

                We received a request to reset your password for your ADvantage account. 
                Please use the One-Time Password (OTP) below to proceed:

                🔢 YOUR OTP: {otp} 

                This OTP is valid for the next 10 minutes. If you did not request a password reset, 
                please ignore this email, and your account will remain secure.

                About ADvantage:  
                ADvantage is an AI-powered ad generation platform that helps businesses create 
                engaging and personalized advertisements using the latest trends and data.  

                If you have any questions, feel free to reach out to our support team.

                Best regards,  
                The ADvantage Team  
                advantage.bluemelon@gmail.com  
            """

        send_mail(
            subject,
            message,
            "advantage.bluemelon@gmail.com",  
            [email],
            fail_silently=False,
        )

    except User.DoesNotExist:
        return redirect("forgot-password")  

    return redirect("forgotpw-otp")


def sign_in_error(request):
    if request.method == 'POST':
        # Access the email and password directly from the POST data
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard after login
        else:
            # If authentication fails, show an error message
            messages.error(request, "The email address and password you entered do not match our records. Please try again.")
    
    return render(request, 'user_auth/sign_in_error.html')


def dashboard(request):
    return render(request, "user_auth/dashboard.html")


def mainpage(request):
    if request.method == "POST":
        form = AdRequestForm(request.POST, request.FILES)
        if form.is_valid():
            # Save form data to DB
            ad_request = form.save()

            # Prepare data to pass to ad_generator.py
            product_name = ad_request.product
            description = ad_request.description

            # Path to the script
            script_path = os.path.join(settings.BASE_DIR, 'AD_gen', 'ad_generator.py')

            # Call the script via subprocess (pass the arguments to the script)
            command = ['python', script_path, product_name, description]
            result = subprocess.run(command, capture_output=True, text=True)

            # Return the result (if successful, capture stdout; otherwise capture stderr)
            if result.returncode == 0:
                output = result.stdout.strip()  # Remove any extra spaces/newlines
            else:
                output = f"Error: {result.stderr.strip()}"

            # Pass the result to the template
            return render(request, "user_auth/mainpage1.html", {
                "form": form, 
                "result": output,
                "campaign": ad_request  # Pass the ad request for display
            })
    else:
        form = AdRequestForm()

    return render(request, "user_auth/mainpage.html", {"form": form})


# View for generate_campaign (this is another page where the user can generate an ad)
def generate_campaign(request):
    if request.method == 'POST':
        form = AdRequestForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to the database
            ad_request = form.save()

            # Get input data from the form
            product_name = ad_request.product
            product_description = ad_request.description

            # Path to your ad_generator.py
            script_path = os.path.join(settings.BASE_DIR, 'AD_gen', 'ad_generator.py')

            # Call the ad_generator.py script via subprocess
            command = ['python', script_path, product_name, product_description]
            result = subprocess.run(command, capture_output=True, text=True)

            # Updated parsing logic
            if result.returncode == 0:
                raw_lines = result.stdout.strip().split('\n')
                ads = []

                for line in raw_lines:
                    line = line.strip()
                    if line:
                        ads.append({'trend': None, 'ad_content': line})  # Treat each line as ad

                return render(request, 'user_auth/mainpage1.html', {'form': form, 'result': ads})
            else:
                error_output = result.stderr
                return render(request, 'user_auth/mainpage1.html', {'form': form, 'result': [], 'error': error_output})
