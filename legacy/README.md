# Legacy application

The legacy application is provided by the pinned image:

```text
ghcr.io/fmfi-svt/candle-php:1268d1c
```

The image is configured in the root `compose.yaml` and is reachable only
through the Caddy gateway. It is expected to listen on port `80` inside the
Compose network.

The database connection is configured in
[`config/databases.yml`](config/databases.yml), following the legacy
application's Symfony configuration. The hostname must be `mysql`, which is
the Compose service name; `localhost` would refer to the legacy container
itself.

Application-specific settings are configured in
[`config/app.yml`](config/app.yml) and mounted at
`/var/www/html/apps/frontend/config/app.yml` in the legacy container.
