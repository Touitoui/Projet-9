from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from . import forms


def login_page(request):
    """Handle user authentication and login form processing."""
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'authentication/login.html', context={'form': form, 'message': message})


def logout_user(request):
    """Logs out the current user and redirects to the home page."""
    logout(request)
    return redirect('/')


def signup_page(request):
    """Handle user registration with auto-login and redirect to home page."""
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    return render(request, 'authentication/signup.html', context={'form': form})
