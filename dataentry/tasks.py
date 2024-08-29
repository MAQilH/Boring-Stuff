import time
from pyexpat.errors import messages

from django.core.mail import EmailMessage
from django.core.management import call_command
from dns.tsigkeyring import from_text

from awd_main.celery import app
from django.conf import settings

@app.task
def celery_test_task():
    print("work finished!")
    send_email()
    return 'task executed successfully.'

def send_email():
    mail_subject = 'Test Subject'
    message = 'This is a test message.'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = 'mohammada.hafezi@gmail.com'
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()

@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e
    return "Data imported successfully."