import csv
from django.core.management.base import BaseCommand
from core.models import MedicalCollege

class Command(BaseCommand):
    help = 'Import medical college data from CSV'

    def handle(self, *args, **kwargs):
        with open('core/management/commands/medicalcollege_data.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                MedicalCollege.objects.create(
                    institute_name=row['Institute'],
                    state=row['State'],
                    course=row['Course'],
                    category=row['Category'],
                    quota=row['Quota'],
                    round=int(row['Round']),
                    air=int(row['AI Rank']) if row['AI Rank'].isdigit() else None
                )
                count += 1

            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} records.'))
