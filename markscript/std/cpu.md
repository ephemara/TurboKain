# CPU

Markscript CPU information and monitoring - core count, usage, load averages,
frequency, model string, temperature, and governor. Dispatches through the
IVT to Kain's `std::machine` bridge and OS performance counters.

---

## count

Get the number of logical CPU cores.

> run "echo %NUMBER_OF_PROCESSORS%"

```markscript
# Query CPU core count
call("cpu_count")
# Result: integer count of logical processors
```

---

## usage

Get the overall CPU usage percentage.

> run "wmic cpu get loadpercentage"

```markscript
# Query overall CPU usage
call("cpu_usage")
# Result: usage percentage as integer (0-100)
```

---

## load

Get the system load averages (1, 5, and 15 minute). On Windows, returns
CPU queue length and usage trends.

> run "wmic cpu get loadpercentage"

```markscript
# Query load averages
call("cpu_load")
# Result: three values --- load1, load5, load15
```

---

## frequency

Get the current CPU frequency in MHz.

> run "wmic cpu get CurrentClockSpeed"

```markscript
# Query current CPU frequency
call("cpu_frequency")
# Result: frequency in MHz as integer
```

---

## model

Get the CPU model name string.

> run "wmic cpu get name"

```markscript
# Query CPU model string
call("cpu_model")
# Result: model string like "Intel(R) Core(TM) i7-12700K"
```

---

## temp

Get the CPU temperature in degrees Celsius. Requires administrative
privileges on some platforms.

> run "wmic /namespace:\\root\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature"

```markscript
# Query CPU temperature
call("cpu_temp")
# Result: temperature in degrees Celsius (rounded)
```

---

## governor

Get the CPU frequency scaling governor (Linux only). Returns "powersave",
"performance", "ondemand", etc. On Windows this is a no-op.

> run "powercfg /query 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"

```markscript
# Query the CPU power policy / governor
call("cpu_governor")
# Result: governor name string or "unknown"
```

---

## per_core

Get CPU usage per logical core as a list.

> run "wmic cpu get loadpercentage"

```markscript
# Query per-core usage breakdown
call("cpu_per_core")
# Result: newline-delimited usage percentages, one per core
```
