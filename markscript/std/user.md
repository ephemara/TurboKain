# User

Markscript user identity and account management -- query the current user,
list groups, inspect account metadata. Dispatches through the IVT to Kain's
`std::user` bridge and OS account APIs.

---

## whoami

Get the current user's login name.

> run "whoami"

```markscript
# Query current user from the OS
call("user_whoami")
# Result: the login name string
```

---

## id

Get the current user's unique identifier (UID on Unix, SID on Windows).

> run "whoami /user"

```markscript
# Query the current user's ID
call("user_id")
# Result: identifier string --- "1000" on Linux, "S-1-5-21-..." on Windows
```

---

## groups

List all groups the current user belongs to.

> run "whoami /groups"

```markscript
# List group memberships
call("user_groups")
# Result: newline-delimited group name list
```

---

## home

Get the current user's home directory path.

> run "echo %USERPROFILE%"

```markscript
# Query the user's home directory
call("user_home")
# Result: path string like "C:\Users\alice"
```

---

## shell

Get the current user's default shell.

> run "echo %COMSPEC%"

```markscript
# Query the default shell path
call("user_shell")
# Result: path string like "C:\Windows\System32\cmd.exe" or "/bin/bash"
```

---

## exists

Check whether a user account exists on the system.

> run "net user alice 2>nul && echo 1 || echo 0"

```markscript
# Check if a specific user exists
push("alice")
call("user_exists")
# Result: 1 if the user exists, 0 otherwise
```

---

## create

Create a new user account on the system (requires elevated privileges).

> run "net user alice password /add"

```markscript
# Create a new user account
push("alice")
push("temporary_password_123")
call("user_create")
# Result: 1 on success, 0 on failure (likely permission denied)
```

---

## info

Get full account metadata for a user.

> run "net user alice"

```markscript
# Query full user account metadata
push("alice")
call("user_info")
# Result: structured info --- full name, sid/uid, groups, account status
```
