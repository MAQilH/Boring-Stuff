from typing import Any
from django.core.management.base import BaseCommand, CommandParser, CommandError
from django.apps import apps
import csv
from django.db import models, DataError

from dataentry.utils import check_csv_errors


class Command(BaseCommand):
    help = 'Import data from csv file'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('file_path', type=str, help='Path to the csv file')
        parser.add_argument('model_name', type=str, help='Name of the model')


    def handle(self, *args, **options):
        file_path = options['file_path']
        model_name = options['model_name'].capitalize()

        model = check_csv_errors(file_path, model_name)

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.__contains__('id'):
                    del row['id']
                model.objects.create(**row)

        self.stdout.write(self.style.SUCCESS("Data added successfully!")) 