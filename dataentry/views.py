from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

from dataentry.tasks import import_data_task, export_data_task
from dataentry.utils import get_all_custom_models_name, check_csv_errors, check_model_name_errors
from uploads.models import Upload


def import_data(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        upload = Upload.objects.create(file=file_path, model_name=model_name)

        relative_path = str(upload.file.url)
        base_url = str(settings.BASE_DIR)
        full_path = base_url + relative_path

        try:
            email_address = request.user.email
            check_csv_errors(full_path, model_name)
            import_data_task.delay(full_path, str(model_name), email_address)
            messages.success(request,
                             f'Your data was been imported, when it is completed We notify you with mail address {email_address}')
        except Exception as e:
            messages.error(request, str(e))

        return redirect('import_data')
    else:
        custom_models_name = get_all_custom_models_name()
        context = {
            'custom_models_name': custom_models_name
        }

    return render(request, 'dataentry/importdata.html', context)


def export_data(request):
    if request.method == 'POST':
        model_name = request.POST.get('model_name')

        try:
            check_model_name_errors(model_name)
            export_data_task.delay(model_name, request.user.email)
            messages.success(request, f'Your data was exported, We will send exported date to {request.user.email}.')
        except Exception as e:
            messages.error(request, str(e))

        return redirect('export_data')
    else:
        custom_models_name = get_all_custom_models_name()
        context = {
            'custom_models_name': custom_models_name
        }
    return render(request, 'dataentry/exportdata.html', context)
