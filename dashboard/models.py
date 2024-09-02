from django.db import models

class Feature(models.Model):
    CHOICE_COLORS = ['primary', 'success', 'danger', 'dark', 'secondary', 'warning']

    name = models.CharField(max_length=50)
    explanation = models.CharField(max_length=200)
    color_name = models.CharField(max_length=20, choices=[(color, color) for color in CHOICE_COLORS], default='success')
    url = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name