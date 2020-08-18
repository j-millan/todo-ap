from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.generic import ListView, CreateView, DetailView
from .models import TodoItem
from .forms import TodoItemForm, SignUpForm

@method_decorator(login_required, name='dispatch')
class CompletedTasksView(ListView):
	model = TodoItem
	context_object_name = "items"
	template_name = "completed_tasks.html"

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(user=self.request.user).filter(completed=True).order_by('-completed_at')

@method_decorator(login_required, name='dispatch')
class HomeView(CreateView):
	model = TodoItem
	form_class = TodoItemForm
	template_name = "home.html"

	def form_valid(self, form):
		item = form.save(commit=False)
		item.user = self.request.user
		item.save()
		return self.render_to_response(self.get_context_data())

	def get_context_data(self, **kwargs):
		context = super(CreateView, self).get_context_data()
		context['items'] = TodoItem.objects.filter(user=self.request.user).filter(completed=False).order_by('-added_at')
		return context
		
class SignUpView(CreateView):
	model = User
	form_class = SignUpForm
	template_name = "signup.html"

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('home')

@login_required
def item_info(request, pk):
	item = get_object_or_404(TodoItem, pk=pk)
	if item.user == request.user:
		return render(request, 'item_info.html', {'item': item})
	
	return redirect('home')

@login_required
def item_action_confirm(request, pk, action):
	item = get_object_or_404(TodoItem, pk=pk)
	if item.user == request.user:
		if action == 0 and not item.completed:
			return render(request, 'actions/complete.html', {'item': item})
		elif action == 1:
			return render(request, 'actions/delete.html', {'item': item})

	return redirect('home')

@login_required
def item_action_done(request, pk, action):
	item = get_object_or_404(TodoItem, pk=pk)
	referer = str(request.META.get('HTTP_REFERER')).find(reverse('action_confirm', kwargs={'pk': pk, 'action': action}))
	if item.user == request.user and referer > 0 and not item.completed:
		if action == 0:
			item.completed = True
			item.save()
			return redirect('info', pk=item.pk)
		elif action == 1:
			item.delete()

	return redirect('home')