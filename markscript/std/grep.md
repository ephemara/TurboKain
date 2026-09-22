# Grep

MarkScript text search -- find lines matching a pattern.
Wraps `grep` via the IVT for actual search operations.

---

## search

Search a file for a pattern and print matching lines.

> run "grep 'pattern' file.txt"

```markscript
let pattern = "error"
let file = "log.txt"
push("grep '" + pattern + "' " + file)
call("run")
# matches printed to stdout
```

---

## count

Count matching lines in a file.

> run "grep -c 'pattern' file.txt"

```markscript
let pattern = "TODO"
let file = "src/main.kn"
push("grep -c '" + pattern + "' " + file)
call("run")
# count printed to stdout
```

---

## recursive

Recursively search all files in a directory tree.

> run "grep -r 'pattern' dir/"

```markscript
let pattern = "function"
let dir = "src/"
push("grep -r '" + pattern + "' " + dir)
call("run")
# all matches with filenames
```

---

## invert

Show lines that do NOT match a pattern.

> run "grep -v 'pattern' file.txt"

```markscript
let pattern = "debug"
let file = "app.log"
push("grep -v '" + pattern + "' " + file)
call("run")
# all lines except debug lines
```

---

## case_insensitive

Search ignoring case.

> run "grep -i 'pattern' file.txt"

```markscript
let pattern = "warning"
let file = "server.log"
push("grep -i '" + pattern + "' " + file)
call("run")
# case-insensitive matches
```

---

## line_number

Show matching lines with their line numbers.

> run "grep -n 'pattern' file.txt"

```markscript
let pattern = "import"
let file = "main.kn"
push("grep -n '" + pattern + "' " + file)
call("run")
# "3:import std::io"
```

---

## context

Show matching lines with surrounding context lines.

> run "grep -C 3 'pattern' file.txt"

```markscript
let pattern = "panic"
let file = "crash.log"
let lines = 3
push("grep -C " + lines + " '" + pattern + "' " + file)
call("run")
# 3 lines before and after each match
```

---

## files_with_matches

List only filenames that contain a match.

> run "grep -l 'pattern' *.txt"

```markscript
let pattern = "config"
let files = "*.conf"
push("grep -l '" + pattern + "' " + files)
call("run")
# filenames only
```

---

## whole_word

Match only whole words.

> run "grep -w 'pattern' file.txt"

```markscript
let pattern = "class"
let file = "source.kn"
push("grep -w '" + pattern + "' " + file)
call("run")
# matches "class" but not "classify"
```
