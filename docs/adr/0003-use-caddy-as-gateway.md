# Use Caddy as the application gateway

## Context and Problem Statement

The application is being rewritten incrementally using the strangler fig approach. The legacy PHP application and the new Django application will run in parallel, and requests must be routed between them through a single gateway.

The gateway should support explicit routing between the legacy and rewritten applications, be easy to configure for local development, and leave room for HTTPS termination and additional services in the future.


## Considered Options

* Nginx - widely used reverse proxy with explicit configuration and extensive routing capabilities
* Caddy - reverse proxy with concise configuration and built-in HTTPS support
* Traefik - Docker-oriented reverse proxy with dynamic service discovery and label-based routing


## Decision Outcome

Chosen option: Caddy, because:

* Its configuration is concise and easy to understand.
* It provides reverse proxy functionality required to route requests between the legacy and Django applications.
* It supports automatic HTTPS, which leaves room for a simpler transition from local development to deployed environments.
* Its configuration can remain explicit and version-controlled while the strangler fig migration is in progress.
* It has fewer concepts and less configuration overhead than Traefik for the current number of services.

The gateway will be the only service exposed to the host. The legacy and Django applications will be reachable through the internal container network and will not expose their ports directly.

Initial routing will send all requests to the legacy application. As features are migrated, individual routes will be added for the Django application.

### Consequences

Positive:

* The gateway provides a stable external entry point while application ownership changes behind it.
* Routing rules can be reviewed and changed independently of the applications.
* The concise configuration reduces the amount of infrastructure required for local development.
* HTTPS termination can be added without introducing a separate reverse proxy.
* The gateway can later route additional services when needed.

Negative:

* The project gains an additional infrastructure component that must be configured and maintained.
* Complex legacy-specific rewrites or advanced proxy behavior may require learning Caddy-specific configuration or extensions.
* Routing changes must be tested separately from the application code to ensure that requests reach the intended application.
