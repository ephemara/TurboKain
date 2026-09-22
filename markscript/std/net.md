# Net

Markscript networking - HTTP requests, file downloads, basic web operations.
Dispatches through the IVT to Kain's process bridge for curl/wget.

---

## get

Make an HTTP GET request and capture the response.

> run "curl -s https://example.com"

```markscript
# Fetch a URL
push("curl -s https://example.com")
call("run")
```

---

## post

Make an HTTP POST request with a JSON body.

> run "curl -s -X POST -d '{\"key\":\"value\"}' https://api.example.com/data"

```markscript
# POST JSON data
push("curl -s -X POST -d '{\"key\":\"value\"}' https://api.example.com/data")
call("run")
```

---

## download

Download a file from a URL.

> run "curl -s -o output.txt https://example.com/file.txt"

```markscript
# Download to file
push("curl -s -o output.txt https://example.com/file.txt")
call("run")
```

---

## headers

Fetch only HTTP response headers.

> run "curl -s -I https://example.com"

```markscript
# Get headers only
push("curl -s -I https://example.com")
call("run")
```

---

## status

Check if a URL is reachable (HTTP status code).

> run "curl -s -o nul -w '%{http_code}' https://example.com"

```markscript
# Check HTTP status
push("curl -s -o nul -w '%{http_code}' https://example.com")
call("run")
```

---

## ping

Ping a host to check connectivity.

> run "ping -n 1 example.com"

```markscript
# Ping a host
push("ping -n 1 example.com")
call("run")
```

---

## dns

Resolve a hostname to an IP address.

> run "nslookup example.com"

```markscript
# DNS lookup
push("nslookup example.com")
call("run")
```

---

## upload

Upload a file via HTTP PUT.

> run "curl -s -X PUT --upload-file data.json https://api.example.com/upload"

```markscript
# Upload file
push("curl -s -X PUT --upload-file data.json https://api.example.com/upload")
call("run")
```

---

## websocket

Placeholder for WebSocket connections.

> print "WebSocket support requires native bridge"

```markscript
# WebSocket placeholder
push("WebSocket support requires native bridge")
call("print")
```

---

## serve

Start a simple HTTP server for static files.

> spawn "python -m http.server 8000"

```markscript
# Start a dev server
push("python -m http.server 8000")
call("spawn")
```
