# Jq

MarkScript JSON query -- filter, transform, and manipulate JSON data.
Wraps `jq` via the IVT for structured data processing.

---

## filter

Extract a value using a simple filter expression.

> run "jq '.name' data.json"

```markscript
let filter = ".name"
let file = "data.json"
push("jq '" + filter + "' " + file)
call("run")
# value of the name field
```

---

## nested

Access nested object fields.

> run "jq '.user.address.city' data.json"

```markscript
let filter = ".user.address.city"
let file = "profile.json"
push("jq '" + filter + "' " + file)
call("run")
# nested city field
```

---

## array_index

Access array elements by index.

> run "jq '.items[0]' data.json"

```markscript
let filter = ".items[0]"
let file = "data.json"
push("jq '" + filter + "' " + file)
call("run")
# first element of items array
```

---

## array_slice

Access a slice of an array.

> run "jq '.items[0:5]' data.json"

```markscript
let filter = ".items[0:5]"
let file = "data.json"
push("jq '" + filter + "' " + file)
call("run")
# first 5 elements of items array
```

---

## select

Select objects that match a condition.

> run "jq '.[] | select(.age > 18)' data.json"

```markscript
let field = "age"
let threshold = 18
let file = "users.json"
push("jq '.[] | select(." + field + " > " + threshold + ")' " + file)
call("run")
# all users over 18
```

---

## select_string

Select objects where a field equals a string.

> run "jq '.[] | select(.status == \"active\")' data.json"

```markscript
let field = "status"
let value = "active"
let file = "users.json"
push("jq '.[] | select(." + field + " == \"" + value + "\")' " + file)
call("run")
# active users only
```

---

## map

Transform each element of an array.

> run "jq 'map(.name)' data.json"

```markscript
let field = "name"
let file = "data.json"
push("jq 'map(." + field + ")' " + file)
call("run")
# array of all names
```

---

## map_values

Transform values in an object while keeping structure.

> run "jq 'map_values(. + 1)' data.json"

```markscript
let file = "numbers.json"
push("jq 'map_values(. + 1)' " + file)
call("run")
# all numeric values incremented
```

---

## reduce

Aggregate array elements into a single value.

> run "jq 'reduce .[] as $item (0; . + $item)' data.json"

```markscript
let file = "numbers.json"
push("jq 'reduce .[] as $item (0; . + $item)' " + file)
call("run")
# sum of all numbers
```

---

## group_by

Group array elements by a key.

> run "jq 'group_by(.category)' data.json"

```markscript
let key = "category"
let file = "products.json"
push("jq 'group_by(." + key + ")' " + file)
call("run")
# products grouped by category
```

---

## keys

List the keys of an object.

> run "jq 'keys' data.json"

```markscript
let file = "config.json"
push("jq 'keys' " + file)
call("run")
# all top-level key names
```

---

## values

List the values of an object.

> run "jq '.[]' data.json"

```markscript
let file = "data.json"
push("jq '.[]' " + file)
call("run")
# all values in the object
```

---

## compact

Output compact JSON (no pretty-printing).

> run "jq -c '.' data.json"

```markscript
let file = "data.json"
push("jq -c '.' " + file)
call("run")
# compact single-line output
```

---

## raw_output

Output raw strings without JSON quoting.

> run "jq -r '.name' data.json"

```markscript
let filter = ".name"
let file = "data.json"
push("jq -r '" + filter + "' " + file)
call("run")
# raw unquoted string output
```

---

## slurp

Read multiple JSON objects into an array.

> run "jq -s '.' *.json"

```markscript
let files = "*.json"
push("jq -s '.' " + files)
call("run")
# combines all JSON files into one array
```

---

## merge

Merge objects together.

> run "jq -s 'add' data.json updates.json"

```markscript
let a = "base.json"
let b = "overrides.json"
push("jq -s '.[0] * .[1]' " + a + " " + b)
call("run")
# merged with b overriding a
```

---

## csv_output

Convert JSON to CSV.

> run "jq -r '.[] | [.name, .age, .city] | @csv' data.json"

```markscript
let fields = ".name, .age, .city"
let file = "data.json"
push("jq -r '.[] | [" + fields + "] | @csv' " + file)
call("run")
# CSV output with quoted fields
```

---

## pipe_prettify

Pretty-print piped JSON.

> run "cat messy.json | jq '.'"

```markscript
let file = "messy.json"
push("cat " + file + " | jq '.'")
call("run")
# pretty-printed JSON
```
