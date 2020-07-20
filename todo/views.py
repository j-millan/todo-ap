from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import TodoItem
from .forms import TodoItemForm, SignUpForm

@login_required
def home(request):
	items = TodoItem.objects.filter(user=request.user).filter(completed=False).order_by('-added_at')
	if request.method == "POST":
		form = TodoItemForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.user = request.user
			item.save()
	else:
		form = TodoItemForm()
	
	return render(request, 'home.html', {'items': items, 'form': form})

@login_required
def completed(request):
	items = TodoItem.objects.filter(user=request.user).filter(completed=True).order_by('-completed_at')
	return render(request, 'completed_tasks.html', {'items': items})

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
	if item.user == request.user and not item.completed:
		if action == 0:
			item.completed = True
			item.save()
			return redirect('info', pk=item.pk)
		elif action == 1:
			item.delete()

	return redirect('home')

def signup(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('home')

	else:
		form = SignUpForm()

	return render(request, 'signup.html', {'form': form})