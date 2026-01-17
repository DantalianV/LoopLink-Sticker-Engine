from decimal import Decimal
from django.db import transaction
from .models import Transaction, Shopper

class StickerEngine:
    @staticmethod
    def validate_payload(payload):
        """Handle obviously invalid inputs (Basic robustness requirement)."""
        required_fields = ['transaction_id', 'shopper_id', 'items', 'timestamp']
        for field in required_fields:
            if field not in payload or not payload[field]:
                raise ValueError(f"Missing required field: {field}")
        
        if not isinstance(payload['items'], list) or len(payload['items']) == 0:
            raise ValueError("Transaction must contain at least one item.")
            
        for item in payload['items']:
            if item.get('quantity', 0) <= 0 or item.get('unit_price', 0) < 0:
                raise ValueError(f"Invalid quantity or price for item: {item.get('name')}")

    @staticmethod
    def calculate_stickers(payload):
        # Base earn rate: 1 sticker per $10 total basket spend
        total_spend = sum(Decimal(str(i['unit_price'])) * i['quantity'] for i in payload['items'])
        stickers = int(total_spend // 10)

        # Promo item bonus: +1 extra sticker per unit
        for item in payload['items']:
            if item.get('category') == "promo":
                stickers += item['quantity']

        # Per-transaction cap: Max 5 stickers
        return min(stickers, 5)

    @classmethod
    def process_transaction(cls, payload):
        cls.validate_payload(payload) # Validation check
        
        tx_id = payload['transaction_id']
        existing = Transaction.objects.filter(transaction_id=tx_id).first()
        if existing:
            return existing, False # Idempotency check

        stickers = cls.calculate_stickers(payload)
        
        with transaction.atomic():
            shopper, _ = Shopper.objects.get_or_create(shopper_id=payload['shopper_id'])
            new_tx = Transaction.objects.create(
                transaction_id=tx_id,
                shopper=shopper,
                store_id=payload.get('store_id', 'unknown'),
                total_amount=sum(Decimal(str(i['unit_price'])) * i['quantity'] for i in payload['items']),
                stickers_earned=stickers,
                timestamp=payload['timestamp'],
                items_data=payload['items']
            )
            shopper.sticker_balance += stickers
            shopper.save()
            
        return new_tx, True

    @staticmethod
    def get_shopper_summary(shopper_id):
        """Retrieve shopper balance and history."""
        try:
            shopper = Shopper.objects.get(shopper_id=shopper_id)
            # Order by most recent transaction
            history = shopper.transactions.all().order_by('-timestamp')
            return {
                "shopper_id": shopper.shopper_id,
                "balance": shopper.sticker_balance,
                "history": history
            }
        except Shopper.DoesNotExist:
            return None
        