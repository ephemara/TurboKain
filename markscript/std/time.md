# Time

Markscript time utilities - timestamps, delays, measurement.
Dispatches through the IVT to Kain's process bridge for system time.

---

## now

Get the current timestamp.

> run "echo %TIME%"

```markscript
# Get current time via shell
push("echo %TIME%")
call("run")
```

---

## sleep

Pause execution for N milliseconds.

> run "timeout /t 1 /nobreak > nul"

```markscript
# Sleep for 1 second (Windows)
push("timeout /t 1 /nobreak > nul")
call("run")
```

---

## timestamp

Generate an ISO-8601 timestamp.

> run "powershell -c Get-Date -Format o"

```markscript
# Generate ISO timestamp
push("powershell -c Get-Date -Format o")
call("run")
```

---

## measure

Measure how long a block of code takes to execute.

> print "Starting measurement..."
> run "echo done"
> print "Measurement complete"

```markscript
# Wrap code with timing markers
push("Starting measurement...")
call("print")
push("echo done")
call("run")
push("Measurement complete")
call("print")
```

---

## date

Get the current date.

> run "echo %DATE%"

```markscript
# Get current date via shell
push("echo %DATE%")
call("run")
```

---

## epoch

Get Unix epoch seconds.

> run "powershell -c [int](Get-Date -UFormat %s)"

```markscript
# Unix timestamp
push("powershell -c [int](Get-Date -UFormat %s)")
call("run")
```

---

## timer

A simple countdown timer.

```markscript
let seconds = 5
while seconds > 0:
    seconds = seconds - 1
# wait loop for countdown
```

---

## calendar

Display a calendar month.

> run "powershell -c Get-Calendar"

```markscript
# Show calendar
push("powershell -c Get-Calendar")
call("run")
```
