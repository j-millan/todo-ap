from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator

class TodoItem(models.Model):
	user = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
	task = models.CharField(unique=True, max_length=70)
	added_at = models.DateTimeField(auto_now_add=True)
	completed = models.BooleanField(default=False)
	completed_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return self.task

	def get_truncated_task(self):
		truncated_message = Truncator(self.task)
		return truncated_message.chars(25)