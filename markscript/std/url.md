# URL

URL parsing, building, and parameter manipulation.

## encode

Percent-encode a string for safe inclusion in URLs.

> print "URL encoded"

```markscript
let query = "name=Alice & Bob/ + done"

let encoded = url.encode(query)
# "name%3DAlice%20%26%20Bob%2F%20%2B%20done"

> assert url.encode("hello world") "hello%20world"
> assert url.encode("a=b") "a%3Db"
```

## decode

Decode a percent-encoded URL string back to plain text.

> print "URL decoded"

```markscript
let encoded = "hello%20world%21"

let decoded = url.decode(encoded)
# "hello world!"

> assert decoded "hello world!"
```

## parse

Parse a URL string into its components: scheme, host, port, path, query, fragment.

> print "Parsed URL"

```markscript
let url_str = "https://user:pass@api.example.com:8080/v1/data?page=2&limit=10#results"

let parts = url.parse(url_str)
# {
#   "scheme": "https",
#   "user": "user",
#   "pass": "pass",
#   "host": "api.example.com",
#   "port": 8080,
#   "path": "/v1/data",
#   "query": "page=2&limit=10",
#   "fragment": "results"
# }

> assert parts["scheme"] "https"
> assert parts["host"] "api.example.com"
> assert parts["port"] 8080
> assert parts["path"] "/v1/data"
```

## build

Construct a URL string from component parts.

> print "Built URL"

```markscript
let parts = {}
parts["scheme"] = "https"
parts["host"] = "example.com"
parts["path"] = "/search"
parts["query"] = "q=hello"

let full = url.build(parts)
# "https://example.com/search?q=hello"

> assert full "https://example.com/search?q=hello"
```

## get_param

Extract a query parameter value from a URL string.

> assert value expected

```markscript
let url_str = "https://example.com/page?name=Alice&age=30"

let name = url.get_param(url_str, "name")
> assert name "Alice"

let missing = url.get_param(url_str, "nonexistent")
> assert missing null
```

## set_param

Add or replace a query parameter in a URL string.

> print "Updated URL"

```markscript
let url_str = "https://example.com/page?name=Alice"

let updated = url.set_param(url_str, "age", "30")
# "https://example.com/page?name=Alice&age=30"

updated = url.set_param(updated, "name", "Bob")
# "https://example.com/page?name=Bob&age=30"

> assert updated match "name=Bob"
> assert updated match "age=30"
```

## remove_param

Remove a query parameter from a URL string.

> print "Parameter removed"

```markscript
let url_str = "https://example.com/page?name=Alice&age=30&debug=true"

let cleaned = url.remove_param(url_str, "debug")
# "https://example.com/page?name=Alice&age=30"

> assert cleaned match "name=Alice"
> assert cleaned not match "debug"
```
