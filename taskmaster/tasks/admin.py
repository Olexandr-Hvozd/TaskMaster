from django.contrib import admin
from django.contrib import messages

from .models import Task, TaskStatistics, CompletedTask, OverdueTask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "user",
        "priority",
        "created_at",
        "due_date",
        "updated_at",
    )
    list_display_links = ("id", "title", "user")
    list_per_page = 15
    ordering = ["created_at"]
    actions = ["set_status1", "set_status2", "set_status3"]
    search_fields = ["title", "user__email"]
    list_filter = ["status", "due_date"]

    @admin.action(description="Позначити виконаним обрані завдання")
    def set_status1(self, request, queryset):
        count = 0
        for task in queryset:
            if hasattr(task, "overdue_task"):
                task.overdue_task.delete()
            task.status = "completed"
            task.save()
            count += 1
        self.message_user(request, f"Змінено {count} завдання (Позначено виконаними)")

    @admin.action(description="Позначити просроченим обрані завдання")
    def set_status2(self, request, queryset):
        count = 0
        for task in queryset:
            if hasattr(task, "completed_task"):
                task.completed_task.delete()

            task.status = "overdue"
            task.save()
            count += 1
        self.message_user(
            request,
            f"Змінено {count} записів (Позначено просроченими)",
            messages.WARNING,
        )

    @admin.action(description="Позначити активними обрані завдання")
    def set_status3(self, request, queryset):
        count = 0
        for task in queryset:
            if hasattr(task, "completed_task"):
                task.completed_task.delete()
            if hasattr(task, "overdue_task"):
                task.overdue_task.delete()

            task.status = "in_progress"
            task.save()
            count += 1
        self.message_user(request, f"Змінено {count} записів (Позначено активними)")


@admin.register(TaskStatistics)
class TaskStatisticsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "total_tasks",
        "completed_tasks",
        "overdue_tasks",
        "active_tasks",
    )
    list_per_page = 15
    search_fields = ["user__email"]


@admin.register(CompletedTask)
class CompletedTaskAdmin(admin.ModelAdmin):
    list_display = ("task", "completed_at")
    list_per_page = 15


@admin.register(OverdueTask)
class OverdueTaskAdmin(admin.ModelAdmin):
    list_display = ("task", "overdue_at")
    list_per_page = 15
