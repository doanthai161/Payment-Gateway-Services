## Gateway (Nginx)

The `gateway/` directory is the **reverse proxy / API gateway** layer in front of the services.

Current status:

- `nginx.conf`: **empty**
- `Dockerfile`: **empty**

---

## Intended goals

- Path-based routing, for example:
  - `/orders/*` → `order_service`
  - `/payments/*` → `payment_service`
  - `/notifications/*` → `notification_service`
- TLS termination (HTTPS) (environment-dependent)
- Rate limiting / request size limits
- Forward headers: `X-Request-ID`, `X-Forwarded-For`, …

---

## Configuration examples (guidance)

You can implement this in one of two common ways:

- **Local dev**: Nginx proxies to `localhost:8001/8002/8003`
- **Docker compose/k8s**: proxy by service name (internal DNS)

When you fill in `nginx.conf`, make sure you include:

- `proxy_set_header Host $host;`
- `proxy_set_header X-Forwarded-Proto $scheme;`
- `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`

