from django.core.management.base import BaseCommand
from looplink.stickers.service import StickerEngine

class Command(BaseCommand):
    help = 'Displays a shopper\'s sticker balance and transaction history.'

    def add_arguments(self, parser):
        parser.add_argument('shopper_id', type=str, help='The ID of the shopper to look up')

    # Handle a Shopper model not with dic
    def handle(self, *args, **options):
        shopper_id = options['shopper_id']
        summary = StickerEngine.get_shopper_summary(shopper_id)

        if not summary:
            self.stdout.write(self.style.ERROR(f"Shopper '{shopper_id}' not found."))
            return

        self.stdout.write(self.style.SUCCESS(f"\n=== Status for Shopper: {summary['shopper_id']} ==="))
        self.stdout.write(f"Current Sticker Balance: {summary['balance']}")
        self.stdout.write("-" * 100)
        self.stdout.write(f"{'Date':<20} | {'Transaction ID':<15} | {'Earned'}")
        self.stdout.write("-" * 100)

        for tx in summary['history']:
            # Format timestamp for readability
            date_str = tx.timestamp.strftime('%Y-%m-%d %H:%M')
            self.stdout.write(f"{date_str:<20} | {tx.transaction_id:<15} | {tx.stickers_earned}")
        
        self.stdout.write("-" * 100 + "\n")
