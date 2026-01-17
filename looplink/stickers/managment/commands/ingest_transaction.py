import json
from django.core.management.base import BaseCommand
from your_app.services import StickerEngine

class Command(BaseCommand):
    help = 'Ingest a transaction via JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
        with open(options['json_file']) as f:
            data = json.load(f)
            tx, created = StickerEngine.process_transaction(data)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Awarded {tx.stickers_earned} stickers!"))
            else:
                self.stdout.write(self.style.WARNING("Transaction already processed."))
                