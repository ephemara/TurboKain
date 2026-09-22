# Head

MarkScript file prefix - read the beginning of files.
Wraps `head` via the IVT for top-of-file extraction.

---

## lines

Show the first N lines of a file.

> run "head -n 10 file.txt"

```markscript
let n = 10
let file = "data.txt"
push("head -n " + n + " " + file)
call("run")
# first 10 lines
```

---

## first_line

Show only the first line.

> run "head -n 1 file.txt"

```markscript
let file = "header.csv"
push("head -n 1 " + file)
call("run")
# first line only
```

---

## bytes_count

Show the first N bytes of a file.

> run "head -c 100 file.txt"

```markscript
let n = 100
let file = "binary.dat"
push("head -c " + n + " " + file)
call("run")
# first 100 bytes
```

---

## multiple_files

Show the first lines of multiple files with headers.

> run "head -n 5 file1.txt file2.txt"

```markscript
let n = 5
let files = "chapter1.md chapter2.md"
push("head -n " + n + " " + files)
call("run")
# "==> chapter1.md <==" header before each
```

---

## quiet

Show head of multiple files without filename headers.

> run "head -q -n 3 *.txt"

```markscript
let n = 3
let files = "*.txt"
push("head -q -n " + n + " " + files)
call("run")
# no filename headers, just content
```

---

## verbose

Show head of multiple files with explicit headers.

> run "head -v -n 3 file.txt"

```markscript
let n = 3
let file = "single.txt"
push("head -v -n " + n + " " + file)
call("run")
# header even for a single file
```

---

## negative_lines

Show all lines except the last N.

> run "head -n -5 file.txt"

```markscript
let exclude = 5
let file = "log.txt"
push("head -n -" + exclude + " " + file)
call("run")
# everything except last 5 lines
```

---

## pipe

Use head in a pipeline to limit output.

> run "grep 'error' log.txt | head -n 20"

```markscript
let pattern = "error"
let file = "big.log"
let n = 20
push("grep '" + pattern + "' " + file + " | head -n " + n)
call("run")
# first 20 matching lines
```

---

## null_terminated

Read NUL-terminated records instead of newlines.

> run "head -z -n 5 file.txt"

```markscript
let n = 5
let file = "records.txt"
push("head -z -n " + n + " " + file)
call("run")
# null-terminated records
```

---

## preview

Show a quick preview (first 3 lines + byte count).

> run "head -n 3 file.txt && wc -l file.txt"

```markscript
let file = "unknown.txt"
push("head -n 3 " + file + " && echo '---' && wc -l " + file)
call("run")
# preview + line count
```

---

## section_extract

Extract a section from a file using head and tail.

> run "head -n 50 file.txt | tail -n 10"

```markscript
let file = "large.txt"
let end_line = 50
let section_size = 10
push("head -n " + end_line + " " + file + " | tail -n " + section_size)
call("run")
# lines 41-50 of the file
```
