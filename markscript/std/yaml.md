# YAML

YAML parsing, dumping, validation, and deep-merge routines.

## parse

Parse a YAML string into a MarkScript value. Supports nested dicts, lists, scalars, and multi-line strings.

> run "python -c \"import yaml; print(yaml.safe_load(open('f.yaml')))\""

```markscript
let yaml_text = `
server:
  host: 0.0.0.0
  port: 8080
databases:
  - name: primary
    url: postgres://localhost/main
  - name: cache
    url: redis://localhost:6379
`

let data = yaml.parse(yaml_text)
> assert data["server"]["host"] "0.0.0.0"
> assert data["databases"][0]["name"] "primary"
> assert data["databases"][1]["url"] "redis://localhost:6379"
```

## dump

Serialize a MarkScript value into a YAML string with proper indentation.

> write file "generated.yaml" content

```markscript
let config = {}
config["app"] = {}
config["app"]["name"] = "myapp"
config["app"]["version"] = "2.0"
config["app"]["features"] = ["auth", "api", "admin"]

let out = yaml.dump(config)
# app:
#   name: myapp
#   version: "2.0"
#   features:
#     - auth
#     - api
#     - admin

> write file "app-config.yaml" out
```

## validate

Check whether a YAML string is valid syntactically. Returns `true` or `false`.

> run "python -c \"import yaml; ...\""

```markscript
let good = yaml.validate("key: value\nnested:\n  a: 1")
let bad = yaml.validate("key: value\n  bad indent")

> assert good true
> assert bad false
```

## merge

Deep-merge two YAML documents, with the second document's values taking precedence.

> run "python -c \"... yaml ... deepmerge ...\""

```markscript
let base = yaml.parse(`
server:
  port: 8080
  log_level: info
`)

let override = yaml.parse(`
server:
  port: 9090
  workers: 4
`)

let merged = yaml.merge(base, override)
# server: {port: 9090, log_level: info, workers: 4}

> assert merged["server"]["port"] 9090
> assert merged["server"]["log_level"] "info"
> assert merged["server"]["workers"] 4
```

## get_value

Safely extract a dot-notation path from a YAML tree. Returns `null` on missing keys.

> print "Read nested value"

```markscript
let yaml_text = `
deployment:
  kubernetes:
    namespace: production
    replicas: 3
`

let data = yaml.parse(yaml_text)
let ns = yaml.get_value(data, "deployment.kubernetes.namespace")
let missing = yaml.get_value(data, "deployment.kubernetes.cluster")

> assert ns "production"
> assert missing null
```

## from_json

Convert a JSON string to YAML format.

> run "python -c \"import json, yaml; ...\""

```markscript
let json_text = `{"name":"demo","deps":["a","b"]}`

let yaml_str = yaml.from_json(json_text)
# name: demo
# deps:
#   - a
#   - b

> print yaml_str
```

## to_json

Convert a YAML string to JSON format.

> run "python -c \"import yaml, json; ...\""

```markscript
let yaml_text = "name: demo\nport: 3000"

let json_str = yaml.to_json(yaml_text)
# {"name":"demo","port":3000}

> run "echo '" + json_str + "' | jq ."
```
