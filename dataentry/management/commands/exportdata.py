from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from dataentry.models import Student
from django.apps import apps
import datetime
import csv


class Command(BaseCommand):
    help = 'Export data from the database to CSV file'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('model_name', type=str, help='Model Name')
    

    def handle(self, *args, **kwargs) -> str | None:       
        model_name = kwargs['model_name'].capitalize()
        model = None

        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                continue
        
        if not model:
            self.stderr.write(f'Model {model_name} can not found!')
            return

        data = model.objects.all()

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name = f'{model_name}_exported_data_{timestamp}.csv'

        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow([field.name for field in model._meta.fields])

            for obj in data:
                writer.writerow([getattr(obj, field.name) for field in model._meta.fields])

        self.stdout.write(self.style.SUCCESS('Data exported successfuly!'))