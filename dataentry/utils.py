import csv

from django.apps import apps
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management import CommandError
from django.db import DataError


def get_all_custom_models_name():
    default_models = ['LogEntry', 'Permission', 'Group', 'User', 'ContentType', 'Session', 'Upload']
    custom_models = []
    for model in apps.get_models():
        name = model.__name__
        if name not in default_models:
            custom_models.append(name)
    return custom_models

def check_csv_errors(file_path, model_name):
    model = None
    for app_config in apps.get_app_configs():
        try:
            model = apps.get_model(app_config.label, model_name)
            break
        except LookupError:
            continue

    if not model:
        raise CommandError(f'Model {model_name} not found in any app!')

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

def send_email_notification(subject, message, to_email):
    from_email = settings.DEFAULT_FROM_EMAIL
    email = EmailMessage(subject, message, from_email, [to_email])
    email.send()