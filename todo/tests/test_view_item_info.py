from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from ..models import TodoItem
from ..views import item_info
from .cases import BaseTestCase

class ItemInfoViewTestCase(BaseTestCase):
	def setUp(self):
		url = reverse('info', kwargs={'pk': 1})
		super().setUp(url)
		TodoItem.objects.create(goal='Finish this app', user=self.user)

class LoginRequiredItemInfoViewTests(ItemInfoViewTestCase):
	def setUp(self):
		super().setUp()
		self.response = self.client.get(self.url)

	def test_redirection(self):
		login_url = reverse('login')
		self.assertRedirects(self.response, f'{login_url}?next={self.url}')

class ItemInfoViewTests(ItemInfoViewTestCase):
	def setUp(self):
		super().setUp()
		self.client.login(username=self.username, password=self.password)
		self.response = self.client.get(self.url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve('/info/1/')
		self.assertEquals(view.func, item_info)

	def test_contains_home_link(self):
		home_url = reverse('home')
		self.assertContains(self.response, f'href="{home_url}"')