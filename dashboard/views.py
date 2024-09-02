from django.shortcuts import render

from dashboard.models import Feature


def home(request):
    context = {
        'features': Feature.objects.all()
    }
    print(context['features'])
    return render(request, 'home.html', context)