from rest_framework import serializers

from .models import Client, Task


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'position',
            'city',
        )


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
        )


class ClientTaskSerializer(serializers.ModelSerializer):
    controllers = ClientSerializer(source='controller_client', many=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'controllers',
        )
