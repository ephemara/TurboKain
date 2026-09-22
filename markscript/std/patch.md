# Patch

MarkScript patch management -- apply, reverse, test, and create patches.
Wraps `patch` via the IVT for applying diffs to files.

---

## apply

Apply a patch file to the target.

> run "patch < changes.patch"

```markscript
let patch_file = "fixes.patch"
push("patch < " + patch_file)
call("run")
# patch applied in-place
```

---

## apply_with_strip

Apply a patch, stripping N leading path components.

> run "patch -p1 < changes.patch"

```markscript
let patch_file = "upstream.patch"
let strip = 1
push("patch -p" + strip + " < " + patch_file)
call("run")
# strips a/b/ prefix from paths
```

---

## reverse

Reverse (undo) a previously applied patch.

> run "patch -R < changes.patch"

```markscript
let patch_file = "bad_patch.patch"
push("patch -R < " + patch_file)
call("run")
# reverts the patch changes
```

---

## dry_run

Test a patch without actually modifying files.

> run "patch --dry-run < changes.patch"

```markscript
let patch_file = "proposed.patch"
push("patch --dry-run < " + patch_file)
call("run")
# shows what would change
```

---

## strip

Control path stripping level.

> run "patch -p0 < changes.patch"

```markscript
let patch_file = "patches/fix.patch"
let level = 0
push("patch -p" + level + " < " + patch_file)
call("run")
# p0 = full path, p1 = strip first component
```

---

## backup

Apply patch with automatic backup of originals.

> run "patch -b < changes.patch"

```markscript
let patch_file = "critical.patch"
push("patch -b < " + patch_file)
call("run")
# originals saved with .orig suffix
```

---

## backup_versioned

Apply patch with versioned backup files.

> run "patch -b -V numbered < changes.patch"

```markscript
let patch_file = "update.patch"
push("patch -b -V numbered < " + patch_file)
call("run")
# backups as file.orig.1, file.orig.2, etc.
```

---

## create

Create a patch by comparing two files.

> run "diff -u original.txt modified.txt > changes.patch"

```markscript
let original = "old.py"
let modified = "new.py"
let patch_file = "changes.patch"
push("diff -u " + original + " " + modified + " > " + patch_file)
call("run")
# patch file created from differences
```

---

## batch_apply

Apply all .patch files in a directory.

> run "for f in patches/*.patch; do patch < \"$f\"; done"

```markscript
let patch_dir = "patches/"
push("for f in " + patch_dir + "*.patch; do patch < \"$f\"; done")
call("run")
# all patches applied in order
```

---

## ignore_whitespace

Apply patch ignoring whitespace differences.

> run "patch -l < changes.patch"

```markscript
let patch_file = "format.patch"
push("patch -l < " + patch_file)
call("run")
# whitespace-insensitive application
```

---

## directory_apply

Apply patch from within a specific directory.

> run "patch -d /target/dir < changes.patch"

```markscript
let target_dir = "src/"
let patch_file = "../fix.patch"
push("patch -d " + target_dir + " < " + patch_file)
call("run")
# patch applied relative to target directory
```
