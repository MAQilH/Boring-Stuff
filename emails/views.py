from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import EmailForm
from .models import Subscriber, Email, EmailTracking, Sent
from .task import send_bulk_email_task


def send_email(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email = email_form.save()
            subject = request.POST.get('subject')
            body = request.POST.get('body')
            subscribers = Subscriber.objects.filter(email_list=email.email_list)
            to_emails = [subscriber.email_address for subscriber in subscribers]
            if email.attachment:
                attachment = email.attachment.path
            else:
                attachment = None

            send_bulk_email_task.delay(subject, body, to_emails, attachment, email.id)

            messages.success(request, 'Your email has been sent.')
            return redirect('send_email')
        else:
            messages.error(request, email_form.errors)
            return redirect('send_email')
    else:
        email_form = EmailForm()
        contex = {'email_form': email_form}
        return render(request, 'emails/send-email.html', contex)


def track_click(request, unique_id):
    email_track = get_object_or_404(EmailTracking, unique_id=unique_id)
    email_track.click_at = timezone.now()
    email_track.save()
    url = request.GET.get('url')
    if url is not None:
        return redirect(url)
    return redirect('home')


def track_open(request, unique_id):
    email_track = get_object_or_404(EmailTracking, unique_id=unique_id)
    email_track.opened_at = timezone.now()
    email_track.save()
    return HttpResponse('email opened')


def track_dashboard(request):
    emails = (Email.objects.all()
              .order_by('-send_at')
              .annotate(total_sent=Sum('sent__total_sent'))
              )
    context = {
        'emails': emails
    }
    return render(request, 'emails/track_dashboard.html', context)


def track_stats(request, pk):
    email = get_object_or_404(Email, pk=pk)
    sent = Sent.objects.get(email=email)
    context = {
        'email': email,
        'total_sent': sent.total_sent
    }
    return render(request, 'emails/track_stats.html', context)
