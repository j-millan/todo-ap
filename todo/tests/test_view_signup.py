from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, resolve
from ..views import SignUpView

class SignUpViewTests(TestCase):
	def setUp(self):
		url = reverse('signup')
		self.response = self.client.get(url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve('/signup/')
		self.assertEquals(view.func.view_class, SignUpView)

	def test_contains_login_link(self):
		login_url = reverse('login')
		self.assertContains(self.response, f'href="{login_url}"')

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, UserCreationForm)

	def test_form_inputs(self):
		self.assertContains(self.response, '<input', 5)
		self.assertContains(self.response, 'type="text"', 1)
		self.assertContains(self.response, 'type="email"', 1)
		self.assertContains(self.response, 'type="password"', 2)

class SuccessfulSignUpTests(TestCase):
	def setUp(self):
		url = reverse('signup')
		data = {
			'username': 'user',
			'email': 'mail@mail.com',
			'password1': 'password212121',
			'password2': 'password212121'
		}
		self.response = self.client.post(url, data)

	def test_redirection(self):
		self.assertRedirects(self.response, reverse('home'))

	def test_user_creation(self):
		self.assertTrue(User.objects.exists())

	def test_user_authenticaton(self):
		response = self.client.get(reverse('home'))
		user = response.context.get('user')
		self.assertTrue(user.is_authenticated)

class InvalidSignUpTests(TestCase):
	def setUp(self):
		url = reverse('signup')
		self.response = self.client.post(url, {})

	def test_redirection(self):
		self.assertEquals(self.response.status_code, 200)

	def test_user_creation(self):
		self.assertFalse(User.objects.exists())

	def test_form_errors(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)