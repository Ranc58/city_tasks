from django.db import models
from django.utils.translation import ugettext_lazy as _


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Client'))
    position = models.CharField(max_length=100, verbose_name=_('Present position'))
    city = models.CharField(max_length=100, verbose_name=_('City'))


class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Task title'))
    description = models.TextField(verbose_name=_('Task description'))
    performer = models.ManyToManyField(Client, related_name='performer_in_tasks')
    controller = models.ManyToManyField(Client, related_name='controller_in_tasks')


class PerformControl(models.Model):
    task = models.ForeignKey(
        Task,
        related_name='perfomed_task',
        on_delete=models.CASCADE
    )
    performer = models.ForeignKey(
        Client,
        related_name='performer_from_control',
        on_delete=models.CASCADE
    )
    controller = models.ForeignKey(
        Client,
        related_name='controller_from_control',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('task', 'performer', 'controller')

    def save(self, *args, **kwargs):
        self.task.controller.add(self.controller)
        super().save(*args, **kwargs)
