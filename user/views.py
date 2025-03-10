from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
from . import forms

def hello(request):
    message = 'Bonjour '
    return render(request, 'hello.html', context={'message': message})

def login_page(request):
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
    logout(request)
    return redirect('/')

def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect("/")
            # return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})