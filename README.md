## Banking Payment Project (Payment Gateway - Microservices)

This repository is a **Payment Gateway**-style system built as **Django microservices**:

- **Order Service**: manages orders + shipping info snapshots.
- **Payment Service**: manages payment transactions + gateway/provider/bank configuration.
- **Notification Service**: stores notification send logs + email templates.
- **Gateway (Nginx)**: reverse proxy / API gateway layer (currently a scaffold; needs config).
- **Infrastructure**: Prometheus/Grafana scaffold (currently a scaffold; needs config).
- **Shared libs**: shared Python library code (base models, utilities, etc.).

> Note: each service currently has `core/urls.py` set to `urlpatterns = []` (no API routes exposed yet). This README still documents setup/run steps and points out where routes need to be added.

---

## Repository structure

```
banking_payment_project/
  gateway/                 # Nginx gateway (Dockerfile, nginx.conf)
  infrastructure/          # Prometheus/Grafana + base image (placeholder)
  deploy/                  # docker compose production (placeholder)
  docs/                    # docs, architecture diagram, postman (placeholder)
  scripts/                 # dev/lint/bootstrap scripts (placeholder)
  shared_libs/python/      # python package: common/*
  services/
    order_service/
    payment_service/
    notification_service/
```

---

## Requirements

- **Python**: 3.11+ (recommended)
- **PostgreSQL**: 13+ (each service uses its own DB by default)
- **Redis**: (if/when enabling Celery)
- (Optional) **Docker Desktop** for containerized runs

---

## Quickstart (dev)

### 1) Create a virtualenv

From the repo root:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -U pip
```

### 2) Install dependencies per service

Each service has its own `requirements.txt`:

```bash
pip install -r .\services\order_service\requirements.txt
pip install -r .\services\payment_service\requirements.txt
pip install -r .\services\notification_service\requirements.txt
```

### 3) Configure environment variables per service

Each service loads env vars from `services/<service>/.env`. Start by copying the example files:

```bash
copy .\services\order_service\.env.example .\services\order_service\.env
copy .\services\payment_service\.env.example .\services\payment_service\.env
copy .\services\notification_service\.env.example .\services\notification_service\.env
```

Then edit the `.env` files with your real values.

### Notes on shared libs (`common.*`)

Services import `common.base_models` from `shared_libs/python/common`.

The shared libs are installed via an editable `-e ..\..\shared_libs\python` line inside each service `requirements.txt`.

---

## Running services

Each service is a standalone Django project with its own `manage.py`.

### Order Service

```bash
cd .\services\order_service
python manage.py migrate
python manage.py runserver 8001
```

### Payment Service

```bash
cd .\services\payment_service
python manage.py migrate
python manage.py runserver 8002
```

### Notification Service

```bash
cd .\services\notification_service
python manage.py migrate
python manage.py runserver 8003
```

> Ports are suggestions; feel free to change them.

---

## Default databases per service

Each service reads its own `.env` file (in `services/<service>/.env`) because `settings.py` uses:

`load_dotenv(BASE_DIR / '.env')`

Defaults when `DB_NAME` is not set:

- `order_service` → `order_db`
- `payment_service` → `payment_db`
- `notification_service` → `notification_db`

---

## Shared libraries

`shared_libs/python/` is a package named `shared-libs` exporting the `common` module.

- `common.base_models.TimeStampedModel`: `created_at`, `updated_at`
- `common.base_models.UUIDModel`: UUID primary key `id`

---

## API / routing (current state)

These files:

- `services/order_service/core/urls.py`
- `services/payment_service/core/urls.py`
- `services/notification_service/core/urls.py`

currently **does not include any endpoints** (`urlpatterns = []`).

To expose an API, you need to:

- create `views.py` / `serializers.py` / `urls.py` for each app (`orders`, `transactions`, `notifications`, …)
- `include()` them in `core/urls.py`

Suggested endpoint groups (based on current models):

- **Order Service**: `orders`, `order-items`, link `payment_id`
- **Payment Service**: `transactions`, `transaction-logs`, `payment-gateways`
- **Notification Service**: `notification-logs`, `email-templates`

---

## Gateway (Nginx)

The `gateway/` folder contains `Dockerfile` and `nginx.conf` but they are currently **empty**.  
See `gateway/README.md` for the scaffold and guidance.

---

## Observability (Prometheus/Grafana)

`infrastructure/` contains a scaffold for `docker-compose.yml` and `prometheus/`, `grafana/` config (currently placeholders).  
Once completed, you can use `django-prometheus` (already pinned in each service `requirements.txt`) to expose metrics.

---

## Documentation

`docs/architecture_diagram.drawio.pdf` contains the architecture diagram.

`docs/postman_collection.json` is currently empty (placeholder).

---

## Troubleshooting

- **ImportError: No module named 'common'**
  - Re-run: `pip install -e .\shared_libs\python`
- **Django isn't reading the .env**
  - Ensure `.env` is located under the service directory: `services/<service>/.env`
  - Or set environment variables directly in your shell/session
- **No API endpoints available**
  - `core/urls.py` is currently empty. You need to add app routes/views and `include()` them into `urlpatterns`.

