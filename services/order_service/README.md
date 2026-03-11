## Order Service

This service manages **orders** (`Order`) and **order line items** (`OrderItem`).

---

## Run the service (dev)

From the repo root, make sure dependencies and shared libs are installed:

```bash
pip install -r requirements.txt
pip install -e .\shared_libs\python
```

Run migrations and start the server:

```bash
cd .\services\order_service
python manage.py migrate
python manage.py runserver 8001
```

---

## `.env` configuration

`core/settings.py` loads env vars from `services/order_service/.env`.

Common variables:

- `SECRET_KEY`
- `DEBUG` (`True`/`False`)
- `DB_NAME` (default: `order_db`)
- `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

---

## Domain model

### `orders.Order`

- `user_id` (UUID): reference to the User Service (no FK).
- `order_code` (unique)
- `total_amount`, `shipping_fee`, `final_amount`
- Shipping snapshot: `recipient_name`, `recipient_phone`, `shipping_address`
- `status`: `pending/confirmed/shipping/completed/cancelled`
- `payment_id` (UUID, nullable): links to the Payment Service (transaction id)

### `orders.OrderItem`

- FK `order`
- Product snapshot: `product_id`, `product_name`, `sku`, `quantity`, `unit_price`

---

## API (current state & next steps)

`core/urls.py` is currently `urlpatterns = []`, so the service **does not expose endpoints yet**.

Suggested checklist:

- Create `orders/serializers.py` (`Order`, `OrderItem`)
- Create `orders/views.py` (order CRUD, list/filter, add items)
- Create `orders/urls.py` and include it in `core/urls.py`
- (Optional) enable DRF + schema (Swagger/OpenAPI)

