from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TodoItem

class TodoItemForm(forms.ModelForm):
	class Meta:
		model = TodoItem
		fields = ['goal', ]

class SignUpForm(UserCreationForm):
	email = forms.CharField(required=True, max_length=150, widget=forms.EmailInput())

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']