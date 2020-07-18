from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse, resolve
from ..forms import TodoItemForm
from ..models import TodoItem
from ..views import home

class HomeViewTestCase(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='user', email='email@email.com', password="password")
		self.username = 'user'
		self.password = 'password'
		self.url = reverse('home')

class HomeViewLoginRequiredTests(HomeViewTestCase):
	def setUp(self):
		super().setUp()
		self.response = self.client.get(self.url)

	def test_redirection(self):
		login_url = reverse('login')
		self.assertRedirects(self.response, f'{login_url}?next={self.url}')

class HomeViewTests(HomeViewTestCase):
	def setUp(self):
		super().setUp()
		self.client.login(username=self.username, password=self.password)
		self.response = self.client.get(self.url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve('/')
		self.assertEquals(view.func, home)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, TodoItemForm)

	def test_form_inputs(self):
		self.assertContains(self.response, '<input', 2)
		self.assertContains(self.response, 'type="text"', 1)

class SuccessfulItemCreationTests(HomeViewTestCase):
	def setUp(self):
		super().setUp()
		self.client.login(username=self.username, password=self.password)
		data = {
			'goal': 'Finish my homework'
		}
		self.response = self.client.post(self.url, data)

	def test_redirection(self):
		self.assertEquals(self.response.status_code, 200)

	def test_item_creation(self):
		self.assertTrue(TodoItem.objects.exists())

	def test_item_display(self):
		self.assertContains(self.response, TodoItem.objects.first().get_truncated_goal())

class InvalidItemCreationTests(HomeViewTestCase):
	def setUp(self):
		super().setUp()
		self.client.login(username=self.username, password=self.password)
		self.response = self.client.post(self.url, {})

	def test_redirection(self):
		self.assertEquals(self.response.status_code, 200)

	def test_item_creation(self):
		self.assertFalse(TodoItem.objects.exists())

	def test_form_errors(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)