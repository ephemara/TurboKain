# HTML

HTML parsing, building, selection, escaping, and table construction.

## parse

Parse an HTML string into a DOM-like tree of nested dicts.

> run "python -c \"from html.parser import HTMLParser; ...\""

```markscript
let html_text = `<div class="container"><h1>Title</h1><p>Hello</p></div>`

let dom = html.parse(html_text)
# dom = {
#   "tag": "div",
#   "attributes": {"class": "container"},
#   "children": [
#     {"tag": "h1", "attributes": {}, "children": ["Title"]},
#     {"tag": "p", "attributes": {}, "children": ["Hello"]}
#   ]
# }

> assert dom["tag"] "div"
> assert dom["children"][0]["tag"] "h1"
```

## build

Construct an HTML string from a MarkScript tree.

> write file "page.html" content

```markscript
let page = {}
page["tag"] = "html"
page["children"] = []
page["children"][0] = {"tag": "head", "children": [{"tag": "title", "children": ["My Page"]}]}
page["children"][1] = {"tag": "body", "children": [
  {"tag": "h1", "attributes": {"class": "title"}, "children": ["Hello"]},
  {"tag": "p", "children": ["World"]}
]}

let out = html.build(page, {"pretty": true})
# <html>
#   <head>
#     <title>My Page</title>
#   </head>
#   <body>
#     <h1 class="title">Hello</h1>
#     <p>World</p>
#   </body>
# </html>

> write file "page.html" out
```

## select

Find all elements matching a CSS selector. Returns a list of element trees.

> run "python -c \"from bs4 import BeautifulSoup; ...\""

```markscript
let html_text = `<div><p class="note">A</p><p class="note urgent">B</p><p>C</p></div>`

let dom = html.parse(html_text)

# select all <p> tags with class "note"
let notes = html.select(dom, "p.note")
> assert html.length(notes) 2

# select the urgent note
let urgent = html.select(dom, ".urgent")
> assert urgent[0]["children"][0] "B"
```

## table_to_html

Convert a MarkScript table (list of dicts) into an HTML `<table>` string.

> write file "table.html" content

```markscript
let rows = [
  {"Name": "Alice", "Role": "Admin", "Status": "Active"},
  {"Name": "Bob", "Role": "User", "Status": "Active"},
  {"Name": "Carol", "Role": "User", "Status": "Inactive"}
]

let table_html = html.table_to_html(rows, {"class": "data-table", "id": "users"})
# <table class="data-table" id="users">
#   <thead><tr><th>Name</th><th>Role</th><th>Status</th></tr></thead>
#   <tbody>
#     <tr><td>Alice</td><td>Admin</td><td>Active</td></tr>
#     ...
#   </tbody>
# </table>

> write file "users-table.html" table_html
```

## escape

Escape HTML special characters (`&`, `<`, `>`, `"`, `'`) for safe embedding.

> print "Escaped string"

```markscript
let raw = "<script>alert('xss')</script> & \"quoted\""

let safe = html.escape(raw)
# &lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt; &amp; &quot;quoted&quot;

> assert html.escape("<") "&lt;"
> assert html.escape("&") "&amp;"
```

## unescape

Reverse HTML entity encoding back to plain text.

> print "Unescaped string"

```markscript
let escaped = "&lt;bold&gt;Text &amp; more&lt;/bold&gt;"

let plain = html.unescape(escaped)
# <bold>Text & more</bold>

> assert plain "<bold>Text & more</bold>"
```

## strip_tags

Remove all HTML tags, returning only the text content.

> print "Plain text extracted"

```markscript
let html_text = "<p>Hello <b>world</b>!</p><ul><li>One</li><li>Two</li></ul>"

let text = html.strip_tags(html_text)
# "Hello world! One Two"

> assert text "Hello world! One Two"
```
