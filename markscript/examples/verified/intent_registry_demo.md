# Intent Registry Demo

Demonstrates the data-driven intent keyword registry (std/intents.md).
Known intents dispatch to handlers. Unknown words are treated as prose.
Uses both blockquote intents AND markscript mini-language function calls.

---

## Blockquote Intents (Single-Word Dispatch)

### String Operations

> print "hello from the intent registry"
> concat "hello " "world"
> upper "make this uppercase"
> lower "MAKE THIS LOWERCASE"
> trim "  padded text  "

### File I/O

> write ".mks_reg_demo.txt" "registry test content"
> read ".mks_reg_demo.txt"

### Math (single-arg)

> sin 1
> cos 0
> sqrt 25
> abs -42

---

## Multi-Arg via Markscript Mini-Language

For complex operations, use the ```markscript fenced blocks:

```markscript
print(min(10, 20))
print(max(10, 20))
print(clamp(50, 0, 100))
print(split("a,b,c", ","))
print(join("-", "x", "y", "z"))
print(substr("hello world", 0, 5))
print(replace("hello world", "world", "registry"))
print(contains("hello world", "world"))
print(random(1, 100))
```

---

## Prose Blockquotes (NOT Dispatched)

These start with prose-starter words -- they produce zero bytecode:

> This is documentation about the registry system.
> The intent keyword registry holds 57 single-word intents.
> Each intent maps to a handler function in bridge.kn.
> When the parser sees a blockquote, it checks the first word.
> If the first word is a known keyword, it dispatches as an intent.
> It describes how the data-driven approach works.

---

## Mix: Intent After Prose

> print "intent after prose works"

---

## Verify

```markscript
let cwd = cwd()
let fpath = concat(cwd, "/.mks_reg_demo.txt")
let content = read(fpath)
print(concat("Registry demo: ", content))
```
