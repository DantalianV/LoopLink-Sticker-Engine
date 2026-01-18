from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import TransactionIngestSerializer, ShopperSummarySerializer
from .service import StickerEngine
from .models import Shopper

class IngestTransactionView(APIView):
    """
    POST /api/stickers/ingest/
    Accepts a purchase transaction and awards stickers.
    """
    permission_classes = [permissions.AllowAny] # Change to IsAuthenticated for production

    def post(self, request):
        serializer = TransactionIngestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                tx, created = StickerEngine.process_transaction(serializer.validated_data)
                return Response({
                    "transaction_id": tx.transaction_id,
                    "stickers_earned": tx.stickers_earned,
                    "new_balance": tx.shopper.sticker_balance,
                    "status": "created" if created else "already_processed"
                }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShopperStatusView(APIView):
    """
    GET /api/stickers/shopper/<str:shopper_id>/
    Show a list of transactions for a given shopper.
    """
    permission_classes = [permissions.AllowAny] # Change to IsAuthenticated for production

    def get(self, request, shopper_id):
        shopper = StickerEngine.get_shopper_with_history(shopper_id)
        
        if not shopper:
            return Response(
                {"error": f"Shopper with ID {shopper_id} not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        # 3. Serialize and return the Web response
        serializer = ShopperSummarySerializer(shopper)
        return Response(serializer.data)
    