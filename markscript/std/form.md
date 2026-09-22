# Form

Form data encoding: URL-encoded form bodies and multipart form data.

## urlencode

Encode a key-value dict as `application/x-www-form-urlencoded` body.

> print "Form body generated"

```markscript
let fields = {}
fields["username"] = "alice"
fields["password"] = "s3cret!"
fields["remember"] = "true"

let body = form.urlencode(fields)
# "username=alice&password=s3cret%21&remember=true"

> assert body match "username=alice"
> assert body match "password=s3cret%21"
```

## multipart

Construct a multipart/form-data boundary-delimited body from fields and optional files.

> run "curl -X POST -F ..."

```markscript
let payload = {}
payload["fields"] = {}
payload["fields"]["name"] = "Alice"
payload["fields"]["email"] = "alice@x.com"

payload["files"] = {}
payload["files"]["avatar"] = {"filename": "pic.jpg", "content_type": "image/jpeg", "data": b64decode("...")}

let boundary = "----FormBoundary7MA4YWxk"
let body = form.multipart(payload, boundary)
# -- ----FormBoundary7MA4YWxk
# Content-Disposition: form-data; name="name"
# 
# Alice
# -- ----FormBoundary7MA4YWxk
# Content-Disposition: form-data; name="avatar"; filename="pic.jpg"
# Content-Type: image/jpeg
# 
# ...binary data...
# -- ----FormBoundary7MA4YWxk--

> run "curl -X POST -H 'Content-Type: multipart/form-data; boundary=----FormBoundary7MA4YWxk' -d @- http://localhost:8080/upload"
```

## parse

Parse a URL-encoded form body string into a key-value dict.

> print "Parsed form"

```markscript
let body = "name=Bob&role=admin&enabled=true"

let fields = form.parse(body)
# {"name": "Bob", "role": "admin", "enabled": "true"}

> assert fields["name"] "Bob"
> assert fields["role"] "admin"
```

## build_field

Create a single form field entry for use in multipart building.

> print "Field built"

```markscript
let field = form.build_field("description", "Hello World")
# {"name": "description", "value": "Hello World"}

let file_field = form.build_field("resume", {"filename": "resume.pdf", "content_type": "application/pdf", "data": "%PDF..."})
# {"name": "resume", "filename": "resume.pdf", "content_type": "application/pdf", "data": "%PDF..."}

> assert field["value"] "Hello World"
> assert file_field["filename"] "resume.pdf"
```

## detect_type

Detect the MIME content type of a form field based on filename extension.

> assert type expected

```markscript
> assert form.detect_type("photo.jpg") "image/jpeg"
> assert form.detect_type("doc.pdf") "application/pdf"
> assert form.detect_type("data.json") "application/json"
> assert form.detect_type("script.js") "application/javascript"
> assert form.detect_type("file.txt") "text/plain"
```
