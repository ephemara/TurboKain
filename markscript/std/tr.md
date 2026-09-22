# Tr

MarkScript character translation --- translate, delete, squeeze characters.
Wraps `tr` via the IVT for character-level transformations.

---

## translate

Replace one set of characters with another.

> run "tr 'abc' 'xyz' < file.txt"

```markscript
let from = "abc"
let to = "xyz"
let file = "input.txt"
push("tr '" + from + "' '" + to + "' < " + file)
call("run")
# a->x, b->y, c->z
```

---

## uppercase

Convert all lowercase letters to uppercase.

> run "tr 'a-z' 'A-Z' < file.txt"

```markscript
let file = "lower.txt"
push("tr 'a-z' 'A-Z' < " + file)
call("run")
# "hello" -> "HELLO"
```

---

## lowercase

Convert all uppercase letters to lowercase.

> run "tr 'A-Z' 'a-z' < file.txt"

```markscript
let file = "UPPER.txt"
push("tr 'A-Z' 'a-z' < " + file)
call("run")
# "HELLO" -> "hello"
```

---

## delete

Delete specific characters from the input.

> run "tr -d 'aeiou' < file.txt"

```markscript
let chars = "aeiou"
let file = "vowels.txt"
push("tr -d '" + chars + "' < " + file)
call("run")
# removes all vowels
```

---

## delete_complement

Delete all characters EXCEPT those specified.

> run "tr -dc '0-9' < file.txt"

```markscript
let keep = "0-9"
let file = "mixed.txt"
push("tr -dc '" + keep + "' < " + file)
call("run")
# only digits survive
```

---

## squeeze

Squeeze repeated characters into single occurrences.

> run "tr -s ' ' < file.txt"

```markscript
let char = " "
let file = "spaced.txt"
push("tr -s '" + char + "' < " + file)
call("run")
# "hello     world" -> "hello world"
```

---

## squeeze_and_translate

Squeeze then translate in one pass.

> run "tr -s 'a-z' 'A-Z' < file.txt"

```markscript
let squeeze = "a-z"
let map = "A-Z"
let file = "noisy.txt"
push("tr -s '" + squeeze + "' '" + map + "' < " + file)
call("run")
# squeeze lowercase then uppercase
```

---

## complement

Translate everything EXCEPT the specified set.

> run "tr -c 'a-zA-Z' '\n' < file.txt"

```markscript
let keep = "a-zA-Z"
let repl = "\\n"
let file = "words.txt"
push("tr -c '" + keep + "' '" + repl + "' < " + file)
call("run")
# replaces non-letters with newlines
```

---

## character_class

Use POSIX character classes for translation.

> run "tr '[:lower:]' '[:upper:]' < file.txt"

```markscript
let from_class = "[:lower:]"
let to_class = "[:upper:]"
let file = "text.txt"
push("tr '" + from_class + "' '" + to_class + "' < " + file)
call("run")
# using POSIX classes
```

---

## delete_class

Delete all characters matching a class.

> run "tr -d '[:punct:]' < file.txt"

```markscript
let class = "[:punct:]"
let file = "punctuated.txt"
push("tr -d '" + class + "' < " + file)
call("run")
# removes !,.,?,- etc.
```

---

## squeeze_newlines

Collapse multiple blank lines into one.

> run "tr -s '\n' < file.txt"

```markscript
let file = "double_spaced.txt"
push("tr -s '\\n' < " + file)
call("run")
# consecutive blank lines reduced to one
```

---

## hex_to_upper

Convert lowercase hex digits to uppercase.

> run "tr 'a-f' 'A-F' < file.txt"

```markscript
let file = "hex_values.txt"
push("tr 'a-f' 'A-F' < " + file)
call("run")
# "ff00aa" -> "FF00AA"
```
