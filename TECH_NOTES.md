# Tech Notes: Mini Sticker Engine

## 1. Problem Overview
The goal was to build a self-contained loyalty system that calculates sticker rewards based on purchase transactions while ensuring data integrity, idempotency, and ease of use via both CLI and API.

## 2. Approach & Modularity
- **Service Layer Pattern**: All business logic (sticker calculations, validation, and persistence) is encapsulated in the `StickerEngine` class. This allows the CLI commands and the REST API to share the same logic, ensuring "DRY" code and consistent behavior across interfaces.
- **Idempotency**: The system checks for existing `transaction_id` records before processing. This prevents shoppers from being double-awarded stickers if a transaction is submitted multiple times.
- **Performance (Eager Loading)**: To avoid the N+1 query problem when retrieving shopper history, we implemented `prefetch_related('transactions')` in the service layer.
- **Database**: SQLite was chosen for its zero-configuration and file-based portability, making it the most efficient choice for this MVP.

## 3. Example Commands / Requests to Try

### CLI Commands
- **Ingest Transaction**:
  `uv run python manage.py ingest_transaction my_data.json`
- **View Shopper Status**:
  `uv run python manage.py shopper_history shopper-abc-123`

### API Requests (PowerShell)
- **Get Shopper Summary**:
  `curl -X GET http://127.0.0.1:8000/api/stickers/shopper/shopper-abc-123/`

## 4. Use of AI Tools
- **Cursor/ChatGPT**: Used to assist in rapid bootstrapping of Django boilerplates (Serializers and CLI Command structures) and for debugging environment-specific issues like PowerShell alias conflicts with `curl`.
- **Framework Onboarding**: AI was used to quickly understand the specific folder structure of the Looplink starter project and to map out the relationships between project/settings.py and the newly created stickers app.

## 5. Extra Notes
- **Bulk Upload**: Used a cli command to bulk upload transactions.
    ``uv run python manage.py bulk_ingest_transaction bulk_data.json``