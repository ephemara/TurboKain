# Tail

MarkScript file suffix - read the end of files, follow live logs.
Wraps `tail` via the IVT for bottom-of-file extraction.

---

## lines

Show the last N lines of a file.

> run "tail -n 10 file.txt"

```markscript
let n = 10
let file = "log.txt"
push("tail -n " + n + " " + file)
call("run")
# last 10 lines
```

---

## last_line

Show only the very last line.

> run "tail -n 1 file.txt"

```markscript
let file = "result.txt"
push("tail -n 1 " + file)
call("run")
# last line only
```

---

## bytes

Show the last N bytes of a file.

> run "tail -c 500 file.txt"

```markscript
let n = 500
let file = "output.bin"
push("tail -c " + n + " " + file)
call("run")
# last 500 bytes
```

---

## follow

Follow a file as it grows (live monitoring).

> run "tail -f app.log"

```markscript
let file = "app.log"
push("tail -f " + file)
call("run")
# continuously shows new lines
```

---

## follow_with_name

Follow a file, even if it gets rotated.

> run "tail -F app.log"

```markscript
let file = "server.log"
push("tail -F " + file)
call("run")
# survives log rotation
```

---

## retry

Keep trying to open a file if it's temporarily unavailable.

> run "tail -F --retry pending.log"

```markscript
let file = "pending.log"
push("tail -F --retry " + file)
call("run")
# waits for file to appear
```

---

## lines_from_start

Show all lines starting from line N.

> run "tail -n +10 file.txt"

```markscript
let start_line = 10
let file = "data.txt"
push("tail -n +" + start_line + " " + file)
call("run")
# lines 10 onwards (skips first 9)
```

---

## sleep_interval

Set polling interval for file following.

> run "tail -f -s 2 app.log"

```markscript
let seconds = 2
let file = "slow_log.txt"
push("tail -f -s " + seconds + " " + file)
call("run")
# checks for new lines every 2 seconds
```

---

## quiet

Suppress filename headers when following multiple files.

> run "tail -q -f *.log"

```markscript
let files = "*.log"
push("tail -q -f " + files)
call("run")
# no headers, just log lines
```

---

## verbose

Always show filename headers.

> run "tail -v -n 5 file.txt"

```markscript
let n = 5
let file = "single.txt"
push("tail -v -n " + n + " " + file)
call("run")
# header even for single file
```

---

## pid

Stop following a file when a process with a given PID exits.

> run "tail -f --pid=1234 app.log"

```markscript
let pid = 1234
let file = "build.log"
push("tail -f --pid=" + pid + " " + file)
call("run")
# stops when PID 1234 exits
```

---

## follow_multiple

Follow multiple files simultaneously.

> run "tail -f log1.log log2.log log3.log"

```markscript
let files = "log1.log log2.log log3.log"
push("tail -f " + files)
call("run")
# live feed from all files
```

---

## recent_errors

Extract the last N errors from a log file.

> run "grep 'ERROR' app.log | tail -n 20"

```markscript
let file = "app.log"
let n = 20
push("grep 'ERROR' " + file + " | tail -n " + n)
call("run")
# last 20 errors
```
