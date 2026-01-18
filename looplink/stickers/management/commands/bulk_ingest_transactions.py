import json
import os
from django.core.management.base import BaseCommand, CommandError
from looplink.stickers.service import StickerEngine

class Command(BaseCommand):
    help = 'Bulk ingests a list of transactions from a single JSON file.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file containing a list of transactions')

    def handle(self, *args, **options):
        file_path = options['json_file']

        if not os.path.exists(file_path):
            raise CommandError(f"File '{file_path}' not found.")

        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            if not isinstance(data, list):
                raise CommandError("The JSON file must contain a LIST of transactions (e.g., [ {...}, {...} ]).")

            success_count = 0
            duplicate_count = 0
            error_count = 0

            self.stdout.write(f"Starting bulk ingestion of {len(data)} transactions...\n")

            for entry in data:
                try:
                    # Reuse the existing service logic
                    transaction, created = StickerEngine.process_transaction(entry)
                    
                    if created:
                        success_count += 1
                    else:
                        duplicate_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error in tx {entry.get('transaction_id', 'unknown')}: {str(e)}"))
                    error_count += 1

            # Final Summary Report
            self.stdout.write(self.style.SUCCESS(f"\nBulk Ingestion Complete:"))
            self.stdout.write(f"- Successfully Processed: {success_count}")
            self.stdout.write(self.style.WARNING(f"- Duplicates Skipped: {duplicate_count}"))
            if error_count > 0:
                self.stdout.write(self.style.ERROR(f"- Errors encountered: {error_count}"))

        except json.JSONDecodeError:
            raise CommandError("Invalid JSON format in file.")
        except Exception as e:
            raise CommandError(f"A critical error occurred: {str(e)}")
        