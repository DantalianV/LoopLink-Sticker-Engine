from django.core.management.base import BaseCommand
from looplink.stickers.service import StickerEngine

class Command(BaseCommand):
    help = "Displays a shopper's sticker balance and transaction history."

    def add_arguments(self, parser):
        parser.add_argument("shopper_id", type=str, help="The ID of the shopper to look up")

    def handle(self, *args, **options):
        shopper_id = options["shopper_id"]
        
        # 1. Use the updated service method that returns a Shopper model
        shopper = StickerEngine.get_shopper_with_history(shopper_id)

        if not shopper:
            self.stdout.write(self.style.ERROR(f"Shopper '{shopper_id}' not found."))
            return

        # 2. Access attributes directly from the Shopper model
        self.stdout.write(self.style.SUCCESS(f"\n=== Status for Shopper: {shopper.shopper_id} ==="))
        self.stdout.write(f"Current Sticker Balance: {shopper.sticker_balance}")
        
        self.stdout.write("-" * 100)
        self.stdout.write(f"{'Date':<20} | {'Transaction ID':<30} | {'Earned'}")
        self.stdout.write("-" * 100)

        # 3. Access transactions via the related_name defined in the model
        # We order them by timestamp to ensure the newest are first
        transactions = shopper.transactions.all().order_by("-timestamp")
        
        for tx in transactions:
            date_str = tx.timestamp.strftime("%Y-%m-%d %H:%M")
            self.stdout.write(f"{date_str:<20} | {tx.transaction_id:<30} | {tx.stickers_earned}")
        
        self.stdout.write("-" * 100 + "\n")