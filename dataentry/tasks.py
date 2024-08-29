from django.conf import settings
from django.core.management import call_command

from awd_main.celery import app
from dataentry.utils import send_email_notification


@app.task
def celery_test_task():
    send_email_notification('Test Subject', 'Sample Message', settings.DEFAULT_TO_EMAIL)
    return 'task executed successfully.'


@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e
    send_email_notification('Import successfully done!',
              'your data successfully inserted to the corresponding model!',
              settings.DEFAULT_TO_EMAIL
                )
    return "Data imported successfully."