# Process Lifecycle

Full process lifecycle management through MarkScript intents.
Covers spawn, await, kill, exit codes, and captured I/O.
Dispatcher through GAMMA-owned IVT handlers (51-59).

---

## spawn tracked

Launch a command and track it in the VM's process table.
Returns a process index (0-based) for use with await, kill, exitcode, stdout, stderr.

> spawn "cargo build --release"

```markscript
# Spawn a tracked build
push("cargo build --release")
call("spawn tracked")
# Returns process index on stack (0, 1, 2, ...)
```

**Handler:** FN_PROCESS_SPAWN_TRACKED (51)

---

## await

Wait for a tracked process to complete.
Captures exit code, stdout, and stderr into the ProcessRecord.

> await 0

```markscript
# Wait for process 0
push(0)
call("await")
# Returns 1 on success, 0 on timeout
```

**Handler:** FN_PROCESS_AWAIT (52)
**Timeout:** 30 seconds

---

## kill

Terminate a running process.

> kill 0

```markscript
# Kill process 0
push(0)
call("kill")
# Returns 1 if killed, 0 if already exited
```

**Handler:** FN_PROCESS_KILL_PID (53)

---

## exitcode

Query the exit code of a completed process.

> exitcode 0

```markscript
# Get exit code of process 0
push(0)
call("exitcode")
# Returns exit code integer
```

**Handler:** FN_PROCESS_EXIT_CODE_PID (54)

---

## stdout (by PID)

Retrieve captured stdout from a tracked process.

> stdout 0

```markscript
# Get stdout of process 0
push(0)
call("stdout")
# Returns captured stdout as string
```

**Handler:** FN_PROCESS_STDOUT_PID (55)

---

## stderr (by PID)

Retrieve captured stderr from a tracked process.

> stderr 0

```markscript
# Get stderr of process 0
push(0)
call("stderr")
# Returns captured stderr as string
```

**Handler:** FN_PROCESS_STDERR_PID (56)

---

## pipe

Chain two commands -- stdout of first feeds stdin of second.

> pipe "cargo check 2>&1" "|" "grep error"

```markscript
# Pipe cargo check output through grep
push("cargo check 2>&1 | grep error")
call("pipe")
# Returns filtered output
```

**Handler:** FN_PROCESS_PIPE (57)

---

## env

Run a command with environment variables.

> env RUST_BACKTRACE=1 run "cargo test"

```markscript
# Run cargo test with backtrace enabled
push("RUST_BACKTRACE=1")
push("cargo test")
call("env")
```

**Handler:** FN_PROCESS_ENV (58)

---

## cwd

Run a command from a specific working directory.

> cwd "/path/to/project" run "cargo build"

```markscript
# Build from a specific directory
push("/path/to/project")
push("cargo build")
call("cwd")
```

**Handler:** FN_PROCESS_CWD (59)

---

## Classic handlers (backward compatible)

### run

Execute synchronously, capture stdout. Single fire-and-forget.

> run "echo hello"

```markscript
push("echo hello")
call("run")
# Returns captured stdout
```

**Handler:** FN_PROCESS_OUTPUT (4)

### spawn (basic)

Launch asynchronously without PID tracking. Returns immediately.

> spawn "server --port 8080"

```markscript
push("server --port 8080")
call("spawn")
```

**Handler:** FN_PROCESS_SPAWN (5)

---

## Example: Full Build with Lifecycle

```markdown
# CI Pipeline

## Build Stage
> spawn "cargo build --release"
> await 0
> exitcode 0
> assert 0 0

## Test Stage
> spawn "cargo test"
> await 1
> exitcode 1
> assert 0 0

## Deploy (only if all passed)
> print "All stages passed -- deploying..."
> run "scp target/release/myapp server:/opt/"
```
