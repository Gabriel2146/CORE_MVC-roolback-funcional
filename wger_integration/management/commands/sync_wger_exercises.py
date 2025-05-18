from django.core.management.base import BaseCommand
from wger_integration.services import WgerAPIClient

class Command(BaseCommand):
    help = 'Sync exercises from wger API into local database'

    def handle(self, *args, **options):
        client = WgerAPIClient()
        self.stdout.write('Starting sync of wger exercises...')
        client.sync_exercises()
        self.stdout.write('Sync completed successfully.')
