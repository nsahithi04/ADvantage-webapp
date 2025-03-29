from django.urls import path
from user_auth import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),  
    path("create-account/", views.create_account, name="createacc"),
    path("reset-password/", views.password_reset, name="reset-password"),
    path("update-pw-error/", views.update_pw_error, name="update-pw-error"), 
    path("dashboard/", views.dashboard, name="dashboard"),
]
