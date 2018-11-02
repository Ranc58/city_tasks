import factory
from .models import Task, Client


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
