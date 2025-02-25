from django import forms

from .models import Task


class AddTaskForm(forms.ModelForm):
    description = forms.CharField(
        label="Опис",
        max_length=300,
        widget=forms.Textarea(),
    )
    due_date = forms.DateField(
    label="Кінцева дата виконання",
    widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    
    priority = forms.ChoiceField(
        label="Важливість",
        choices=Task.PRIORITY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "priority"]


class DueDateUpdateForm(forms.ModelForm):
    due_date = forms.DateField(
        label="Кінцева дата виконання",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )

    class Meta:
        model = Task
        fields = ["due_date"]
