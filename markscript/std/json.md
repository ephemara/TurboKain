# JSON

JSON parsing, stringification, validation, and manipulation routines.

## parse

Parse a JSON string into a MarkScript value (dict or list).

> read file "data.json"

```markscript
let raw = `{"name":"Alice","scores":[95,87,102]}`

# parse into a dict
let data = json.parse(raw)
let name = data["name"]
let high = data["scores"][2]

> assert name "Alice"
> assert high 102
```

## stringify

Convert a MarkScript value to a compact JSON string.

> print "Serialized to JSON"

```markscript
let obj = {}
let obj["title"] = "Hello"
let obj["count"] = 42
let obj["tags"] = ["a", "b"]

let out = json.stringify(obj)
> assert out `{"title":"Hello","count":42,"tags":["a","b"]}`
```

## pretty_print

Format a JSON string with indentation for human readability.

> run "jq . input.json"

```markscript
let raw = `{"name":"Bob","address":{"city":"NYC","zip":10001}}`

let pretty = json.pretty_print(raw, 2)
# pretty is:
# {
#   "name": "Bob",
#   "address": {
#     "city": "NYC",
#     "zip": 10001
#   }
# }

> print pretty
```

## validate

Check whether a string is well-formed JSON. Returns `true` or `false`.

> assert valid 1

```markscript
let valid = json.validate(`{"ok": true}`)
let invalid = json.validate(`{bad json}`)

> assert valid true
> assert invalid false
```

## get_key

Safely extract a nested key from a JSON object. Returns `null` if missing.

> read file "config.json"

```markscript
let data = json.parse(`{"logging":{"level":"debug","file":"/var/log/app.log"}}`)

let level = json.get_key(data, "logging.level")
let db = json.get_key(data, "database.host")
# db is null - key doesn't exist

> assert level "debug"
> assert db null
```

## set_key

Set a value at a nested path, creating intermediate objects as needed.

> print "Updated JSON"

```markscript
let data = json.parse(`{"app":{"name":"demo"}}`)

let updated = json.set_key(data, "app.version", "1.2.3")
# updated = {"app":{"name":"demo","version":"1.2.3"}}

> print json.stringify(updated)
```

## merge

Deep-merge two JSON objects. Later values override earlier ones.

> run "jq -s '.[0] * .[1]' a.json b.json"

```markscript
let a = json.parse(`{"theme":"dark","window":{"width":800,"height":600}}`)
let b = json.parse(`{"window":{"height":900},"fullscreen":true}`)

let merged = json.merge(a, b)
# {"theme":"dark","window":{"width":800,"height":900},"fullscreen":true}

> assert merged["window"]["height"] 900
> assert merged["fullscreen"] true
```

## array_map

Apply a function to every element in a JSON array. Returns a new array.

> run "jq '[.[] | . * 2]'"

```markscript
let nums = json.parse(`[1,2,3,4]`)

let doubles = json.array_map(nums, fn(x) -> x * 2)
# [2, 4, 6, 8]

> assert doubles[0] 2
> assert doubles[3] 8
```

## array_filter

Return elements from a JSON array that pass a predicate.

> run "jq '[.[] | select(. > 2)]'"

```markscript
let items = json.parse(`[1,5,2,8,3]`)

let big = json.array_filter(items, fn(x) -> x > 3)
# [5, 8]

> assert json.length(big) 2
```
