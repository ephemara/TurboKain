# String

Markscript string utilities -- manipulation, search, formatting.
Uses the markscript mini-language for character operations and the IVT
for printing and conversion.

---

## length

Get the length of a string.

> len "hello world"
> print result

```markscript
let s = "hello world"
push(s)
call("len")
# result = 11
```

---

## concat

Concatenate two strings.

> print "hello " + "world"

```markscript
let a = "hello "
let b = "world"
let result = a + b
# result = "hello world"
```

---

## repeat

Repeat a string N times using a loop.

```markscript
let base = "ha"
let times = 3
let result = ""
let i = 0
while i < times:
    result = result + base
    i = i + 1
# result = "hahaha"
```

---

## starts_with

Check if a string starts with a prefix.

```markscript
let text = "markdown rules"
let prefix = "mark"
let found = 0
# compare first N chars
```

---

## ends_with

Check if a string ends with a suffix.

```markscript
let text = "file.kn"
let suffix = ".kn"
let found = 0
# compare last N chars
```

---

## contains

Check if a string contains a substring.

```markscript
let text = "the quick brown fox"
let search = "brown"
let found = 0
# scan for substring match
```

---

## upper

Convert a string to uppercase (placeholder --- needs char-by-char).

> print "UPPERCASE"

```markscript
let text = "hello"
push("UPPER: " + text)
call("print")
```

---

## lower

Convert a string to lowercase (placeholder).

> print "lowercase"

```markscript
let text = "HELLO"
push("lower: " + text)
call("print")
```

---

## trim

Strip leading and trailing whitespace (placeholder).

```markscript
let text = "  padded  "
# trim whitespace from both ends
```

---

## split

Split a string by a delimiter (placeholder).

```markscript
let text = "a,b,c,d"
let delim = ","
# split into tokens
```
