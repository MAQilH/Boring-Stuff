from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from awd_main.forms import RegistrationForm
from dataentry.tasks import celery_test_task


def home(request):
    return render(request, 'home.html')



def celery_test(request):
    celery_test_task.delay()
    return HttpResponse('its working')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration was successful')
            return redirect('register')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = RegistrationForm()
        context = {'form': form}

    return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('login')