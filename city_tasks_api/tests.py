from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import Task, Client
from .serializers import ClientSerializer, ClientTaskSerializer, TaskSerializer
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
        performer = ClientFactory()
        controller = ClientFactory()
        task = TaskFactory()
        task.performer.add(performer)
        task.controller.add(controller)
        url = reverse('client-tasks', kwargs=dict(pk=performer.pk))
        response = self.client.get(url)
        tasks = Task.objects.filter(pk=task.pk)
        expected_result = ClientTaskSerializer(tasks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_result.data)
        self.assertEqual(len(response.json()[0]['controllers']), 1)


class TestTasksHandler(APITestCase):

    def test_get_tasks_list(self):
        task_created = TaskFactory()
        url = reverse('task-list')
        response = self.client.get(url)
        data = response.json()
        task = Task.objects.filter(pk=task_created.pk)
        expected_result = TaskSerializer(task, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data, expected_result.data)

    def test_get_tasks_by_title(self):
        TaskFactory(
            title='test_title'
        )
        TaskFactory(
            title='test_title'
        )
        TaskFactory()
        url = reverse('task-list')
        response = self.client.get(url, {'title': 'test_title'})
        tasks = Task.objects.filter(title='test_title')
        expected_result = TaskSerializer(tasks, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_result.data)

    def test_post_task(self):
        url = reverse('task-list')
        data = {
            'title': 'test_title',
            'description': 'test_description',
        }
        response = self.client.post(url, data=data)
        expected_client = TaskSerializer(Task.objects.get(title=data.get('title')))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), expected_client.data)

    def test_get_task_detail(self):
        task = TaskFactory()
        url = reverse('task-detail', kwargs=dict(pk=task.pk))
        response = self.client.get(url)
        task_data = TaskSerializer(task)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), task_data.data)

    def test_put_task(self):
        task = TaskFactory()
        url = reverse('task-detail', kwargs=dict(pk=task.pk))
        data = {
            'title': 'test_title',
            'description': 'test_description',
        }
        response = self.client.put(url, data=data)
        updated_task = Task.objects.get(pk=task.pk)
        expected_task = TaskSerializer(updated_task)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_task.data)

    def test_patch_task(self):
        task = TaskFactory()
        url = reverse('task-detail', kwargs=dict(pk=task.pk))
        data = {
            'title': 'test_title',
        }
        response = self.client.patch(url, data=data)
        patched_task = Task.objects.get(pk=task.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], patched_task.title)

    def test_delete_task(self):
        task = TaskFactory()
        url = reverse('task-detail', kwargs=dict(pk=task.pk))
        response = self.client.delete(url)
        task_exist = Client.objects.filter(pk=task.pk).exists()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(task_exist)

    def test_get_task_performers(self):
        task = TaskFactory()
        performer = ClientFactory()
        task.performer.add(performer)
        url = reverse('task-clients', kwargs=dict(pk=performer.pk))
        response = self.client.get(url)
        clients = task.performer.all()
        expected_result = ClientSerializer(clients, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_result.data)

    def test_add_performer_to_task(self):
        task = TaskFactory()
        performer = ClientFactory()
        url = reverse('task-clients', kwargs=dict(pk=performer.pk))
        data = {
            'to_perform': int(performer.pk)
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task.performer.first().pk, data['to_perform'])

    def test_remove_performer_from_task(self):

        performer = ClientFactory()
        task = TaskFactory()
        task.performer.add(performer)
        url = reverse('task-clients', kwargs=dict(pk=performer.pk))
        data = {
            'to_remove': int(performer.pk)
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(task.performer.all())
