from django_filters.rest_framework import FilterSet

from .models import Client, Task


class ClientFilter(FilterSet):

    class Meta:
        model = Client
        fields = ['position']


class TaskFilter(FilterSet):

    class Meta:
        model = Task
        fields = ['title']
