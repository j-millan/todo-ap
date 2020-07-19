from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class BaseTestCase(TestCase):
	def setUp(self, url):
		self.user = User.objects.create_user(username='user', email='email@email.com', password="password")
		self.username = 'user'
		self.password = 'password'
		self.url = url