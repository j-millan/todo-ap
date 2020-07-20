from .cases import BaseTestCase
from django.urls import reverse, resolve
from ..models import TodoItem
from ..views import item_action_confirm

class ActionConfirmViewTests(BaseTestCase):
	def setUp(self):
		url = reverse('action_confirm', kwargs={'pk': 1, 'action': 0})
		super().setUp(url)
		
		TodoItem.objects.create(goal='finish this app', user=self.user)

		self.client.login(username=self.username, password=self.password)
		self.response = self.client.get(url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve('/item/1/confirm/0/')
		self.assertEquals(view.func, item_action_confirm)

	def test_contains_links(self):
		home_url = reverse('home')
		done_url = reverse('action_done', kwargs={'pk': 1, 'action': 0})
		self.assertContains(self.response, f'href="{home_url}"', 1)
		self.assertContains(self.response, f'href="{done_url}"', 1)