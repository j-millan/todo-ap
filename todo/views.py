from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import TodoItem
from .forms import TodoItemForm, SignUpForm

@login_required
def home(request):
	items = TodoItem.objects.filter(user=request.user).order_by('-added_at')

	if request.method == "POST":
		form = TodoItemForm(request.POST)
		if form.is_valid():
			item = form.save(commit=False)
			item.user = request.user
			item.save()
	else:
		form = TodoItemForm()
	
	return render(request, 'home.html', {'items': items, 'form': form})
	#return render(request, 'home.html')

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