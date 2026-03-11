## Infrastructure (Prometheus / Grafana)

`infrastructure/` is intended to hold **observability** configuration for the system:

- Prometheus: scrape metrics
- Grafana: dashboard

Current status:

- `docker-compose.yml`: empty (placeholder)
- `prometheus/`, `grafana/`: directories exist but configs need to be completed

---

## Django metrics integration (guidance)

This repo already includes `django-prometheus` in `requirements.txt`.

When you're ready to enable metrics per service:

- Add `django_prometheus` to `INSTALLED_APPS`
- Add the `django_prometheus` middleware
- Expose `/metrics` and configure Prometheus to scrape each service

