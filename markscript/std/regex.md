# Regex

MarkScript regular expressions - match, search, replace, split, groups.
Wraps standard regex tools via the IVT for pattern operations.

---

## match

Check if a pattern exists in text and print matches.

> run "grep -o 'pattern' file.txt"

```markscript
let pattern = "[0-9]+\\.[0-9]+"
let file = "versions.txt"
push("grep -oE '" + pattern + "' " + file)
call("run")
# all version numbers extracted
```

---

## find_all

Find all occurrences of a pattern, one per line.

> run "grep -oE 'pattern' file.txt"

```markscript
let pattern = "\\w+@\\w+\\.\\w+"
let file = "contacts.txt"
push("grep -oE '" + pattern + "' " + file)
call("run")
# all email addresses
```

---

## replace

Substitute regex matches with replacement text.

> run "sed -E 's/pattern/replacement/g' file.txt"

```markscript
let pattern = "([0-9]{4})-([0-9]{2})-([0-9]{2})"
let repl = "\\3/\\2/\\1"
let file = "dates.txt"
push("sed -E 's/" + pattern + "/" + repl + "/g' " + file)
call("run")
# ISO dates to DD/MM/YYYY
```

---

## split

Split text on a regex delimiter.

> run "awk -F'[,\\t]' '{print $1}' file.txt"

```markscript
let sep = "[,\\t|]"
let file = "mixed.txt"
push("awk -F'" + sep + "' '{for(i=1;i<=NF;i++) print $i}' " + file)
call("run")
# split on comma, tab, or pipe
```

---

## groups

Extract regex capture groups.

> run "sed -E 's/([^:]+): ([0-9]+)/\\1 -> \\2/' file.txt"

```markscript
let file = "pairs.txt"
push("sed -E 's/([^:]+): ([0-9]+)/Label: \\1, Value: \\2/' " + file)
call("run")
# extracts label and value groups
```

---

## flags

Use regex flags for case-insensitive, multiline, etc.

> run "grep -iE 'pattern' file.txt"

```markscript
let pattern = "error|warning|fatal"
let file = "app.log"
push("grep -iE '" + pattern + "' " + file)
call("run")
# case-insensitive match of any level
```

---

## multiline

Match patterns across multiple lines using pcregrep.

> run "pcregrep -M 'start\\n.*end' file.txt"

```markscript
let pattern = "function \\w+\\(\\n[^}]+\\n}"
let file = "source.kn"
push("pcregrep -M '" + pattern + "' " + file)
call("run")
# multi-line function bodies
```

---

## word_boundary

Match only at word boundaries.

> run "grep -E '\\bpattern\\b' file.txt"

```markscript
let pattern = "\\bcat\\b"
let file = "animals.txt"
push("grep -E '" + pattern + "' " + file)
call("run")
# matches "cat" but not "caterpillar"
```

---

## line_start_end

Match patterns anchored to start or end of line.

> run "grep -E '^import' file.txt"

```markscript
let anchor = "^import"
let file = "code.kn"
push("grep -E '" + anchor + "' " + file)
call("run")
# lines starting with import
```

---

## validate

Validate that text matches an expected pattern.

> run "grep -E '^[a-zA-Z0-9_]+$' file.txt"

```markscript
let pattern = "^[a-zA-Z0-9_]+$"
let file = "identifiers.txt"
push("grep -vE '" + pattern + "' " + file)
call("run")
# lines that do NOT match = invalid identifiers
```
