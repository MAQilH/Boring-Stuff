from typing import Any
from django.core.management.base import BaseCommand, CommandParser, CommandError
from django.apps import apps
import csv
from django.db import models, DataError


class Command(BaseCommand):
    help = 'Import data from csv file'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('file_path', type=str, help='Path to the csv file')
        parser.add_argument('model_name', type=str, help='Name of the model')


    def handle(self, *args, **options):
        file_path = options['file_path']
        model_name = options['model_name'].capitalize()

        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                continue
        
        if not model:
            raise CommandError(f'Model {model_name} not found in any app!')


        model_fields = [field.name for field in model._meta.fields if field.name != 'id']

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames
            if csv_header != model_fields:
                raise DataError(f'CSV file doesn\'t match with the {model_name} table fields.')

            for row in reader:
                if row.__contains__('id'):
                    del row['id']
                model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS("Data added successfully!")) 