from ast import parse
from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from dataentry.models import Student
from django.apps import apps
import datetime
import csv

from dataentry.utils import check_model_name_errors


class Command(BaseCommand):
    help = 'Export data from the database to CSV file'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('model_name', type=str, help='Model Name')
        parser.add_argument('file_path', type=str, help='File Path')
    

    def handle(self, *args, **kwargs) -> str | None:       
        model_name = kwargs['model_name'].capitalize()
        file_path = kwargs['file_path']

        model = check_model_name_errors(model_name)

        data = model.objects.all()

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow([field.name for field in model._meta.fields])

            for obj in data:
                writer.writerow([getattr(obj, field.name) for field in model._meta.fields])

        self.stdout.write(self.style.SUCCESS('Data exported successfuly!'))