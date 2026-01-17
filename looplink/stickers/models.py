from django.db import models

class Shopper(models.Model):
    shopper_id = models.CharField(max_length=255, unique=True)
    sticker_balance = models.IntegerField(default=0)

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=255, unique=True) # For Idempotency
    shopper = models.ForeignKey(Shopper, on_delete=models.CASCADE, related_name='transactions')
    store_id = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    stickers_earned = models.IntegerField()
    timestamp = models.DateTimeField()
    # Storing raw items as JSON is efficient for a MVP
    # In production use dedicated model for item
    items_data = models.JSONField()
    