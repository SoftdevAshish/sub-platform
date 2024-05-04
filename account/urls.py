from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name=""),
    path("register", views.register, name="register"),
    path("login", views.logins, name="login"),
    path("logout", views.logouts, name="logout"),
    #     Password Management
    #     1 - allow us to enter our email in order to receive a password reset link
    path(
        "reset_password",
        auth_views.PasswordResetView.as_view(
            template_name="account/password-reset.html"
        ),
        name="reset_password",
    ),
    #      2 - show a success message stating an email was sent to reset out password.
    path(
        "reset_password_sent",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password-reset-sent.html"
        ),
        name="password_reset_done",
    ),
    #     3 - Send a link to our email, so that we can reset our password + We will prompt to enter a new password.
    path(
        "reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password-reset-form.html"
        ),
        name="password_reset_confirm",
    ),
    # - 4 Show a success message stating that our password was changed
    path(
        "password_reset_complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
    #     Email Verification
    path("email-verification/<str:uidb64>/<str:token>/", views.email_verification, name="email-verification"),
    path(
        "email-verification-sent",
        views.email_verification_sent,
        name="email-verification-sent",
    ),
    path(
        "email-verification-success",
        views.email_verification_success,
        name="email-verification-success",
    ),
    path(
        "email-verification-failed",
        views.email_verification_failed,
        name="email-verification-failed",
    ),
]
