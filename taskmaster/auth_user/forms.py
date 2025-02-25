from typing import Any

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логін або Email", max_length=30)
    password = forms.CharField(
        label="Пароль", max_length=30, widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ["username", "password"]


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="Логін", max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Підтвердьте пароль")

    class Meta:
        model = User
        fields = ["email", "username", "password", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        password = cleaned_data["password"]
        password2 = cleaned_data["password2"]

        if not len(password) >= 8:
            raise forms.ValidationError("* Пароль повинен містити мінімум 8 символів")

        if not any(char in "1234567890" for char in password):
            raise forms.ValidationError("* Пароль повинен містити хоча б 1 цифру")

        special_characters = "!#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
        if not any(char in special_characters for char in password):
            raise forms.ValidationError(
                "* Пароль повинен містити хоча б один спец. символ"
            )

        if password != password2:
            raise forms.ValidationError("* Паролі не збігаються")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("* Даний Email вже зареєстрований")
        return email
