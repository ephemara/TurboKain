# XML

XML document parsing, building, querying, and transformation routines.

## parse

Parse an XML string into a tree structure of nested dicts with `@attributes`, `#text`, and child element keys.

> run "python -c \"import xml.etree.ElementTree as ET; ...\""

```markscript
let xml_text = `<root><item id="1">Apple</item><item id="2">Banana</item></root>`

let tree = xml.parse(xml_text)
# tree = {
#   "root": {
#     "item": [
#       {"@attributes": {"id": "1"}, "#text": "Apple"},
#       {"@attributes": {"id": "2"}, "#text": "Banana"}
#     ]
#   }
# }

> assert tree["root"]["item"][0]["#text"] "Apple"
```

## build

Construct an XML string from a MarkScript tree.

> print "Generated XML"

```markscript
let doc = {}
doc["catalog"] = {}
doc["catalog"]["book"] = []
doc["catalog"]["book"][0] = {"@attributes": {"isbn": "123"}, "#text": "Kain Guide"}
doc["catalog"]["book"][1] = {"@attributes": {"isbn": "456"}, "#text": "MarkScript Ref"}

let out = xml.build(doc, {"pretty": true})
# <catalog>
#   <book isbn="123">Kain Guide</book>
#   <book isbn="456">MarkScript Ref</book>
# </catalog>

> write file "catalog.xml" out
```

## xpath

Evaluate a simple XPath expression against a parsed XML tree.

> run "python -c \"... lxml ... xpath ...\""

```markscript
let xml_text = `<data><person><name>Alice</name><age>30</age></person></data>`
let tree = xml.parse(xml_text)

let names = xml.xpath(tree, "//person/name")
# ["Alice"]

> assert names[0] "Alice"
```

## validate

Check if an XML string is well-formed. Optionally validate against a DTD or XSD.

> run "python -c \"import xml.etree.ElementTree as ET; ...\""

```markscript
let well_formed = xml.validate(`<root><child/></root>`)
let broken = xml.validate(`<root><child></root>`)

> assert well_formed true
> assert broken false
```

## transform

Apply an XSLT-like transformation: given a source tree and a template tree, produce a new XML tree.

> run "python -c \"... xml.etree.ElementTree ... transform ...\""

```markscript
let src = xml.parse(`<items><item>a</item><item>b</item></items>`)

# template: wrap each item in <wrapper>
let tpl = {
  "wrapper": {
    "item": {"#text": "{{ . }}"}
  }
}

let result = xml.transform(src, tpl)
# <wrapper><item>a</item><item>b</item></wrapper>

> print xml.build(result)
```

## get_element

Get the first element matching a tag name from a parsed tree.

> print "Found element"

```markscript
let tree = xml.parse(`<config><db host="localhost" port="5432"/></config>`)

let db = xml.get_element(tree, "db")
> assert db["@attributes"]["host"] "localhost"
> assert db["@attributes"]["port"] "5432"
```

## list_tags

Return all unique tag names present in the document.

> run "python -c \"import xml.etree.ElementTree as ET; tags = set(...)\""

```markscript
let tree = xml.parse(`<root><a/><b><c/></b><a/></root>`)

let tags = xml.list_tags(tree)
# ["root", "a", "b", "c"]

> assert tags[1] "a"
```
