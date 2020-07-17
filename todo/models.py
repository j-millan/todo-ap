from django.db import models
from django.contrib.auth.models import User

class TodoItem(models.Model):
	user = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
	goal = models.CharField(unique=True, max_length=50)
	added_at = models.DateTimeField(auto_now_add=True)
	completed = models.BooleanField(default=False)
	completed_at = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return self.goal