from decimal import Decimal
from .models import Transaction, Shopper
from django.db import transaction

class StickerEngine:
    @staticmethod
    def calculate_stickers(payload):
        # 1. Base Earn: 1 per $10
        total_spend = sum(Decimal(str(i['unit_price'])) * i['quantity'] for i in payload['items'])
        stickers = int(total_spend // 10)

        # 2. Promo Bonus: +1 per promo item unit
        for item in payload['items']:
            if item.get('category') == "promo":
                stickers += item['quantity']

        # 3. Cap: Max 5 per transaction
        return min(stickers, 5)

    @classmethod
    def process_transaction(cls, payload):
        tx_id = payload['transaction_id']
        
        # Idempotency Check
        existing = Transaction.objects.filter(transaction_id=tx_id).first()
        if existing:
            return existing, False # False means 'not newly created'

        stickers = cls.calculate_stickers(payload)
        
        with transaction.atomic():
            shopper, _ = Shopper.objects.get_or_create(shopper_id=payload['shopper_id'])
            
            # Save Transaction
            new_tx = Transaction.objects.create(
                transaction_id=tx_id,
                shopper=shopper,
                store_id=payload['store_id'],
                total_amount=sum(Decimal(str(i['unit_price'])) * i['quantity'] for i in payload['items']),
                stickers_earned=stickers,
                timestamp=payload['timestamp'],
                items_data=payload['items']
            )
            
            # Update Balance
            shopper.sticker_balance += stickers
            shopper.save()
            
        return new_tx, True
    