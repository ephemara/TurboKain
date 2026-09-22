# Markdown

Markdown parsing, rendering, inspection, and metadata extraction.

## parse

Parse a Markdown string into an AST: list of block objects with type, content, depth.

> run "python -c \"import markdown; ...\""

```markscript
let md_text = `
# Title

Hello world.

- item 1
- item 2

> A blockquote
`

let ast = markdown.parse(md_text)
# ast = [
#   {"type": "heading", "level": 1, "content": "Title"},
#   {"type": "paragraph", "content": "Hello world."},
#   {"type": "list", "ordered": false, "items": ["item 1", "item 2"]},
#   {"type": "blockquote", "content": "A blockquote"}
# ]

> assert ast[0]["type"] "heading"
> assert ast[0]["level"] 1
```

## render

Convert a Markdown AST back into a formatted Markdown string.

> write file "output.md" content

```markscript
let ast = []
ast[0] = {"type": "heading", "level": 2, "content": "Chapter 1"}
ast[1] = {"type": "paragraph", "content": "Once upon a time..."}
ast[2] = {"type": "code", "language": "markscript", "content": "let x = 5"}

let md = markdown.render(ast)
# ## Chapter 1
#
# Once upon a time...
#
# ```markscript
# let x = 5
# ```

> write file "chapter1.md" md
```

## toc

Extract a table of contents from a Markdown string: all headings with their levels.

> print "TOC generated"

```markscript
let md_text = `
# Introduction
## Installation
## Quick Start
# API Reference
## Endpoints
### GET /users
### POST /users
`

let toc = markdown.toc(md_text)
# [
#   {"title": "Introduction", "level": 1},
#   {"title": "Installation", "level": 2},
#   {"title": "Quick Start", "level": 2},
#   {"title": "API Reference", "level": 1},
#   {"title": "Endpoints", "level": 2},
#   {"title": "GET /users", "level": 3},
#   {"title": "POST /users", "level": 3}
# ]

> assert toc[3]["title"] "API Reference"
```

## frontmatter

Extract YAML frontmatter between `---` markers at the start of a document.

> run "python -c \"... frontmatter ...\""

```markscript
let md_text = `---
title: My Post
date: 2026-06-10
tags: [markscript, stdlib]
---

# Actual Content

The body starts here.
`

let fm = markdown.frontmatter(md_text)
# {"title": "My Post", "date": "2026-06-10", "tags": ["markscript", "stdlib"]}

> assert fm["title"] "My Post"
> assert fm["tags"][0] "markscript"
```

## links

Extract all hyperlinks from a Markdown document as `[{"text": "...", "url": "..."}]`.

> print "Links found"

```markscript
let md_text = `
See the [docs](https://docs.example.com) for more.
Email [support](mailto:help@example.com) or visit [home](/) for info.
`

let links = markdown.links(md_text)
# [
#   {"text": "docs", "url": "https://docs.example.com"},
#   {"text": "support", "url": "mailto:help@example.com"},
#   {"text": "home", "url": "/"}
# ]

> assert links[0]["url"] "https://docs.example.com"
```

## code_blocks

Extract all fenced code blocks with their language tags.

> run "python -c \"... markdown ...\""

```markscript
let md_text = `
Some text.

\`\`\`python
print("hello")
\`\`\`

More text.

\`\`\`markscript
let x = 1
let y = x + 2
\`\`\`
`

let blocks = markdown.code_blocks(md_text)
# [
#   {"language": "python", "content": "print(\"hello\")"},
#   {"language": "markscript", "content": "let x = 1\nlet y = x + 2\n"}
# ]

> assert blocks[0]["language"] "python"
> assert blocks[1]["language"] "markscript"
```

## strip

Remove all Markdown formatting, returning plain text only.

> print "Plain text extracted"

```markscript
let md_text = "**Bold** and *italic* and `code` and [link](http://x.com)"

let plain = markdown.strip(md_text)
# "Bold and italic and code and link"

> assert plain "Bold and italic and code and link"
```
