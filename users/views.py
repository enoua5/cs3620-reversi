from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth, messages
from .forms import RegistrationForm

# Create your views here.

def signup(req):
    if req.method == 'POST':
        form = RegistrationForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = auth.authenticate(username=username, password=password)
            auth.login(req, user)
            messages.success(req, f"Welcome, {username}!")
            return redirect('base:index')
    else:
        form = RegistrationForm()
    return render(req, 'users/register.html', {'form': form})

def login(req):
    if req.method == 'GET':
        form = AuthenticationForm()
        return render(req, 'users/login.html', {'form': form})
    if req.method == 'POST':
        form = AuthenticationForm(request=req, data=req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(req, user)
                # TODO add a redirect to the index page when it exists
                return redirect('base:index')
        else:
            # rerender with errors
            return render(req, 'users/login.html', {'form': form})

def logout(req):
    auth.logout(req)
    return redirect('users:login')
