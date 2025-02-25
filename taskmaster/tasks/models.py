from venv import logger

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from auth_user.models import User


def validate_due_date(value):
    if value < now().date():
        raise ValidationError("Дата виконання не може бути в минулому.")


class Task(models.Model):
    STATUS_CHOICES = [
        ("in_progress", _("В процесі")),
        ("completed", _("Завершене")),
        ("overdue", _("Прострочене")),
    ]

    PRIORITY_CHOICES = [
        ("Низька", _("Низька")),
        ("Середня", _("Середня")),
        ("Висока", _("Висока")),
        ("Дуже висока", _("Дуже висока")),
    ]

    title = models.CharField(max_length=30, verbose_name="Назва")
    description = models.TextField(blank=True, verbose_name="Опис", max_length=300)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks", verbose_name="Користувач"
    )
    due_date = models.DateField(
        validators=[validate_due_date], verbose_name="Кінцева дата виконання"
    )
    priority = models.CharField(
        max_length=12,
        choices=PRIORITY_CHOICES,
        default="Середня",
        verbose_name="Важливість",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="in_progress",
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата останнього оновлення"
    )

    class Meta:
        verbose_name = "Завдання"
        verbose_name_plural = "Завдання"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not hasattr(self.user, "statistics"):
            TaskStatistics.objects.create(user=self.user)

        if self.user.statistics:
            self.user.statistics.update_statistics()

        if self.status == "completed":
            CompletedTask.objects.get_or_create(task=self)
        elif self.status == "overdue":
            OverdueTask.objects.get_or_create(task=self)

    @staticmethod
    def update_overdue_tasks():
        today = now().date()
        overdue_tasks = Task.objects.filter(due_date__lt=today, status="in_progress")
        for task in overdue_tasks:
            task.status = "overdue"
            task.save()

    def get_status_display_ua(self):
        translations = {
            "in_progress": "Активне",
            "completed": "Виконано",
            "overdue": "Прострочено",
        }
        return translations.get(self.status, self.status)

    def __str__(self):
        return self.title


class TaskStatistics(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="statistics",
        verbose_name="Користувач",
    )
    total_tasks = models.PositiveIntegerField(default=0, verbose_name="Всього завдань")
    completed_tasks = models.PositiveIntegerField(default=0, verbose_name="Виконано")
    overdue_tasks = models.PositiveIntegerField(default=0, verbose_name="Просрочено")
    active_tasks = models.PositiveIntegerField(default=0, verbose_name="Активні")

    class Meta:
        verbose_name = "Статистику"
        verbose_name_plural = "Статистика"

    def update_statistics(self):
        tasks = self.user.tasks.all()
        self.total_tasks = tasks.count()
        self.completed_tasks = tasks.filter(status="completed").count()
        self.overdue_tasks = tasks.filter(status="overdue").count()
        self.active_tasks = tasks.filter(status="in_progress").count()

        logger.debug(
            f"Оновлення статистики для {self.user.username}: {self.total_tasks} завдань"
        )
        print(
            f"Оновлення статистики: {self.user.username} -> {self.completed_tasks} виконано, {self.overdue_tasks} прострочено, {self.active_tasks} активні"
        )

        self.save()

    def __str__(self):
        return f"Статистика для {self.user.username}"


class CompletedTask(models.Model):
    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        related_name="completed_task",
        verbose_name="Завдання",
    )
    completed_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата виконання"
    )

    class Meta:
        verbose_name = "Виконане завдання"
        verbose_name_plural = "Виконані завдання"

    def __str__(self):
        return f"Виконане завдання: {self.task.title}"


class OverdueTask(models.Model):
    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        related_name="overdue_task",
        verbose_name="Завдання",
    )
    overdue_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата пророчення")

    class Meta:
        verbose_name = "Просрочене завдання"
        verbose_name_plural = "Просрочені завдання"

    def __str__(self):
        return f"Прострочене завдання: {self.task.title}"
