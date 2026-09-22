# Cookie

HTTP cookie parsing, stringification, and manipulation for request/response handling.

## parse

Parse a `Cookie` header string into a key-value dict.

> print "Cookies parsed"

```markscript
let header = "session=abc123; theme=dark; lang=en-US"

let cookies = cookie.parse(header)
# {"session": "abc123", "theme": "dark", "lang": "en-US"}

> assert cookies["session"] "abc123"
> assert cookies["theme"] "dark"
```

## stringify

Convert a key-value dict into a `Cookie` header string.

> print "Cookie string built"

```markscript
let cookies = {}
cookies["session"] = "xyz789"
cookies["path"] = "/"
cookies["secure"] = "true"

let header = cookie.stringify(cookies)
# "session=xyz789; path=/; secure=true"

> assert header match "session=xyz789"
> assert header match "secure=true"
```

## get

Extract a single cookie value by name from a cookie header or dict.

> assert value expected

```markscript
let header = "token=eyJhbGciOiJIUzI1NiJ9; refresh=true"

let token = cookie.get(header, "token")
let missing = cookie.get(header, "nonexistent")

> assert token "eyJhbGciOiJIUzI1NiJ9"
> assert missing null
```

## set

Create a `Set-Cookie` header string with attributes.

> print "Set-Cookie header"

```markscript
let set_cookie = cookie.set("session", "abc123", {
  "Path": "/",
  "HttpOnly": true,
  "Secure": true,
  "Max-Age": 3600,
  "SameSite": "Lax"
})

# "session=abc123; Path=/; HttpOnly; Secure; Max-Age=3600; SameSite=Lax"

> run "echo 'Set-Cookie: " + set_cookie + "'"
```

## delete

Create a `Set-Cookie` header that expires a cookie immediately.

> print "Deleting cookie"

```markscript
let delete_cookie = cookie.delete("session", {
  "Path": "/",
  "Domain": "example.com"
})

# "session=; Path=/; Domain=example.com; Max-Age=0; Expires=Thu, 01 Jan 1970 00:00:00 GMT"

> assert delete_cookie match "session="
> assert delete_cookie match "Max-Age=0"
```

## parse_set_cookie

Parse a `Set-Cookie` header into its components: name, value, and attributes.

> print "Set-Cookie parsed"

```markscript
let header = "token=abc; Path=/; HttpOnly; Max-Age=86400; SameSite=Strict"

let parsed = cookie.parse_set_cookie(header)
# {
#   "name": "token",
#   "value": "abc",
#   "attributes": {
#     "Path": "/",
#     "HttpOnly": true,
#     "Max-Age": "86400",
#     "SameSite": "Strict"
#   }
# }

> assert parsed["name"] "token"
> assert parsed["attributes"]["HttpOnly"] true
> assert parsed["attributes"]["SameSite"] "Strict"
```

## jar

Maintain a cookie jar --- a dict of cookies that accumulates across responses.

> print "Cookie jar state"

```markscript
let jar = {}

# simulate receiving Set-Cookie headers
let c1 = cookie.parse_set_cookie("session=abc; Path=/")
jar = cookie.jar_set(jar, c1)

let c2 = cookie.parse_set_cookie("csrf=xyz; Path=/; HttpOnly")
jar = cookie.jar_set(jar, c2)

# build a Cookie header from the jar
let header = cookie.jar_header(jar, "/")
# "session=abc; csrf=xyz"

> assert jar["session"]["value"] "abc"
> assert jar["csrf"]["value"] "xyz"
```
