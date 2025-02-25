from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Task, TaskStatistics


@receiver(post_delete, sender=Task)
def update_statistics_after_delete(sender, instance, **kwargs):
    if hasattr(instance.user, "statistics"):
        instance.user.statistics.update_statistics()
