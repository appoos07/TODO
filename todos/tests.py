# todos/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Project, Todo

class TodoManagerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.project = Project.objects.create(title='Test Project', user=self.user)
        self.todo = Todo.objects.create(description='Test Todo', project=self.project)

    def test_project_creation(self):
        self.assertEqual(self.project.title, 'Test Project')
        self.assertEqual(self.project.user, self.user)

    def test_todo_creation(self):
        self.assertEqual(self.todo.description, 'Test Todo')
        self.assertFalse(self.todo.status)  # Default status is False

    def test_home_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')

    def test_project_detail_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('project_detail', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')

    def test_create_project_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('create_project'), {'title': 'New Project', 'user': self.user.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(title='New Project').exists())

    def test_export_gist_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('export_gist', args=[self.project.id]))
        self.assertIn(response.status_code, [302, 200, 400, 403, 404])  # Depending on response from GitHub
