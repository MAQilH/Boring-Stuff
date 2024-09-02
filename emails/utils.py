import csv
import re

from emails.models import Subscriber, List

def add_email_csv_file_to_subscriber(csv_file_path, email_list_name):
    with open(csv_file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            add_email_to_subscriber(row[0], email_list_name)

def add_email_to_subscriber(email_address, email_list_name):
    email_list = List.objects.get(email_list=email_list_name)
    if re.match(r'[^@]+@[^@]+\.[^@]+', email_address) and (not Subscriber.objects.filter(email_address=email_address, email_list=email_list).exists()):
        Subscriber.objects.create(
            email_list=email_list,
            email_address=email_address
        )