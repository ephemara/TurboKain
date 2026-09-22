# Base64

Base64 encoding, decoding, and URL-safe variants for binary data transport.

## encode

Encode a string to Base64.

> print "Encoded"

```markscript
let text = "Hello, World!"

let encoded = base64.encode(text)
# "SGVsbG8sIFdvcmxkIQ=="

> assert encoded "SGVsbG8sIFdvcmxkIQ=="
```

## decode

Decode a Base64 string back to the original text.

> print "Decoded"

```markscript
let encoded = "SGVsbG8sIFdvcmxkIQ=="

let decoded = base64.decode(encoded)
# "Hello, World!"

> assert decoded "Hello, World!"
```

## url_encode

Base64 URL-safe encoding: replaces `+` with `-`, `/` with `_`, and strips padding `=`.

> print "URL-safe encoded"

```markscript
let data = "Hello + World / 2026"

let encoded = base64.url_encode(data)
# "SGVsbG8gKyBXb3JsZCAvIDIwMjY"  -- no padding, safe chars

> assert base64.url_encode(">?") match "^[A-Za-z0-9_-]+$"
```

## url_decode

Decode a URL-safe Base64 string back to original text.

> print "URL-safe decoded"

```markscript
let url_encoded = "SGVsbG8sIFdvcmxkIQ"

let decoded = base64.url_decode(url_encoded)
# "Hello, World!"

> assert decoded "Hello, World!"
```

## validate

Check if a string is valid Base64. Returns `true` or `false`.

> assert result expected

```markscript
let valid = base64.validate("SGVsbG8=")
let no_padding = base64.validate("SGVsbG8")   # valid --- padding optional
let invalid = base64.validate("!!!invalid!!!")

> assert valid true
> assert no_padding true
> assert invalid false
```

## encode_file

Read a file and encode its contents to Base64.

> read file "image.png"

```markscript
let b64 = base64.encode_file("image.png")
# data URI ready string

> print "data:image/png;base64," + b64
```

## decode_to_file

Decode a Base64 string and write the result to a file.

> write file "decoded_output" content

```markscript
let b64 = "SGVsbG8sIFdvcmxkIQ=="

let written = base64.decode_to_file(b64, "output.txt")
# writes "Hello, World!" to output.txt

> assert written true
> assert file exists "output.txt"
```
