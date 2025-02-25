from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.Profile.as_view(), name='profile'),
    path("user_statistics/", views.StatisticsProfile.as_view(), name='statistics'),
    path("edit_profile/", views.EditProfile.as_view(), name='edit_profile'),
    path('edit_password/', auth_views.PasswordChangeView.as_view(
        template_name='profile_user/change_password.html',
        success_url='change-done/'), name='edit_password'),
    path('edit_password/change-done/', views.ChangeDone.as_view(), name="change-done"),
]

