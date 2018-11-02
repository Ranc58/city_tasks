from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters


from .models import Client, Task
from .serializers import ClientSerializer, TaskSerializer, ClientTaskSerializer
from .filters import ClientFilter


class ClientsViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ClientFilter
    lookup_field = 'pk'

    def get_queryset(self):
        return Client.objects.prefetch_related(
            'performer_in_tasks',
            'controller_in_tasks'
        ).all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        return obj

    @action(detail=True)
    def tasks(self, request, pk=None):
        client = self.get_object()
        if not client:
            return Response([])
        tasks = Task.objects.prefetch_related('controller_client').filter(performer_client=client)
        serializer = ClientTaskSerializer(data=tasks, many=True)
        serializer.is_valid()
        return Response(serializer.data)


class TasksViewSet(viewsets.ViewSet):
    pass

