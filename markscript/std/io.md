# IO

Markscript file I/O - read, write, check existence, list directories.
Every intent dispatches through the IVT to Kain's `std::fs` bridge.

---

## read

Read a file and return its contents as a string.

> read file "path/to/file.txt"

```markscript
# Usage: push the file path, then call read
push("/path/to/file.txt")
call("read file")
# Result is the file contents on the stack
```

---

## write

Write content to a file. Returns 1 on success.

> write file "path/to/file.txt" "content to write"

```markscript
# Usage: push path, push content, then call write
push("/path/to/output.txt")
push("Hello, MarkScript!")
call("write file")
# Result is 1 on success
```

---

## exists

Check if a file exists. Returns 1 if it does, 0 if not.

> file exists "path/to/file.txt"

```markscript
# Usage: push the path, call exists
push("/path/to/check.txt")
call("file exists")
# Result is 1 if file exists, 0 otherwise
```

---

## read_lines

Read a file and process it line by line. Each line is pushed to the stack.

> read file "path/to/data.csv"
> print "processing lines..."

```markscript
# Read a file and push each line to the stack as a string
push("/path/to/data.csv")
call("read file")
# The result string contains all lines
# In a real implementation, split by newline and push each
# For now, the entire content is on the stack
```

---

## append

Append content to an existing file. Creates it if it doesn't exist.

> read file "log.txt"
> write file "log.txt" "old content\nnew line"

```markscript
# Read existing content, append, write back
push("/path/to/log.txt")
call("read file")
# Now the old content is on the stack
# Append new content and write back
push("/path/to/log.txt")
push("appended text")
call("write file")
```
