from typing import Any

from django.views.generic import TemplateView, UpdateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from auth_user.models import User
from tasks.utils import DataMixin
from tasks.models import TaskStatistics
from .forms import EditProfileForm


class Profile(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = "profile_user/profile.html"
    page_title = "Профіль"


class StatisticsProfile(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = "profile_user/statistics.html"
    page_title = "Статистика"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["statics"] = TaskStatistics.objects.filter(user=self.request.user)
        return context


class EditProfile(LoginRequiredMixin, DataMixin, UpdateView):
    model = User
    template_name = "profile_user/edit_profile.html"
    form_class = EditProfileForm
    success_url = reverse_lazy("profile")
    page_title = "Редагувати профіль"

    def get_object(self, queryset=None):
        return self.request.user


class ChangeDone(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = "profile_user/change_done_password.html"
    page_title = "Пароль змінено"


class HomeRedirect(LoginRequiredMixin, DataMixin, RedirectView):
    url = reverse_lazy("home")
