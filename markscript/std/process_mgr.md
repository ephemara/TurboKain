# Process Manager

Markscript process management - list, inspect, kill, reprioritize, and query
process trees. Dispatches through the IVT to Kain's `std::process` bridge.

---

## list

List all running processes with PID, name, and memory usage.

> run "tasklist /FO CSV"

```markscript
# List running processes
call("process_list")
# Result: CSV-like output with PID, name, memory, status
```

---

## find

Find a process by name or PID.

> run "tasklist /FI "IMAGENAME eq myapp.exe""

```markscript
# Find a process by name
push("myapp.exe")
call("process_find")
# Result: process list matching the name, or empty if not running
```

---

## kill

Terminate a process by PID. Send a signal (SIGTERM/SIGKILL) on Unix or
terminate on Windows.

> run "taskkill /PID 1234 /F"

```markscript
# Kill a process by PID
push(1234)
call("process_kill")
# Result: 1 if terminated, 0 if not found
```

---

## nice

Adjust the priority of a process. Value range: -20 (highest) to 19 (lowest)
on Unix; maps to priority classes on Windows.

> run "wmic process where processid=1234 CALL setpriority 32"

```markscript
# Adjust process priority
push(1234)
push(-10)
call("process_nice")
# Result: 1 on success, 0 on failure (likely permission denied)
```

---

## tree

Get the process tree rooted at a given PID, showing parent-child
relationships.

> run "tasklist /FO CSV /SVC /V"

```markscript
# Get the process tree
push(1234)
call("process_tree")
# Result: indented tree showing parent-child relationships
```

---

## parent

Get the parent PID of a given process.

> run "wmic process where processid=1234 get parentprocessid"

```markscript
# Query parent PID
push(1234)
call("process_parent")
# Result: parent PID as integer, or 0 if no parent
```

---

## children

Get all child PIDs of a given process.

> run "wmic process where parentprocessid=1234 get processid"

```markscript
# Query child PIDs
push(1234)
call("process_children")
# Result: newline-delimited child PID list
```

---

## cmdline

Get the full command line of a running process.

> run "wmic process where processid=1234 get commandline"

```markscript
# Query process command line
push(1234)
call("process_cmdline")
# Result: full command line string
```
