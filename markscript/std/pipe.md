# Pipe

Markscript pipe and descriptor operations -- create FIFO pipes, redirect
standard streams, duplicate file descriptors. Dispatches through the IVT
to Kain's `std::process` and `std::io` bridges.

---

## create

Create a unidirectional pipe. Returns a pair of file descriptors: one for
reading, one for writing.

> run "echo test | findstr test"

```markscript
# Create a pipe - returns two handles
call("pipe_create")
# Result: two integers -- read_fd, write_fd
```

---

## read

Read data from a pipe or file descriptor into a string buffer.

> run "type input.txt | more"

```markscript
# Read from a pipe descriptor
push(read_fd)
call("pipe_read")
# Result: data string read from the pipe
```

---

## write

Write data to a pipe or file descriptor.

> run "echo data | clip"

```markscript
# Write data to a pipe descriptor
push(write_fd)
push("data to send")
call("pipe_write")
# Result: number of bytes written
```

---

## close

Close a pipe end (file descriptor). Releases the OS resource.

> run "exec 3>&-"

```markscript
# Close a pipe descriptor
push(fd)
call("pipe_close")
# Result: 1 on successful close
```

---

## dup

Duplicate a file descriptor, creating a new descriptor pointing to the same
underlying handle.

> run "exec 3>&1"

```markscript
# Duplicate a file descriptor
push(fd)
call("pipe_dup")
# Result: new_fd (integer)
```

---

## redirect

Redirect a standard stream (stdin, stdout, stderr) to a pipe or file.

> run "command 2>&1"

```markscript
# Redirect a stream
push(stream)    # 0=stdin, 1=stdout, 2=stderr
push(target_fd)
call("pipe_redirect")
# Result: 1 on success
```

---

## named_create

Create a named pipe (FIFO) at a filesystem path.

> run "mklink \\.\pipe\myapp"

```markscript
# Create a named pipe
push("\\\\.\\pipe\\mymarkscript")
call("pipe_named_create")
# Result: 1 on success
```

---

## named_connect

Connect to an existing named pipe for reading or writing.

```markscript
# Connect to a named pipe
push("\\\\.\\pipe\\mymarkscript")
call("pipe_named_connect")
# Result: a file descriptor for the connected pipe
```
