# QueryString

Query string encoding, decoding, and parameter manipulation without full URL handling.

## parse

Parse a query string into a key-value dict. Supports multiple values per key (list).

> assert result expected

```markscript
let qs = "name=Alice&age=30&tags=admin&tags=editor"

let params = querystring.parse(qs)
# {"name": "Alice", "age": "30", "tags": ["admin", "editor"]}

> assert params["name"] "Alice"
> assert params["tags"][0] "admin"
> assert params["tags"][1] "editor"
```

## stringify

Convert a key-value dict to a query string.

> print "Generated query string"

```markscript
let params = {}
params["search"] = "hello world"
params["page"] = "2"
params["limit"] = "20"

let qs = querystring.stringify(params)
# "search=hello%20world&page=2&limit=20"

> assert qs match "search=hello%20world"
> assert qs match "page=2"
```

## get

Extract a single parameter value from a query string.

> assert value expected

```markscript
let qs = "token=abc123&format=json&pretty=true"

let token = querystring.get(qs, "token")
let missing = querystring.get(qs, "sort")

> assert token "abc123"
> assert missing null
```

## set

Add or update a parameter in an existing query string.

> print "Updated query string"

```markscript
let qs = "theme=dark&view=grid"

let updated = querystring.set(qs, "theme", "light")
# "theme=light&view=grid"

let extended = querystring.set(updated, "lang", "en")
# "theme=light&view=grid&lang=en"

> assert extended match "theme=light"
> assert extended match "lang=en"
```

## delete_param

Remove a parameter from a query string.

> print "Parameter removed"

```markscript
let qs = "a=1&b=2&c=3&debug=true"

let cleaned = querystring.delete_param(qs, "debug")
# "a=1&b=2&c=3"

> assert cleaned match "a=1"
> assert cleaned not match "debug"
```

## has

Check if a parameter exists in a query string.

> assert result expected

```markscript
let qs = "present=true&also=here"

> assert querystring.has(qs, "present") true
> assert querystring.has(qs, "missing") false
```

## parse_all

Parse a query string into a list of individual `{key, value}` pairs, preserving order and duplicates.

> print "All pairs"

```markscript
let qs = "a=1&b=2&a=3"

let pairs = querystring.parse_all(qs)
# [{"key": "a", "value": "1"}, {"key": "b", "value": "2"}, {"key": "a", "value": "3"}]

> assert pairs[0]["key"] "a"
> assert pairs[0]["value"] "1"
> assert pairs[2]["value"] "3"
```
