from ckeditor.fields import RichTextField
from django.db import models
from django.db.models import ForeignKey


class List(models.Model):
    email_list = models.CharField(max_length=25)

    def __str__(self):
        return self.email_list

    def email_count(self):
        return Subscriber.objects.filter(email_list=self).count()


class Subscriber(models.Model):
    email_list = models.ForeignKey(List, on_delete=models.CASCADE)
    email_address = models.EmailField(max_length=50)

    def __str__(self):
        return self.email_address


class Email(models.Model):
    email_list = models.ForeignKey(List, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    body = RichTextField()
    attachment = models.FileField(upload_to='email-attachments/', blank=True)
    send_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    def open_rate(self):
        total_sent = Sent.objects.get(email=self).total_sent
        if total_sent == 0:
            return 0
        total_open = EmailTracking.objects.filter(email=self, opened_at__isnull=False).count()
        return int(total_open) * 100 // total_sent

    def click_rate(self):
        total_click = EmailTracking.objects.filter(email=self, click_at__isnull=False).count()
        total_open = EmailTracking.objects.filter(email=self, opened_at__isnull=False).count()
        if total_open == 0:
            return 0
        return int(total_click) * 100 // total_open


class EmailTracking(models.Model):
    email = ForeignKey(Email, on_delete=models.CASCADE, null=True, blank=True)
    subscriber = ForeignKey(Subscriber, on_delete=models.CASCADE, null=True, blank=True)
    unique_id = models.CharField(max_length=50, unique=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    click_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email.subject


class Sent(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, null=True, blank=True)
    total_sent = models.IntegerField(default=0)

    def __str__(self):
        return str(self.email)
