from django.core.management.base import BaseCommand
from dataentry.models import Student


class Command(BaseCommand):
    help = 'It will be add data to database'

    def handle(self, *args, **kwargs):
        dataset = [
            {'roll_no': 1002, 'name': 'hasan', 'age': 34},
            {'roll_no': 1005, 'name': 'amin', 'age': 22},
            {'roll_no': 1004, 'name': 'hasanain', 'age': 33},
        ]
        
        for data in dataset:
            roll_no = data['roll_no']
            existing_record = Student.objects.filter(roll_no = roll_no).exists()
            if not existing_record:
                Student.objects.create(name = data['name'], roll_no = data['roll_no'], age = data['age'])
            else:
                self.stdout.write(self.style.WARNING(f'Student with roll no {roll_no} already exists!'))

        self.stdout.write(self.style.SUCCESS('Data added successfully!'))