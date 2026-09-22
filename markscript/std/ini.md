# INI

Classic INI configuration file reading, writing, and section management.

## read

Parse an INI string into a section-key dict structure.

> read file "config.ini"

```markscript
let ini_text = `
[general]
app_name = MyApp
version = 1.0

[database]
host = localhost
port = 5432
user = admin
`

let config = ini.read(ini_text)
> assert config["general"]["app_name"] "MyApp"
> assert config["database"]["port"] "5432"
```

## write

Serialize a section-key dict into INI format.

> write file "settings.ini" content

```markscript
let cfg = {}
cfg["net"] = {}
cfg["net"]["host"] = "0.0.0.0"
cfg["net"]["port"] = "8080"

cfg["auth"] = {}
cfg["auth"]["enabled"] = "true"
cfg["auth"]["jwt_secret"] = "***"

let out = ini.write(cfg)
# [net]
# host = 0.0.0.0
# port = 8080
# [auth]
# enabled = true
# jwt_secret = ***

> write file "app.ini" out
```

## section

Retrieve or set an entire section within an INI document.

> print "Working with section"

```markscript
let config = ini.read("[logging]\nlevel=warn\nfile=/var/log/app.log")

# get section
let log = ini.section(config, "logging")
> assert log["level"] "warn"

# set section
config = ini.section(config, "logging", {"level": "debug", "file": "/tmp/debug.log"})
> assert config["logging"]["level"] "debug"
```

## property

Get or set an individual property within a section.

> assert value "expected"

```markscript
let config = ini.read("[ui]\ntheme=dark\nfont_size=14")

# get property
let theme = ini.property(config, "ui", "theme")
> assert theme "dark"

# set property
config = ini.property(config, "ui", "font_size", "16")
> assert config["ui"]["font_size"] "16"
```

## list_sections

Return all section names from an INI document.

> print "Listing sections"

```markscript
let config = ini.read("[a]\nx=1\n[b]\ny=2\n[c]\nz=3")

let sections = ini.list_sections(config)
# ["a", "b", "c"]

> assert sections[0] "a"
> assert sections[2] "c"
```

## delete_section

Remove an entire section from an INI document.

> print "Section removed"

```markscript
let config = ini.read("[keep]\na=1\n[remove]\nb=2")

let cleaned = ini.delete_section(config, "remove")
# only [keep] remains

> assert ini.property(cleaned, "keep", "a") "1"
> assert ini.list_sections(cleaned) ["keep"]
```

## from_dict

Convert a flat dict into an INI section (keys become `[section]` entries, properties become `key = value`).

> print "Converted to INI"

```markscript
let flat = {}
flat["db_host"] = "localhost"
flat["db_port"] = "5432"
flat["db_name"] = "test"

let ini_text = ini.from_dict(flat)
# db_host = localhost
# db_port = 5432
# db_name = test

> write file "flat.ini" ini_text
```
