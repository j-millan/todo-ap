from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import TodoItem
from ..views import item_action_done

class ActionDoneViewTestCase(TestCase):
	def setUp(self, url, confirm_url):
		user = User.objects.create_user(username='user', email='email@email.com', password="password")
		self.item = TodoItem.objects.create(goal='finish this app', user=user)
		self.client.login(username='user', password='password')
		self.client.get(confirm_url)
		self.response = self.client.get(url)

class ActionCompleteDoneViewTest(ActionDoneViewTestCase):
	def setUp(self):
		url = reverse('action_done', kwargs={'pk': 1, 'action': 0})
		confirm_url = reverse('action_confirm', kwargs={'pk': 1, 'action': 0})
		super().setUp(url, confirm_url)

	'''def test_redirection(self):
		info_url = reverse('info', kwargs={'pk': 1})
		self.assertRedirects(self.response, info_url)

	def test_completed(self):
		pass
		#self.assertTrue(self.item.completed)'''

class ActionDeleteDoneViewTests(ActionDoneViewTestCase):
	def setUp(self):
		url = reverse('action_done', kwargs={'pk': 1, 'action': 1})
		confirm_url = reverse('action_confirm', kwargs={'pk': 1, 'action': 1})
		super().setUp(url, confirm_url)

	'''def test_redirection(self):
		self.assertRedirects(self.response, reverse('home'))

	def test_deleted(self):
		self.assertFalse(TodoItem.objects.exists())'''