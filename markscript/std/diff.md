# Diff

MarkScript file comparison - find differences between files.
Wraps `diff` via the IVT for line-by-line comparison.

---

## unified

Show differences in unified format with context.

> run "diff -u file1.txt file2.txt"

```markscript
let a = "original.txt"
let b = "modified.txt"
push("diff -u " + a + " " + b)
call("run")
# unified diff output
```

---

## context

Show differences in context format.

> run "diff -c file1.txt file2.txt"

```markscript
let a = "draft.md"
let b = "final.md"
push("diff -c " + a + " " + b)
call("run")
# context diff with surrounding lines
```

---

## side_by_side

Show differences side by side.

> run "diff -y file1.txt file2.txt"

```markscript
let a = "left.txt"
let b = "right.txt"
push("diff -y " + a + " " + b)
call("run")
# side-by-side comparison
```

---

## side_by_side_width

Side-by-side with custom column width.

> run "diff -y -W 120 file1.txt file2.txt"

```markscript
let a = "config1.ini"
let b = "config2.ini"
let width = 120
push("diff -y -W " + width + " " + a + " " + b)
call("run")
# wider side-by-side view
```

---

## recursive

Recursively compare directories.

> run "diff -r dir1/ dir2/"

```markscript
let dir_a = "src/old/"
let dir_b = "src/new/"
push("diff -r " + dir_a + " " + dir_b)
call("run")
# diffs all files in directory trees
```

---

## brief

Show only which files differ, not the changes.

> run "diff -q file1.txt file2.txt"

```markscript
let a = "expected.txt"
let b = "actual.txt"
push("diff -q " + a + " " + b)
call("run")
# "Files differ" or silence
```

---

## brief_recursive

Show which files differ in directory trees.

> run "diff -qr dir1/ dir2/"

```markscript
let dir_a = "backup/"
let dir_b = "live/"
push("diff -qr " + dir_a + " " + dir_b)
call("run")
# only filenames that differ
```

---

## ignore_whitespace

Compare ignoring whitespace differences.

> run "diff -w file1.txt file2.txt"

```markscript
let a = "formatted.py"
let b = "reindented.py"
push("diff -w " + a + " " + b)
call("run")
# ignores indentation changes
```

---

## ignore_case

Compare ignoring case differences.

> run "diff -i file1.txt file2.txt"

```markscript
let a = "UPPERCASE.txt"
let b = "lowercase.txt"
push("diff -i " + a + " " + b)
call("run")
# case-insensitive comparison
```

---

## newline_at_eof

Check for missing trailing newline difference.

> run "diff file1.txt file2.txt"

```markscript
let a = "file_a.txt"
let b = "file_b.txt"
push("diff " + a + " " + b)
call("run")
# reports "No newline at end of file"
```

---

## patch_output

Generate a patch file from differences.

> run "diff -u file1.txt file2.txt > changes.patch"

```markscript
let a = "old.txt"
let b = "new.txt"
let patch_file = "changes.patch"
push("diff -u " + a + " " + b + " > " + patch_file)
call("run")
# patch file written to disk
```

---

## stat

Show summary of changes (lines added/removed).

> run "diff --stat file1.txt file2.txt"

```markscript
let a = "before.txt"
let b = "after.txt"
push("diff --stat " + a + " " + b)
call("run")
# "5 files changed, 23 insertions(+), 7 deletions(-)"
```
