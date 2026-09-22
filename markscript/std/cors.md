# CORS

Markscript CORS (Cross-Origin Resource Sharing) -- policy configuration.
Generates and validates CORS headers for HTTP responses.

---

## allow_origin_single

Allow a single specific origin.

> print "Access-Control-Allow-Origin: https://example.com"

---

## allow_origin_wildcard

Allow any origin (not compatible with credentials).

> print "Access-Control-Allow-Origin: *"

---

## allow_methods

Specify allowed HTTP methods.

> print "Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS"

---

## allow_headers

Specify allowed request headers.

> print "Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With"

---

## preflight_response

Generate a full preflight OPTIONS response.

> print "Access-Control-Allow-Origin: https://example.com"
> print "Access-Control-Allow-Methods: POST, GET, OPTIONS"
> print "Access-Control-Allow-Headers: Content-Type"

---

## allow_credentials

Allow credentials (cookies, auth headers) in cross-origin requests.

> print "Access-Control-Allow-Credentials: true"

---

## expose_headers

Expose custom headers to the browser.

> print "Access-Control-Expose-Headers: X-Custom-Header, X-Request-Id"

---

## max_age

Set how long the preflight response can be cached.

> print "Access-Control-Max-Age: 86400"

---

## validate_origin

Check if an origin is in the allowed list.

> print "Checking origin against whitelist"

---

## wildcard_match

Check if an origin matches a wildcard pattern.

> print "Checking origin against subdomain pattern *.example.com"

---

## restrict_host

Generate CORS policy restricted to a specific host.

> print "Access-Control-Allow-Origin: https://app.example.com"

---

## cors_config

Read CORS configuration from a JSON file.

> read file "cors_config.json"
