# LexerComprehensiveTest

This file exercises every token type in the upgraded lexer.

## headings

# Header 1
## Header 2
### Header 3
#### Header 4
##### Header 5
###### Header 6

## fenced_code_block

```kain
fn hello():
    println("hello world")
```

```python
def hello():
    print("hello world")
```

```
raw code block with no language tag
```

## blockquotes

> This is a blockquote.
> It continues on the next line.

## tables

| Name  | Value |
|-------|-------|
| Alpha | 100   |
| Beta  | 200   |

## lists

- unordered item one
- unordered item two
* asterisk list item
* another asterisk item
+ plus list item
1. ordered item one
2. ordered item two
3. ordered item three

## horizontal_rules

---

***

___

## mixed_content

Paragraph with **bold text** and *italic text* and `inline code`.

This paragraph has a [link](https://example.com) in it.

- list item with **bold** and *italic*
- another item

> blockquote with a code block:
>
> ```js
> console.log("hello")
> ```

## setext_style_headers

This text is followed by a setext heading
---

But this paragraph has content that is not a heading.

Another paragraph.

## Empty content after various markers

<!-- This comment has `backtick` and **bold** but we don't parse HTML comments -->

The end.
