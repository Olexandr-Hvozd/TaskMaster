from typing import Any

from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from .utils import DataMixin
from .models import Task
from .forms import AddTaskForm, DueDateUpdateForm


class TaskHome(LoginRequiredMixin, DataMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    page_title = "Завдання"

    def get_queryset(self):
        task = Task.objects.filter(user=self.request.user)
        Task.update_overdue_tasks()
        filter_type = self.request.GET.get("filter", "in_progress")

        if filter_type == "all":
            filter_type = None
        if filter_type == "in_progress":
            task = task.filter(status="in_progress")
        if filter_type == "completed":
            task = task.filter(status="completed")
        if filter_type == "overdue":
            task = task.filter(status="overdue")

        filter_priority = self.request.GET.get("priority")
        if filter_priority:
            priority_maping = {
                "low": "Низька",
                "medium": "Середня",
                "high": "Висока",
                "very_high": "Дуже висока",
            }
            priority_value = priority_maping.get(filter_priority)
            if priority_value:
                task = task.filter(priority=priority_value)

        return task


class TaskDetail(LoginRequiredMixin, DataMixin, DetailView):
    model = Task
    template_name = "tasks/task_details.html"
    context_object_name = "task"
    pk_url_kwarg = "task_id"
    page_title = "Деталі завдання"


class AddTask(LoginRequiredMixin, DataMixin, CreateView):
    model = Task
    template_name = "tasks/add_task.html"
    form_class = AddTaskForm
    success_url = reverse_lazy("home")
    page_title = "Додати завдання"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditTask(LoginRequiredMixin, DataMixin, UpdateView):
    model = Task
    template_name = "tasks/edit_task.html"
    form_class = AddTaskForm
    success_url = reverse_lazy("home")
    pk_url_kwarg = "task_id"
    page_title = "Редагувати завдання"


class DeleteTask(LoginRequiredMixin, DataMixin, DeleteView):
    model = Task
    template_name = "tasks/delete_task.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "task_id"
    page_title = "Видалити завдання"


class DoneTask(LoginRequiredMixin, View):
    def post(self, request, task_id):
        done_task = get_object_or_404(Task, id=task_id)

        if done_task.user == request.user:
            done_task.status = "completed"
            done_task.save()
        return redirect("home")


class ActiveTask(LoginRequiredMixin, DataMixin, UpdateView):
    model = Task
    template_name = "tasks/edit_duedate.html"
    form_class = DueDateUpdateForm
    success_url = reverse_lazy("home")
    pk_url_kwarg = "task_id"
    page_title = "Оновлення кінцевої дати виконня"

    def form_valid(self, form):
        form.instance.status = "in_progress"
        return super().form_valid(form)
