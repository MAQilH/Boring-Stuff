from django.urls import path

from image_compression import views

urlpatterns = [
    path('compress/', views.compress, name='compress'),
]