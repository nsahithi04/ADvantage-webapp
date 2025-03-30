from django.urls import path
from .views import signup, login_view, password_reset, forgot_password, update_pw_error, dashboard

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login_view, name="login"),
    path("reset-password/", password_reset, name="reset-password"),
    path("forgot-password/", forgot_password, name="forgot-password"),  # ✅ Check this name
    path("update-password-error/", update_pw_error, name="update-pw-error"),
    path("dashboard/", dashboard, name="dashboard"),
]
