from PIL import Image
from django.contrib import admin
from django.utils.html import format_html

from image_compression.models import CompressImage
import sys


class CompressImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'thumbnail', 'original_image_size', 'compress_image_size', 'compressed_at')

    def thumbnail(self, obj):
        return format_html(f'<img src="{obj.original_image.url}" width="40" height="40">')

    def compress_image_size(self, obj):
        return self.get_image_size(obj.compressed_image)

    def original_image_size(self, obj):
        return self.get_image_size(obj.original_image)

    def get_image_size(self, img):
        size_in_MB = int(img.size) / (1024 * 1024)
        if size_in_MB < 1:
            return f'{size_in_MB*1024:.2f}KB'
        else:
            return f'{size_in_MB:.2f}MB'

admin.site.register(CompressImage, CompressImageAdmin)