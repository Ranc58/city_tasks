from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import Task, Client
from .serializers import ClientSerializer, ClientTaskSerializer
from .factories import ClientFactory, TaskFactory


class TestClientsHandler(APITestCase):

    def test_get_clients_list(self):
        client_created = ClientFactory()
        url = reverse('client-list')
        response = self.client.get(url)
        data = response.json()
        client = Client.objects.filter(pk=client_created.pk)
        expected_result = ClientSerializer(client, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data, expected_result.data)

    def test_get_clients_by_position(self):
        ClientFactory(
            position='test_position'
        )
        ClientFactory(
            position='test_position'
        )
        ClientFactory()
        url = reverse('client-list')
        response = self.client.get(url, {'position': 'test_position'})
        clients = Client.objects.filter(position='test_position')
        expected_result = ClientSerializer(clients, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_result.data)

    def test_post_client(self):
        url = reverse('client-list')
        data = {
            'name': 'test_name',
            'city': 'test_city',
            'position': 'test_position',
        }
        response = self.client.post(url, data=data)
        expected_client = ClientSerializer(Client.objects.get(name=data.get('name')))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), expected_client.data)

    def test_get_client_detail(self):
        client = ClientFactory()
        url = reverse('client-detail', kwargs=dict(pk=client.pk))
        response = self.client.get(url)
        client_data = ClientSerializer(client)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), client_data.data)

    def test_put_client(self):
        client = ClientFactory()
        url = reverse('client-detail', kwargs=dict(pk=client.pk))
        data = {
            'name': 'test_name',
            'city': 'test_city',
            'position': 'test_position',
        }
        response = self.client.put(url, data=data)
        updated_client = Client.objects.get(pk=client.pk)
        expected_client = ClientSerializer(updated_client)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_client.data)

    def test_patch_client(self):
        client = ClientFactory()
        url = reverse('client-detail', kwargs=dict(pk=client.pk))
        data = {
            'position': 'test_position',
        }
        response = self.client.patch(url, data=data)
        client = Client.objects.get(pk=client.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['position'], client.position)

    def test_delete_client(self):
        client = ClientFactory()
        url = reverse('client-detail', kwargs=dict(pk=client.pk))
        response = self.client.delete(url)
        client_exist = Client.objects.filter(pk=client.pk).exists()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(client_exist)

    def test_get_client_tasks(self):
        client_performer = ClientFactory()
        client_controller = ClientFactory()
        task = TaskFactory()
        task.performer_client.set((client_performer, ))
        task.controller_client.set((client_controller, ))
        url = reverse('client-tasks', kwargs=dict(pk=client_performer.pk))
        response = self.client.get(url)
        expected_result = ClientTaskSerializer(Task.objects.filter(pk=task.pk), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_result.data)

