from awd_main.celery import app
from dataentry.utils import send_email_notification

@app.task
def send_bulk_email_task(subject, body, to_emails, attachment):
    send_email_notification(subject, body, to_emails, attachment)
    return 'emails send successfully'