## Notification Service

This service manages **notification logs** (email/sms/webhook) and **email templates**.

---

## Run the service (dev)

From the repo root, make sure dependencies and shared libs are installed:

```bash
pip install -r requirements.txt
pip install -e .\shared_libs\python
```

Run migrations and start the server:

```bash
cd .\services\notification_service
python manage.py migrate
python manage.py runserver 8003
```

---

## `.env` configuration

`core/settings.py` loads env vars from `services/notification_service/.env`.

Common variables:

- `SECRET_KEY`
- `DEBUG` (`True`/`False`)
- `DB_NAME` (default: `notification_db`)
- `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

---

## Domain model

### `notifications.NotificationLog`

- `user_id` (nullable)
- `recipient_contact`: email or phone number
- `channel`: `email/sms/webhook`
- `subject`, `content`
Business reference:
  - `reference_type` (e.g. `order`, `payment`)
  - `reference_id` (UUID)
- `status`: `pending/sent/failed`
- `error_message`, `sent_at`

### `notifications.EmailTemplate`

- `code` (unique): e.g. `ORDER_SUCCESS`
- `subject_template`, `body_template` (HTML)
- `variables` (JSON list): required variables list (e.g. `["order_code","amount"]`)
- `is_active`

---

## API (current state & next steps)

`core/urls.py` is currently `urlpatterns = []`, so the service **does not expose endpoints yet**.

Suggested checklist:

- API to create notifications from events (order/payment) → write `NotificationLog`
- Admin API for `EmailTemplate` (CRUD)
- Worker/Celery (optional) to send asynchronously and update `status/sent_at/error_message`
- Include routes in `core/urls.py`

