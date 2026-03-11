## Payment Service

This service manages **payment transactions** (`Transaction`), status logs, and gateway/bank/provider configuration.

---

## Run the service (dev)

From the repo root, make sure dependencies and shared libs are installed:

```bash
pip install -r requirements.txt
pip install -e .\shared_libs\python
```

Run migrations and start the server:

```bash
cd .\services\payment_service
python manage.py migrate
python manage.py runserver 8002
```

---

## `.env` configuration

`core/settings.py` loads env vars from `services/payment_service/.env`.

Common variables:

- `SECRET_KEY`
- `DEBUG` (`True`/`False`)
- `DB_NAME` (default: `payment_db`)
- `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

---

## Domain model

### `transactions.Transaction`

- `order_id` (UUID): reference to the Order Service
- `reference_id` (unique): reference code (often mapped to an internal order code)
- `amount`, `currency` (default `VND`)
- `provider`: e.g. `vnpay`, `momo`, `stripe`, `banking`
- `payment_method`: more specific method descriptor (nullable)
- `status`: `pending/processing/success/failed/refunded/canceled`
- Gateway fields:
  - `gateway_transaction_id`
  - `gateway_response_code`
  - `gateway_message`
  - `signature` (used to verify callback/webhook)
  - `paid_at`

### `transactions.TransactionLog`

- FK `transaction`
- `status_from`, `status_to`
- `message`
- `raw_data` (JSON): callback/webhook payload

### `banks.PaymentGateway`

- `name`, `code` (unique), `is_active`
- `config` (JSON): **recommended to encrypt at the application layer** before storing

---

## API (current state & next steps)

`core/urls.py` is currently `urlpatterns = []`, so the service **does not expose endpoints yet**.

Suggested checklist:

- API to create a transaction from `order_id/reference_id/amount`
- API endpoint to receive callback/webhook to update transaction status + write `TransactionLog`
- API to query transactions by `reference_id` or `order_id`
- Admin API for `PaymentGateway` (CRUD, enable/disable)
- Include routes in `core/urls.py`

