from django.contrib import admin
from .models import Upload

class UploadAdmin(admin.ModelAdmin):
    list_display = ['model_name', 'upload_date']

admin.site.register(Upload, UploadAdmin)
