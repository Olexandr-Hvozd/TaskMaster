from django import forms

from auth_user.models import User


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
