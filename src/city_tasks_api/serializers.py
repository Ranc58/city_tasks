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


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
        )


class ClientTaskSerializer(serializers.ModelSerializer):
    controllers = ClientSerializer(source='controller', many=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'description',
            'controllers',
        )


class CheckSerializer(serializers.Serializer):
    performer = serializers.IntegerField(required=True)
    controller = serializers.IntegerField(required=True)
    remove = serializers.BooleanField(required=False)

    def validate_performer(self, value):
        if not Client.objects.filter(id=value).exists():
            raise serializers.ValidationError("Not found performer")
        return value

    def validate_controller(self, value):
        if not Client.objects.filter(id=value).exists():
            raise serializers.ValidationError("Not found controller")
        return value


class ControllerSettingSerializer(serializers.Serializer):
    task = serializers.IntegerField(required=True)
    controller = serializers.IntegerField(required=True)

    def validate_task(self, value):
        if not Task.objects.filter(id=value).exists():
            raise serializers.ValidationError("Not found task")
        return value

    def validate_controller(self, value):
        if not Client.objects.filter(id=value).exists():
            raise serializers.ValidationError("Not found client")
        return value


class PerformerSettingSerializer(serializers.Serializer):
    to_perform = serializers.IntegerField(required=False)
    to_remove = serializers.IntegerField(required=False)

    def validate_to_perform(self, value):
        if not Client.objects.filter(id=value).exists():
            raise serializers.ValidationError("Not found client")
        return value

    def validate_to_remove(self, value):
        if not Client.objects.filter(id=value).exists():
            raise serializers.ValidationError("Not found client")
        return value
