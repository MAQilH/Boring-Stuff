from typing import Any
from django.core.management.base import BaseCommand, CommandParser, CommandError
from django.apps import apps
import csv
from django.db import models


class Command(BaseCommand):
    help = 'Import data from csv file'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('file_path', type=str, help='Path to the csv file')
        parser.add_argument('model_name', type=str, help='Name of the model')

    def add_student(self, data, model: models.Model):
        roll_no = data['roll_no']
        existing_record = model.objects.filter(roll_no = roll_no).exists()
        if not existing_record:
            model.objects.create(**data)
        else:
            self.stdout.write(self.style.WARNING(f'Student with roll no {roll_no} already exists!'))

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

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.add_student(row, model)

        self.stdout.write(self.style.SUCCESS("Data added successfully!")) 