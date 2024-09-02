# Generated by Django 5.1 on 2024-09-02 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='color_name',
            field=models.IntegerField(choices=[('primary', 'primary'), ('success', 'success'), ('danger', 'danger'), ('dark', 'dark'), ('secondary', 'secondary'), ('warning', 'warning')], default=0),
        ),
    ]