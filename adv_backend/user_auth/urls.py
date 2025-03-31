from django.urls import path
from .views import signup, login_view, password_reset, forgot_password, update_pw_error, dashboard, forgotpw_otp, sign_in_error, resend_otp, forgotpw_emailerror

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login_view, name="login"),
    path("reset-password/", password_reset, name="reset-password"),
    path("forgot-password/", forgot_password, name="forgot-password"),
    path("forgot-password/error/", forgotpw_emailerror, name="forgotpw-email-error"),
    path("forgotpw-otp/", forgotpw_otp, name="forgotpw-otp"),  
    path("resend_otp/", resend_otp, name="resend-otp"),
    path("update-password-error/", update_pw_error, name="update-pw-error"),
    path("dashboard/", dashboard, name="dashboard"),
    path('sign-in-error/', sign_in_error, name='sign_in_error'),
]
