# Find

MarkScript file location --- search files by name, type, size, time, and execute actions.
Wraps `find` via the IVT for filesystem traversal.

---

## by_name

Search for files by exact filename.

> run "find . -name 'file.txt'"

```markscript
let name = "config.json"
let dir = "."
push("find " + dir + " -name '" + name + "'")
call("run")
# all files named config.json
```

---

## by_pattern

Search for files matching a glob pattern.

> run "find . -name '*.kn'"

```markscript
let pattern = "*.kn"
let dir = "src/"
push("find " + dir + " -name '" + pattern + "'")
call("run")
# all Kain source files
```

---

## by_type_file

Search for regular files only.

> run "find . -type f -name '*.txt'"

```markscript
let pattern = "*.txt"
let dir = "."
push("find " + dir + " -type f -name '" + pattern + "'")
call("run")
# regular files matching pattern
```

---

## by_type_directory

Search for directories only.

> run "find . -type d"

```markscript
let dir = "."
push("find " + dir + " -type d")
call("run")
# all subdirectories
```

---

## by_type_symlink

Search for symbolic links.

> run "find . -type l"

```markscript
let dir = "."
push("find " + dir + " -type l")
call("run")
# all symbolic links
```

---

## by_size_plus

Search for files larger than N bytes.

> run "find . -size +1M"

```markscript
let size = "10M"
let dir = "."
push("find " + dir + " -type f -size +" + size)
call("run")
# files larger than 10MB
```

---

## by_size_minus

Search for files smaller than N bytes.

> run "find . -size -1K"

```markscript
let size = "1K"
let dir = "."
push("find " + dir + " -type f -size -" + size)
call("run")
# files smaller than 1KB
```

---

## by_size_exact

Search for files exactly N bytes.

> run "find . -size 1024c"

```markscript
let size = "1024c"
let dir = "."
push("find " + dir + " -type f -size " + size)
call("run")
# files exactly 1024 bytes
```

---

## by_mtime_newer

Search for files modified within the last N days.

> run "find . -mtime -7"

```markscript
let days = 7
let dir = "."
push("find " + dir + " -type f -mtime -" + days)
call("run")
# files modified in the last 7 days
```

---

## by_mtime_older

Search for files not modified in N days.

> run "find . -mtime +30"

```markscript
let days = 30
let dir = "."
push("find " + dir + " -type f -mtime +" + days)
call("run")
# files untouched for 30+ days
```

---

## by_minutes

Search for files modified within the last N minutes.

> run "find . -mmin -10"

```markscript
let minutes = 10
let dir = "."
push("find " + dir + " -type f -mmin -" + minutes)
call("run")
# files modified in the last 10 minutes
```

---

## exec_delete

Find and delete files matching criteria.

> run "find . -name '*.tmp' -delete"

```markscript
let pattern = "*.tmp"
let dir = "."
push("find " + dir + " -name '" + pattern + "' -delete")
call("run")
# all temp files deleted
```

---

## exec_command

Find and run a command on each file.

> run "find . -name '*.txt' -exec wc -l {} +"

```markscript
let pattern = "*.txt"
let dir = "."
push("find " + dir + " -name '" + pattern + "' -exec wc -l {} +")
call("run")
# word count on each text file
```

---

## exec_rename

Find and rename files by extension.

> run "find . -name '*.bak' -exec mv {} {}.old \;"

```markscript
let pattern = "*.bak"
let dir = "."
push("find " + dir + " -name '" + pattern + "' -exec sh -c 'mv \"$1\" \"$1.old\"' _ {} \\;")
call("run")
# appends .old to each .bak file
```

---

## maxdepth

Limit search depth in directory tree.

> run "find . -maxdepth 3 -name '*.kn'"

```markscript
let depth = 3
let pattern = "*.kn"
let dir = "."
push("find " + dir + " -maxdepth " + depth + " -name '" + pattern + "'")
call("run")
# only 3 levels deep
```

---

## print0

Output filenames separated by NUL for piping to xargs.

> run "find . -name '*.log' -print0"

```markscript
let pattern = "*.log"
let dir = "."
push("find " + dir + " -name '" + pattern + "' -print0")
call("run")
# NUL-separated for safe xargs
```

---

## newest

Find the most recently modified file in a directory.

> run "find . -type f -printf '%T@ %p\\n' | sort -n | tail -1"

```markscript
let dir = "."
push("find " + dir + " -type f -printf '%T@ %p\\n' | sort -n | tail -1")
call("run")
# path of newest file
```
