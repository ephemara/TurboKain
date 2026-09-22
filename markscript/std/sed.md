# Sed

MarkScript stream editor -- search, replace, insert, delete lines.
Wraps `sed` via the IVT for text transformations.

---

## substitute

Replace first occurrence of a pattern per line.

> run "sed 's/old/new/' file.txt"

```markscript
let old = "foo"
let new = "bar"
let file = "data.txt"
push("sed 's/" + old + "/" + new + "/' " + file)
call("run")
# first match per line replaced
```

---

## substitute_all

Replace all occurrences of a pattern on each line (global).

> run "sed 's/old/new/g' file.txt"

```markscript
let old = "  "
let new = " "
let file = "spaced.txt"
push("sed 's/" + old + "/" + new + "/g' " + file)
call("run")
# all matches on each line replaced
```

---

## delete_line

Delete lines matching a pattern.

> run "sed '/pattern/d' file.txt"

```markscript
let pattern = "^#"
let file = "config.cfg"
push("sed '/" + pattern + "/d' " + file)
call("run")
# all comment lines removed
```

---

## delete_line_by_number

Delete a specific line number.

> run "sed '5d' file.txt"

```markscript
let line = 5
let file = "list.txt"
push("sed '" + line + "d' " + file)
call("run")
# line 5 removed
```

---

## append_after

Append a line after every match.

> run "sed '/pattern/a\\new line' file.txt"

```markscript
let pattern = "[end]"
let append = "---"
let file = "notes.md"
push("sed '/" + pattern + "/a\\\\" + append + "' " + file)
call("run")
```

---

## insert_before

Insert a line before every match.

> run "sed '/pattern/i\\new line' file.txt"

```markscript
let pattern = "CHAPTER"
let line = "===="
let file = "book.md"
push("sed '/" + pattern + "/i\\\\" + line + "' " + file)
call("run")
```

---

## replace_line

Replace entire matching lines.

> run "sed '/pattern/c\\replacement' file.txt"

```markscript
let pattern = "old_config"
let repl = "new_config=1"
let file = "settings.ini"
push("sed '/" + pattern + "/c\\\\" + repl + "' " + file)
call("run")
```

---

## in_place

Edit a file directly (no backup).

> run "sed -i 's/old/new/g' file.txt"

```markscript
let old = "copyright 2025"
let new = "copyright 2026"
let file = "LICENSE"
push("sed -i 's/" + old + "/" + new + "/g' " + file)
call("run")
# file modified in-place
```

---

## in_place_backup

Edit in-place with a backup file.

> run "sed -i.bak 's/old/new/g' file.txt"

```markscript
let old = "version 1.0"
let new = "version 2.0"
let file = "README.md"
push("sed -i.bak 's/" + old + "/" + new + "/g' " + file)
call("run")
# README.md.bak preserved
```

---

## multiple_edits

Apply multiple sed expressions.

> run "sed -e 's/a/A/' -e 's/b/B/' file.txt"

```markscript
let file = "letters.txt"
push("sed -e 's/a/A/' -e 's/b/B/' -e 's/c/C/' " + file)
call("run")
# all three substitutions applied
```

---

## print_lines

Print specific line ranges.

> run "sed -n '10,20p' file.txt"

```markscript
let start = 10
let end = 20
let file = "data.csv"
push("sed -n '" + start + "," + end + "p' " + file)
call("run")
# lines 10 through 20 only
```

---

## quit_after

Print lines until a match, then quit.

> run "sed '/STOP/q' file.txt"

```markscript
let stop = "ERROR"
let file = "build.log"
push("sed '/" + stop + "/q' " + file)
call("run")
# prints lines up to first ERROR
```
