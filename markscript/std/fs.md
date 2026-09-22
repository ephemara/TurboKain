# FS

Markscript filesystem operations -- create, delete, traverse, permissions,
symlinks, and file metadata. Dispatches through the IVT to Kain's
`std::fs` bridge.

---

## mkdir

Create a directory. Supports recursive creation of parent directories.

> run "mkdir /path/to/new/dir 2>nul || md /path/to/new/dir"

```markscript
# Create a directory (recursive)
push("/path/to/new/directory")
call("fs_mkdir")
# Result: 1 on success, 0 if already exists
```

---

## rmdir

Remove a directory. Fails if the directory is not empty unless recursive.

> run "rmdir /s /q /path/to/dir 2>nul || rd /s /q /path/to/dir"

```markscript
# Remove a directory tree
push("/path/to/directory")
call("fs_rmdir")
# Result: 1 on success, 0 on failure
```

---

## read_dir

List entries in a directory. Returns filenames only (not full paths).

> run "dir /b /path/to/dir"

```markscript
# List directory contents
push("/path/to/directory")
call("fs_read_dir")
# Result: newline-delimited file and folder names
```

---

## walk

Recursively walk a directory tree, yielding every file and folder path.

> run "dir /s /b /path/to/dir"

```markscript
# Walk directory tree recursively
push("/path/to/directory")
call("fs_walk")
# Result: newline-delimited full paths, depth-first
```

---

## chmod

Change permissions on a file or directory (Unix mode bits, Windows DACL).

> run "attrib -R /path/to/file"

```markscript
# Change file permissions
push("/path/to/file")
push("644")
call("fs_chmod")
# Result: 1 on success, 0 on failure
```

---

## chown

Change the owner and group of a file or directory (Unix only; no-op on
Windows without privilege).

> run "takeown /f /path/to/file"

```markscript
# Change ownership of a file
push("/path/to/file")
push("alice")
push("staff")
call("fs_chown")
# Result: 1 on success, 0 on failure
```

---

## symlink

Create a symbolic link pointing to a target.

> run "mklink link target"

```markscript
# Create a symbolic link
push("/path/to/link")
push("/path/to/target")
call("fs_symlink")
# Result: 1 on success, 0 on failure
```

---

## hardlink

Create a hard link to an existing file.

> run "mklink /h hardlink existing"

```markscript
# Create a hard link
push("/path/to/hardlink")
push("/path/to/existing")
call("fs_hardlink")
# Result: 1 on success, 0 on failure
```

---

## stat

Get file metadata --- size, modified time, created time, permissions, type.

> run "dir /path/to/file"

```markscript
# Get file metadata
push("/path/to/file")
call("fs_stat")
# Result: structured metadata string
```

---

## touch

Create an empty file or update the modification timestamp of an existing one.

> run "copy /b nul /path/to/file"

```markscript
# Touch a file (create or update timestamp)
push("/path/to/file")
call("fs_touch")
# Result: 1 on success
```
