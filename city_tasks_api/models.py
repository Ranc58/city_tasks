from django.db import models
from django.utils.translation import ugettext_lazy as _


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Customer'))
    position = models.CharField(max_length=100, verbose_name=_('Present position'))
    city = models.CharField(max_length=100, verbose_name=_('City'))

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Task title'))
    description = models.TextField(verbose_name=_('Task description'))
    performer_client = models.ManyToManyField(Client)
    controller_client = models.ForeignKey(Client, on_delete=models.DO_NOTHING) #todo change on_delete

    def __str__(self):
        return self.title
