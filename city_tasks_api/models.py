from django.db import models
from django.utils.translation import ugettext_lazy as _


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Client'))
    position = models.CharField(max_length=100, verbose_name=_('Present position'))
    city = models.CharField(max_length=100, verbose_name=_('City'))

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Task title'))
    description = models.TextField(verbose_name=_('Task description'))
    performer_client = models.ManyToManyField(
        Client,
        verbose_name=_('Performer'),
        related_name='performer_in_tasks'
    )
    controller_client = models.ManyToManyField(
        Client,
        verbose_name=_('Controller'),
        related_name='controller_in_tasks'
    )

    def __str__(self):
        return self.title
