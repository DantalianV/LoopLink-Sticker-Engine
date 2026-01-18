from rest_framework import serializers
from .models import Shopper, Transaction

class ItemSerializer(serializers.Serializer):
    sku = serializers.CharField()
    name = serializers.CharField()
    quantity = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)
    category = serializers.CharField()

class TransactionIngestSerializer(serializers.Serializer):
    transaction_id = serializers.CharField()
    shopper_id = serializers.CharField()
    store_id = serializers.CharField()
    timestamp = serializers.DateTimeField()
    items = ItemSerializer(many=True)

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'store_id', 'total_amount', 'stickers_earned', 'timestamp']

class ShopperSummarySerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Shopper
        fields = ['shopper_id', 'sticker_balance', 'transactions']