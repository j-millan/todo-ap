from django.test import TestCase
from django.urls import reverse, resolve
from ..models import TodoItem
from ..views import completed
from .cases import BaseTestCase

class CompletedTasksViewLoginRequiredTests(BaseTestCase):
	def setUp(self):
		super().setUp(reverse('completed'))
		self.response = self.client.get(self.url)

	def test_redirection(self):
		login_url = reverse('login')
		self.assertRedirects(self.response, f'{login_url}?next={self.url}')

class CompletedTasksViewTests(BaseTestCase):
	def setUp(self):
		super().setUp(reverse('completed'))
		self.client.login(username=self.username, password=self.password)
		self.item = TodoItem.objects.create(goal='Finish this app', user=self.user)
		self.item.completed = True
		self.item.save()
		self.response = self.client.get(self.url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve('/completed/')
		self.assertEquals(view.func, completed)

	def test_shows_completed_task(self):
		self.assertContains(self.response, self.item.get_truncated_goal())

	def test_doesnt_show_uncompleted_task(self):
		self.item.completed = False
		self.item.save()
		response = self.client.get(self.url)
		self.assertContains(response, self.item.get_truncated_goal(), 0)