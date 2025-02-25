import random
from typing import Any

from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import LoginForm, RegisterForm
from .models import Quit


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = "auth_user/login.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        quotes = Quit.objects.all()
        if quotes:
            context["quote"] = random.choice(quotes)
        else:
            context["quote"] = None

        context["form"] = self.get_form()
        context["page_title"] = "Вхід"
        
        return context


class LogoutUser(LogoutView):
    next_page = "/"


class RegisterUser(CreateView):
    form_class = RegisterForm
    template_name = "auth_user/register.html"
    success_url = reverse_lazy("auth_user:login")

    def form_valid(self, form):
        response = super().form_valid(form)  
        messages.success(self.request, "Ви успішно зареєструвалися! Тепер можете увійти в систему.")  
        return redirect(self.success_url)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        quotes = Quit.objects.all()

        context["quote"] = random.choice(quotes) if quotes else None
        context["form"] = self.get_form()
        context["page_title"] = "Реєстрація"
        
        return context
