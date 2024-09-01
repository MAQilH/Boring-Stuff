from awd_main.celery import app
from dataentry.utils import send_email_notification


@app.task
def send_bulk_email_task(subject, body, to_emails, attachment, email_id):
    send_email_notification(subject, body, to_emails, attachment, email_id=email_id)
    return 'emails send successfully'
