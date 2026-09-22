# Signal

Markscript signal handling -- send, trap, ignore, and list operating system
signals. Dispatches through the IVT to Kain's `std::process` bridge and OS
signal APIs.

---

## send

Send a named signal to a process by PID.

> run "taskkill /PID 1234"

```markscript
# Send a signal to a process
push(1234)
push("SIGTERM")
call("signal_send")
# Result: 1 if the signal was delivered
```

---

## trap

Register a handler for a specific signal. When the signal arrives, the
handler runs instead of the default action.

```markscript
# Trap a signal (set up a handler)
push("SIGINT")
push("handle_interrupt")
call("signal_trap")
# Result: 1 if the handler was registered
```

---

## ignore

Tell the runtime to ignore a specific signal entirely.

```markscript
# Ignore a signal
push("SIGPIPE")
call("signal_ignore")
# Result: 1 if the signal is now ignored
```

---

## default

Reset a signal's disposition back to the platform default behavior.

```markscript
# Reset a signal to default handler
push("SIGTERM")
call("signal_default")
# Result: 1 if the signal was reset
```

---

## list_signals

List all signal names known to the platform.

> run "kill -l 2>nul || echo SIGTERM,SIGINT,SIGKILL,SIGHUP,SIGQUIT,SIGUSR1,SIGUSR2"

```markscript
# List all available signal names
call("signal_list")
# Result: newline-delimited signal names
```

---

## kill

Send SIGKILL (SIGTERM fallback) to a process. On Unix this cannot be
caught or ignored; on Windows it force-terminates.

> run "taskkill /PID 1234 /F"

```markscript
# Force-kill a process
push(1234)
call("signal_kill")
# Result: 1 if the process was terminated
```

---

## pending

Get a list of signals currently pending delivery to this process.

```markscript
# Query pending signals
call("signal_pending")
# Result: newline-delimited pending signal names, empty if none
```

---

## block

Block a signal from delivery during a critical section. Unblock it later
with `default`.

```markscript
# Block a signal during critical section
push("SIGINT")
call("signal_block")
# Critical section code runs here...
push("SIGINT")
call("signal_default")
# Result: SIGINT was held during the critical section
```
