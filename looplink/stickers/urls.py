from django.urls import path
from .views import IngestTransactionView, ShopperStatusView

urlpatterns = [
    path("ingest/", IngestTransactionView.as_view(), name="api_ingest_transaction"),
    path("shopper/<str:shopper_id>/", ShopperStatusView.as_view(), name="api_shopper_status"),
]

