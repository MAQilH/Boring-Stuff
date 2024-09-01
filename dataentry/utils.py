import csv
import datetime
import hashlib
import os.path
import time

from bs4 import BeautifulSoup
from django.apps import apps
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management import CommandError
from django.db import DataError

from emails.models import Email, Sent, EmailTracking, Subscriber


def get_all_custom_models_name():
    default_models = ['LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session', 'Upload']
    custom_models = []
    for model in apps.get_models():
        name = model.__name__
        if name not in default_models:
            custom_models.append(name)
    return custom_models


def check_csv_errors(file_path, model_name):
    model = check_model_name_errors(model_name)

    model_fields = [field.name for field in model._meta.fields if field.name != 'id']
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames
            if csv_header != model_fields:
                raise DataError(f'CSV file doesn\'t match with the {model_name} table fields.')
    except Exception as e:
        raise e

    return model


def check_model_name_errors(model_name):
    model = None
    for app_config in apps.get_app_configs():
        try:
            model = apps.get_model(app_config.label, model_name)
            break
        except LookupError:
            continue

    if not model:
        raise CommandError(f'Model {model_name} not found in any app!')
    return model


def send_email_notification(subject, message, to_email, attachment=None, email_id=None):
    from_email = settings.DEFAULT_FROM_EMAIL
    for email in to_email:
        mail = EmailMessage(subject, message, from_email, [email])
        if attachment:
            mail.attach_file(attachment)
        mail.content_subtype = 'html'

        if email_id is not None:
            mail = tracking_email(mail, email_id, email)

        mail.send()

    record_sent(email_id)


def tracking_email(mail: EmailMessage, email_id, to_email):
    email = Email.objects.get(id=email_id)

    email_track = EmailTracking()
    email_track.email = email
    email_track.subscriber = Subscriber.objects.get(email_address=to_email, email_list=email.email_list)
    timestamp = str(time.time())
    data_to_hash = f'{to_email}{timestamp}'
    email_track.unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
    email_track.save()

    click_tracking_url = f'{settings.BASE_URL}/emails/track/click/{email_track.unique_id}'
    open_tracking_url = f'{settings.BASE_URL}/emails/track/open/{email_track.unique_id}'

    soup = BeautifulSoup(mail.body, 'html.parser')
    for a in soup.find_all('a', href=True):
        url = a['href']
        new_url = f'{click_tracking_url}?url={url}'
        mail.body = mail.body.replace(url, new_url)

    open_tracking_img = f'<img src="{open_tracking_url}" width="1" height="1">'
    mail.body += open_tracking_img

    return mail


def record_sent(email_id):
    if email_id:
        email_model = Email.objects.get(id=email_id)
        sent_email = Sent()
        sent_email.email = email_model
        sent_email.total_sent = email_model.email_list.email_count()
        sent_email.save()


def generate_csv_export_file_path(model_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_name = f'{model_name}_exported_data_{timestamp}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, 'store', file_name)
    return file_path
