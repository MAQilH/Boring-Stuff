import io

from django.http import HttpResponse
from django.shortcuts import render, redirect

from image_compression.forms import CompressImageForm

from PIL import Image

from image_compression.models import CompressImage


def compress(request):
    if request.method == 'POST':
        image_compress_form = CompressImageForm(request.POST, request.FILES)
        user = request.user
        if image_compress_form.is_valid():
            original_image = image_compress_form.cleaned_data['original_image']
            quality = image_compress_form.cleaned_data['quality']

            compressed_image_model: CompressImage = image_compress_form.save(commit=False)
            compressed_image_model.user = user

            img = Image.open(original_image)
            buffer = io.BytesIO()
            output_format = img.format
            img.save(buffer, output_format, quality=quality)
            buffer.seek(0)

            compressed_image_model.compressed_image.save(
                f'compressed_{original_image}', buffer
            )

            response = HttpResponse(buffer.getvalue(), content_type='image/' + output_format.lower())
            response['Content-Disposition'] = f'attachment; filename=compressed_{original_image}'
            return response
        else:
            return redirect('home')
    else:
        form = CompressImageForm()
        context = {
            'form': form
        }
        return render(request, 'image_compression/compress.html', context=context)

