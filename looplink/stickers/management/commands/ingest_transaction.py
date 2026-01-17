import json
import os
from django.core.management.base import BaseCommand, CommandError
from looplink.stickers.service import StickerEngine

class Command(BaseCommand):
    help = 'Ingests a transaction from a JSON file and awards stickers.'

    def add_arguments(self, parser):
        # This allows you to pass the filename as an argument
        parser.add_argument('json_file', type=str, help='Path to the JSON transaction file')

    def handle(self, *args, **options):
        file_path = options['json_file']

        if not os.path.exists(file_path):
            raise CommandError(f"File '{file_path}' does not exist.")

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            # Call your service logic
            transaction, created = StickerEngine.process_transaction(data)

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully processed {transaction.transaction_id}. "
                        f"Awarded {transaction.stickers_earned} stickers to {transaction.shopper.shopper_id}."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Transaction {transaction.transaction_id} was already processed (Idempotent check).")
                )

        except json.JSONDecodeError:
            raise CommandError("Invalid JSON format in file.")
        except Exception as e:
            raise CommandError(f"An error occurred: {str(e)}")