# OS

Markscript operating system identification and runtime information -- query
the platform name, architecture, version, hostname, user identity, and
current working directory. Dispatches through the IVT to Kain's system bridge.

---

## name

Get the operating system name.

> run "ver"

```markscript
# Query OS name from the IVT
call("os_name")
# Result: "windows", "linux", "macos", "freebsd", etc.
```

---

## arch

Get the CPU architecture of the running system.

> run "echo %PROCESSOR_ARCHITECTURE%"

```markscript
# Query CPU architecture
call("os_arch")
# Result: "x86_64", "aarch64", "x86", etc.
```

---

## version

Get the OS version string.

> run "ver"

```markscript
# Query full OS version
call("os_version")
# Result: version string like "10.0.22631"
```

---

## uptime

Get system uptime in seconds since last boot.

> run "net stats workstation | find "since""

```markscript
# Query system uptime
call("os_uptime")
# Result: uptime in seconds as an integer
```

---

## hostname

Get the hostname of the machine.

> run "hostname"

```markscript
# Query the system hostname
call("os_hostname")
# Result: the hostname string
```

---

## user

Get the current user's username.

> run "echo %USERNAME%"

```markscript
# Query the current user name
call("os_user")
# Result: the username string
```

---

## home

Get the current user's home directory path.

> run "echo %USERPROFILE%"

```markscript
# Query the home directory path
call("os_home")
# Result: path string like "C:\Users\alice"
```

---

## tmpdir

Get the system temporary directory path.

> run "echo %TEMP%"

```markscript
# Query the temp directory path
call("os_tmpdir")
# Result: path string like "C:\Users\alice\AppData\Local\Temp"
```

---

## pid

Get the current process ID.

> run "echo %PID%"

```markscript
# Query the current process PID
call("os_pid")
# Result: integer PID
```

---

## cwd

Get the current working directory path.

> run "echo %CD%"

```markscript
# Query the current directory
call("os_cwd")
# Result: absolute path string
```

---

## chdir

Change the current working directory.

> run "cd /d C:\Users\alice\projects"

```markscript
# Change to a new working directory
push("C:\\Users\\alice\\projects")
call("os_chdir")
# Result: 1 on success, 0 if the directory doesn't exist
```
