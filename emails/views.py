from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from awd_main import settings
from uploads.models import Upload
from .forms import EmailForm
from .models import Subscriber, Email, EmailTracking, Sent, List
from .task import send_bulk_email_task
from .utils import add_email_to_subscriber, add_email_csv_file_to_subscriber


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


def create_email_list(request):
    if request.method == 'POST':
        list_name = request.POST.get('list_name')
        emails_csv_file = request.FILES.get('emails_csv_file')

        List.objects.create(email_list=list_name)

        if emails_csv_file is not None:
            import_email_csv_file(list_name, emails_csv_file)

        return redirect('create_email_list')
    else:
        return render(request, 'emails/create_email_list.html')


def add_email_to_list(request):
    if request.method == 'POST':
        email_list_name = request.POST.get('email_list_name')
        added_email = request.POST.get('email_address')
        emails_csv_file = request.FILES.get('emails_csv_file')

        if added_email:
            add_email_to_subscriber(added_email, email_list_name)

        if emails_csv_file is not None:
            import_email_csv_file(email_list_name, emails_csv_file)

        return redirect('add_email_to_list')
    else:
        context = {
            'email_list_names': [list.email_list for list in List.objects.all()]
        }
        return render(request, 'emails/add_email_to_list.html', context)


def import_email_csv_file(email_list_name, emails_csv_file):
    upload = Upload.objects.create(
        file=emails_csv_file,
        model_name=email_list_name
    )
    relative_path = str(upload.file.url)
    base_url = str(settings.BASE_DIR)
    full_path = base_url + relative_path
    add_email_csv_file_to_subscriber(full_path, email_list_name)
