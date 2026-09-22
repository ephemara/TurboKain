# Memory

Markscript memory and RAM querying - total, free, used, swap, and pressure
indicators. Dispatches through the IVT to Kain's `std::machine` bridge and
OS memory APIs.

---

## total

Get total physical RAM in bytes.

> run "wmic computersystem get TotalPhysicalMemory"

```markscript
# Query total physical memory
call("mem_total")
# Result: total RAM in bytes as a large integer
```

---

## free

Get currently free (unused) physical RAM in bytes.

> run "wmic OS get FreePhysicalMemory"

```markscript
# Query free physical memory
call("mem_free")
# Result: free RAM in bytes as a large integer
```

---

## used

Get currently used physical RAM in bytes.

> run "wmic OS get TotalVisibleMemorySize,FreePhysicalMemory"

```markscript
# Calculate used = total - free
let total = call("mem_total")
let free = call("mem_free")
let used = total - free
# Result: used RAM in bytes as a large integer
```

---

## swap_total

Get total swap space in bytes.

> run "wmic OS get TotalSwapSpaceSize"

```markscript
# Query total swap space
call("mem_swap_total")
# Result: total swap in bytes
```

---

## swap_free

Get free swap space in bytes.

> run "wmic OS get FreeVirtualMemory"

```markscript
# Query free swap space
call("mem_swap_free")
# Result: free swap in bytes
```

---

## available

Get available memory (free + reclaimable) in bytes.

> run "wmic OS get FreePhysicalMemory"

```markscript
# Query available memory (includes cached/reclaimable pages)
call("mem_available")
# Result: available RAM in bytes
```

---

## pressure

Get a memory pressure score from 0 (idle) to 100 (critical).

> run "wmic OS get FreePhysicalMemory,TotalVisibleMemorySize"

```markscript
# Calculate memory pressure
let free = call("mem_free")
let total = call("mem_total")
let pressure = 100 - (free * 100 / total)
# Result: pressure score 0-100
```

---

## breakdown

Get a structured breakdown of memory usage: total, used, free, cached,
buffered, available, swap.

> run "wmic OS get TotalVisibleMemorySize,FreePhysicalMemory /format:csv"

```markscript
# Query full memory breakdown
call("mem_breakdown")
# Result: structured breakdown string with all categories
```
