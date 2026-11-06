# Temporarily use `mysql_native_password` for the legacy application

## Context and Problem Statement

The legacy application runs on PHP 5.6 with the legacy `pdo_mysql` client
provided by `mysqlnd`. MySQL 8 defaults to the `caching_sha2_password`
authentication plugin. This decision is a temporary compatibility measure
until the legacy application is removed or its database client is upgraded.

When the MySQL service uses that default, the legacy application cannot
connect:

```text
The server requested authentication method unknown to the client
[caching_sha2_password]
```

The MySQL service therefore emits a deprecation warning when the compatible
`mysql_native_password` plugin is used.

## Considered Options

* `caching_sha2_password` - the more secure modern default, but not an option
  for the current deployment. It was tested with the legacy image and
  the application failed to connect because its PHP 5.6 client does not
  recognize this authentication method.
* `mysql_native_password` - supported by the current legacy client, but
  deprecated and less secure.
* Upgrade the legacy application's PHP and database client - the preferred
  technical solution, but not worth the investment as the application is
  being rewritten.

## Decision Outcome

Temporarily use `mysql_native_password` for the MySQL account used by the
legacy application. This is required for the currently legacy image to
connect; using `caching_sha2_password` is not a viable alternative without
upgrading the legacy application's PHP and database client.

Suppress only MySQL warning `MY-013360`, which reports use of the deprecated
authentication plugin. We do not reduce general MySQL log verbosity, so other
warnings and errors remain visible.

Revisit this decision when the legacy application is removed or its database
client is upgraded. At that point, switch to `caching_sha2_password` where
supported and remove both the compatibility option and the warning
suppression. The long-term plan is to remove MySQL after the legacy
application has been fully removed.

### Consequences

Good:

* The legacy application can connect to MySQL.
* The log is not repeatedly filled with a known, intentional warning.
* Other MySQL diagnostics remain visible.

Bad:

* The legacy database account uses an older and less secure authentication
  plugin.
* The configuration temporarily depends on a deprecated MySQL feature.
