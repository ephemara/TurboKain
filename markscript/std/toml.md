# TOML

TOML configuration format: reading, writing, sections, and validation.

## read

Parse a TOML string into a MarkScript dict. Table headers become nested keys.

> run "python -c \"import tomllib; print(tomllib.load(open('f.toml')))\"" if py >= 3.11
> run "python -c \"import toml; print(toml.load(open('f.toml')))\""

```markscript
let toml_text = `
[server]
host = "0.0.0.0"
port = 8080

[server.logging]
level = "debug"
`

let config = toml.read(toml_text)
> assert config["server"]["host"] "0.0.0.0"
> assert config["server"]["port"] 8080
> assert config["server"]["logging"]["level"] "debug"
```

## write

Serialize a MarkScript dict to TOML format.

> write file "config.toml" content

```markscript
let cfg = {}
cfg["title"] = "My App"

cfg["build"] = {}
cfg["build"]["compiler"] = "kain"
cfg["build"]["optimize"] = true

cfg["deps"] = {}
cfg["deps"]["kain"] = "0.1.0"
cfg["deps"]["markscript"] = "0.2.0"

let out = toml.write(cfg)
# title = "My App"
# [build]
# compiler = "kain"
# optimize = true
# [deps]
# kain = "0.1.0"
# markscript = "0.2.0"

> write file "pyproject.toml" out
```

## section

Extract a named section from a TOML document as its own dict.

> print "Section extracted"

```markscript
let toml_text = `
[database]
host = "db.internal"
port = 5432

[redis]
host = "redis.internal"
port = 6379
`

let doc = toml.read(toml_text)
let db = toml.section(doc, "database")

> assert db["host"] "db.internal"
> assert db["port"] 5432
```

## key_value

Read or set a specific key within a TOML document using dot notation.

> print "Key updated"

```markscript
let doc = toml.read(`
[tool]
name = "helper"
verbose = false
`)

let name = toml.key_value(doc, "tool.name")
> assert name "helper"

# set a key
let updated = toml.key_value(doc, "tool.verbose", true)
> assert updated["tool"]["verbose"] true
```

## validate

Check whether a TOML string is syntactically valid.

> run "python -c \"import tomllib; ...\"" if py >= 3.11

```markscript
let valid = toml.validate("key = 42\n[section]\nval = true")
let invalid = toml.validate("key = 42\n[section\nval = true")

> assert valid true
> assert invalid false
```

## merge_tables

Merge two or more TOML documents, with later documents taking precedence.

> print "Merged configuration"

```markscript
let base = toml.read("host = \"localhost\"\nport = 3000")
let override = toml.read("port = 4000\nverbose = true")

let merged = toml.merge_tables([base, override])
> assert merged["host"] "localhost"
> assert merged["port"] 4000
> assert merged["verbose"] true
```

## inline_table

Build or parse a TOML inline table (`key = {a = 1, b = "2"}`).

> print "Inline table parsed"

```markscript
let toml_text = `point = {x = 10, y = 20, label = "origin"}`

let doc = toml.read(toml_text)
let pt = doc["point"]

> assert pt["x"] 10
> assert pt["label"] "origin"
```
