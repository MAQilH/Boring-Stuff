from django.conf import settings
from django.contrib import messages
from django.core.management import call_command
from django.shortcuts import render, redirect

from dataentry.utils import get_all_custom_models_name
from uploads.models import Upload


def import_data(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        upload = Upload.objects.create(file = file_path, model_name = model_name)

        relative_path = str(upload.file.url)
        base_url = str(settings.BASE_DIR)
        full_path = base_url + relative_path

        try:
            call_command('importdata', full_path, model_name)
            messages.success(request, 'Data imported successfully')
        except Exception as e:
            messages.error(request, str(e))

        return redirect('import_data')

    else:
        custom_models_name = get_all_custom_models_name()
        context = {
            'custom_models_name': custom_models_name
        }

    return render(request, 'dataentry/importdata.html', context)