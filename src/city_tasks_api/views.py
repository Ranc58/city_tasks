from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters


from .models import Client, Task, PerformControl
from .serializers import ClientSerializer, TaskSerializer, ClientTaskSerializer, \
    PerformerSettingSerializer, ControllerSettingSerializer
from .filters import ClientFilter, TaskFilter
from .schemas import ClientTasksSchema, TaskClientsSchema


class ClientsViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ClientFilter
    lookup_field = 'pk'
    schema = ClientTasksSchema()


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Client.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        return obj

    @action(detail=True)
    def tasks(self, request, **kwargs):
        client = self.get_object()
        if not client:
            return Response([])
        tasks = client.performer_in_tasks.all()
        serializer = ClientTaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @tasks.mapping.post
    def set_controller_to_task(self, request, **kwargs):
        client = self.get_object()
        data = request.data
        serializer = ControllerSettingSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        obj, created = PerformControl.objects.get_or_create(
            performer=client,
            task_id=serializer.data.get('task'),
            controller_id=serializer.data.get('controller'))

        response_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(data, status=response_status)


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = TaskFilter
    lookup_field = 'pk'
    schema = TaskClientsSchema()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        return obj

    @action(detail=True)
    def clients(self, request, **kwargs):
        task = self.get_object()
        if not task:
            return Response([])
        clients = task.performer.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    @clients.mapping.post
    def set_performer_to_task(self, request, **kwargs):
        task = self.get_object()
        if not task:
            return Response([])
        data = request.data
        serializer = PerformerSettingSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        to_perform = serializer.data.get('to_perform')
        to_remove = serializer.data.get('to_remove')
        if to_perform:
            task.performer.add(to_perform)
        if to_remove:
            task.performer.remove(to_remove)
        return Response(data)
