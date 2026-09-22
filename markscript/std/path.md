# Path

Markscript path manipulation - join, split, resolve, normalize, and query
filesystem paths. Pure string manipulation combined with filesystem checks
through the IVT.

---

## join

Join two or more path components with the platform separator.

```markscript
let parent = "/home/user"
let child = "docs"
let result = parent + "/" + child
# result = "/home/user/docs"
```

---

## basename

Extract the last component of a path.

```markscript
let full = "/home/user/docs/report.md"
# Walk backward to last separator
# result = "report.md"
```

---

## dirname

Extract the parent directory path.

```markscript
let full = "/home/user/docs/report.md"
# Strip the basename
# result = "/home/user/docs"
```

---

## ext

Extract the file extension (including the dot).

```markscript
let file = "image.png"
# Find the last '.' and take everything from there
# result = ".png"
```

---

## exists

Check whether a path exists in the filesystem.

> file exists "/home/user/docs/report.md"

```markscript
push("/home/user/docs/report.md")
call("file exists")
# Result is 1 if the path exists, 0 otherwise
```

---

## is_dir

Check whether a path points to a directory.

> run "dir /AD /B /S path 2>nul && echo 1 || echo 0"

```markscript
push("/home/user/docs")
call("path_is_dir")
# Result is 1 if it's a directory, 0 otherwise
```

---

## is_file

Check whether a path points to a regular file.

> run "if exist path\..\nul (echo 1) else (echo 0)"

```markscript
push("/home/user/docs/report.md")
call("path_is_file")
# Result is 1 if it's a regular file, 0 otherwise
```

---

## resolve

Resolve a path to its absolute form, expanding symlinks and normalizing
`..` and `.` components.

> run "cd /d path && echo %CD%"

```markscript
let rel = "../docs/report.md"
# Push the relative path and resolve to absolute
push(rel)
call("path_resolve")
# Result is the absolute path
```

---

## normalize

Normalize a path by collapsing redundant separators, `..`, and `.`.

```markscript
let messy = "/home/./user/../user/docs//report.md"
# Collapse .. and . and duplicate separators
let result = messy
# result = "/home/user/docs/report.md"
```

---

## relative

Compute the relative path from one directory to another.

```markscript
let base = "/home/user/docs"
let target = "/home/user/photos/vacation/img001.jpg"
# Subtract the common prefix
# result = "../photos/vacation/img001.jpg"
```
