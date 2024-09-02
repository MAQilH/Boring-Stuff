from django import forms

from image_compression.models import CompressImage


class CompressImageForm(forms.ModelForm):
    class Meta:
        model = CompressImage
        fields = ('original_image', 'quality')

    original_image = forms.ImageField(label='Upload an Image')