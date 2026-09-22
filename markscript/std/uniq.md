# Uniq

MarkScript duplicate detection -- filter, count, report repeated lines.
Wraps `uniq` via the IVT for adjacent duplicate operations.

---

## unique

Output only unique lines (removes adjacent duplicates).

> run "uniq file.txt"

```markscript
let file = "lines.txt"
push("uniq " + file)
call("run")
# adjacent duplicates removed
```

---

## sorted_unique

Find unique lines from a sorted file.

> run "sort file.txt | uniq"

```markscript
let file = "words.txt"
push("sort " + file + " | uniq")
call("run")
# globally unique lines
```

---

## count

Count occurrences of each unique line.

> run "uniq -c file.txt"

```markscript
let file = "visits.log"
push("uniq -c " + file)
call("run")
# "   42 Monday"
```

---

## sorted_count

Count unique occurrences from a sorted file.

> run "sort file.txt | uniq -c"

```markscript
let file = "errors.log"
push("sort " + file + " | uniq -c | sort -rn")
call("run")
# sorted by frequency, highest first
```

---

## repeated

Show only lines that appear more than once.

> run "uniq -d file.txt"

```markscript
let file = "dupes.txt"
push("uniq -d " + file)
call("run")
# only duplicated lines
```

---

## all_repeated

Show all copies of repeated lines.

> run "uniq -D file.txt"

```markscript
let file = "all_dupes.txt"
push("uniq -D " + file)
call("run")
# all duplicate lines printed
```

---

## unique_only

Show only lines that appear exactly once.

> run "uniq -u file.txt"

```markscript
let file = "singletons.txt"
push("uniq -u " + file)
call("run")
# lines that never repeat
```

---

## skip_fields

Skip N fields before duplicate comparison.

> run "uniq -f 2 file.txt"

```markscript
let fields = 2
let file = "data.txt"
push("uniq -f " + fields + " " + file)
call("run")
# first 2 whitespace-delimited fields ignored
```

---

## skip_chars

Skip N characters before duplicate comparison.

> run "uniq -s 5 file.txt"

```markscript
let chars = 5
let file = "timestamped.txt"
push("uniq -s " + chars + " " + file)
call("run")
# first 5 characters ignored
```

---

## check_chars

Only compare the first N characters.

> run "uniq -w 3 file.txt"

```markscript
let chars = 3
let file = "codes.txt"
push("uniq -w " + chars + " " + file)
call("run")
# only first 3 chars matter
```

---

## group

Display duplicate groups separated by blank lines.

> run "uniq --group file.txt"

```markscript
let file = "grouped.txt"
push("uniq --group " + file)
call("run")
# groups separated by blank line
```

---

## case_insensitive

Compare ignoring case.

> run "uniq -i file.txt"

```markscript
let file = "mixed.txt"
push("uniq -i " + file)
call("run")
# "Hello" and "hello" treated as duplicate
```
