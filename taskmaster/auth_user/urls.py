from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views


app_name = "auth_user"
urlpatterns = [
    path("", views.LoginUser.as_view(), name="login"),
    path("logout/", views.LogoutUser.as_view(), name="logout"),
    path("register/", views.RegisterUser.as_view(), name="register"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="auth_user/password_reset.html",
            success_url=reverse_lazy("auth_user:password_reset_done"),
            email_template_name="auth_user/password_reset_email.html",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth_user/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth_user/password_reset_confirm.html",
            success_url=reverse_lazy("auth_user:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth_user/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
