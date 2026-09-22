# Wc

MarkScript word count -- count lines, words, characters, bytes in files.
Wraps `wc` via the IVT for file statistics.

---

## default

Count lines, words, and characters in a file.

> run "wc file.txt"

```markscript
let file = "document.txt"
push("wc " + file)
call("run")
# "  42  350  2100 file.txt"
```

---

## lines

Count only the number of lines.

> run "wc -l file.txt"

```markscript
let file = "code.kn"
push("wc -l " + file)
call("run")
# line count only
```

---

## words

Count only the number of words.

> run "wc -w file.txt"

```markscript
let file = "essay.txt"
push("wc -w " + file)
call("run")
# word count only
```

---

## chars

Count only the number of characters.

> run "wc -m file.txt"

```markscript
let file = "unicode.txt"
push("wc -m " + file)
call("run")
# character count (multibyte aware)
```

---

## bytes

Count only the number of bytes.

> run "wc -c file.txt"

```markscript
let file = "binary.dat"
push("wc -c " + file)
call("run")
# byte count
```

---

## max_line_length

Find the maximum line length in a file.

> run "wc -L file.txt"

```markscript
let file = "code.kn"
push("wc -L " + file)
call("run")
# length of longest line
```

---

## multiple_files

Count lines for multiple files in a single command.

> run "wc -l file1.txt file2.txt file3.txt"

```markscript
let files = "src/*.kn"
push("wc -l " + files)
call("run")
# per-file line counts plus total
```

---

## files_recursive

Count lines recursively across directories.

> run "find src/ -name '*.kn' -exec wc -l {} +"

```markscript
let pattern = "*.kn"
let dir = "src/"
push("find " + dir + " -name '" + pattern + "' -exec wc -l {} +")
call("run")
# total for all matching files
```

---

## total_only

Show only the total for multiple files.

> run "wc -l --total=only file1.txt file2.txt"

```markscript
let files = "*.log"
push("wc -l --total=only " + files)
call("run")
# combined total only
```

---

## compare_files

Compare line counts of two files.

> run "wc -l file1.txt file2.txt"

```markscript
let a = "original.txt"
let b = "modified.txt"
push("wc -l " + a + " " + b)
call("run")
# compare line counts
```

---

## code_metrics

Count lines of code, comments, and blanks.

> run "wc -l -w -c *.kn"

```markscript
let files = "*.kn"
push("wc -l -w -c " + files)
call("run")
# lines, words, bytes for all Kain files
```

---

## all_stats

Get all statistics (lines, words, chars, bytes) for a file.

> run "wc -l -w -m -c file.txt"

```markscript
let file = "complete_stats.txt"
push("wc -l -w -m -c " + file)
call("run")
# full statistics output
```
