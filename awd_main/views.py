from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.shortcuts import render

from dataentry.tasks import celery_test_task


def home(request):
    return render(request, 'home.html')



def celery_test(request):
    celery_test_task.delay()
    return HttpResponse('its working')
