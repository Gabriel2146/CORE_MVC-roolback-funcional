from django.core.management.base import BaseCommand
from wger_integration.services import fetch_wger_exercises

class Command(BaseCommand):
    help = 'Sync exercises from the wger API'

    def handle(self, *args, **options):
        count = fetch_wger_exercises()
        self.stdout.write(self.style.SUCCESS(f'Successfully synced {count} exercises from wger API'))
