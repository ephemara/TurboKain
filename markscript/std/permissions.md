# Permissions

Markscript file permission and access control --- check, grant, revoke,
inspect octal modes, and manage ACL entries. Dispatches through the IVT
to Kain's `std::fs` bridge and OS security APIs.

---

## check

Check whether the current process has a specific permission on a path.

> run "icacls /path/to/file"

```markscript
# Check permission on a path
push("/path/to/file")
push("read")
call("perm_check")
# Result: 1 if the permission is granted, 0 otherwise
```

---

## grant

Grant a permission to a user or group on a file or directory.

> run "icacls /path/to/file /grant alice:(R,W)"

```markscript
# Grant permission to a user
push("/path/to/file")
push("alice")
push("read,write")
call("perm_grant")
# Result: 1 on success, 0 on failure
```

---

## revoke

Revoke a permission from a user or group on a file or directory.

> run "icacls /path/to/file /remove alice"

```markscript
# Revoke permission from a user
push("/path/to/file")
push("alice")
call("perm_revoke")
# Result: 1 on success
```

---

## octal

Get the Unix-style octal permission mode for a file or directory.

> run "icacls /path/to/file"

```markscript
# Query octal permission mode
push("/path/to/file")
call("perm_octal")
# Result: three-digit octal string like "644", "755"
```

---

## mask

Set the file creation umask for the current process. Affects permissions
on newly created files.

> run "umask 022"

```markscript
# Set the process umask
push(022)
call("perm_mask")
# Result: previous umask as integer
```

---

## acl

Get the full Access Control List for a file or directory.

> run "icacls /path/to/file"

```markscript
# Get the ACL for a path
push("/path/to/file")
call("perm_acl")
# Result: newline-delimited ACL entries
```

---

## owner

Get the owner of a file or directory (user and group).

> run "dir /Q /path/to/file"

```markscript
# Get file ownership
push("/path/to/file")
call("perm_owner")
# Result: "user:group" string
```

---

## mode_bits

Interpret an octal mode string into read/write/execute bits for owner,
group, and others.

```markscript
let mode = "755"
# owner: rwx (7), group: r-x (5), others: r-x (5)
# Bit interpretation:
# 7 = read+write+execute (4+2+1)
# 6 = read+write (4+2)
# 5 = read+execute (4+1)
# 4 = read only
# 0 = no permissions
# Result is a structured breakdown
```
