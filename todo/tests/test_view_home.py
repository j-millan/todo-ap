from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse, resolve
from ..forms import TodoItemForm
from ..models import TodoItem
from ..views import HomeView
from .cases import BaseTestCase

class HomeViewLoginRequiredTests(BaseTestCase):
	def setUp(self):
		super().setUp(reverse('home'))
		self.response = self.client.get(self.url)

	def test_redirection(self):
		login_url = reverse('login')
		self.assertRedirects(self.response, f'{login_url}?next={self.url}')

class HomeViewTests(BaseTestCase):
	def setUp(self):
		super().setUp(reverse('home'))
		self.client.login(username=self.username, password=self.password)
		self.response = self.client.get(self.url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve('/')
		self.assertEquals(view.func.view_class, HomeView)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, TodoItemForm)

	def test_form_inputs(self):
		self.assertContains(self.response, '<input', 2)
		self.assertContains(self.response, 'type="text"', 1)

class SuccessfulItemCreationTests(BaseTestCase):
	def setUp(self):
		super().setUp(reverse('home'))
		self.client.login(username=self.username, password=self.password)
		data = {
			'task': 'Finish my homework'
		}
		self.response = self.client.post(self.url, data)

	def test_redirection(self):
		self.assertEquals(self.response.status_code, 200)

	def test_item_creation(self):
		self.assertTrue(TodoItem.objects.exists())

	def test_item_display(self):
		self.assertContains(self.response, TodoItem.objects.first().get_truncated_task())

class InvalidItemCreationTests(BaseTestCase):
	def setUp(self):
		super().setUp(reverse('home'))
		self.client.login(username=self.username, password=self.password)
		self.response = self.client.post(self.url, {})

	def test_redirection(self):
		self.assertEquals(self.response.status_code, 200)

	def test_item_creation(self):
		self.assertFalse(TodoItem.objects.exists())

	def test_form_errors(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)