import random

import factory
from .models import Task, Client, PerformControl


class ClientFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('first_name')
    city = factory.Faker('city')
    position = factory.Faker('job')

    class Meta:
        model = Client


class TaskFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('word')
    description = factory.Faker('sentence')

    class Meta:
        model = Task


class PerformControlFactory(factory.django.DjangoModelFactory):

    task = factory.SubFactory(TaskFactory)
    performer = factory.SubFactory(ClientFactory)
    controller = factory.SubFactory(ClientFactory)

    class Meta:
        model = PerformControl
