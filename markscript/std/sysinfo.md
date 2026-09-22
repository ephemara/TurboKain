# Sysinfo

Markscript comprehensive system information --- kernel release, machine type,
boot time, load averages, sensor readings, and system-wide resource state.
Dispatches through the IVT to Kain's `std::machine` bridge.

---

## kernel

Get the kernel version string.

> run "ver"

```markscript
# Query the kernel version
call("sysinfo_kernel")
# Result: kernel version string like "10.0.22631" or "6.8.0-45-generic"
```

---

## release

Get the OS release or distribution version string.

> run "wmic os get version"

```markscript
# Query the OS release / distribution version
call("sysinfo_release")
# Result: release string like "22H2" or "Ubuntu 24.04 LTS"
```

---

## machine

Get the machine hardware identifier.

> run "echo %PROCESSOR_ARCHITECTURE%"

```markscript
# Query machine hardware identifier
call("sysinfo_machine")
# Result: architecture string like "x86_64", "aarch64"
```

---

## boot_time

Get the system boot time as a UTC timestamp string.

> run "wmic os get LastBootUpTime"

```markscript
# Query system boot time
call("sysinfo_boot_time")
# Result: timestamp string like "2026-06-10T08:30:00Z"
```

---

## loadavg

Get system load averages split into 1, 5, and 15 minute values.

> run "wmic cpu get loadpercentage"

```markscript
# Query system load averages
call("sysinfo_loadavg")
# Result: three integers -- load1, load5, load15
```

---

## sensors

Query available hardware sensors (temperature, voltage, fan speed) and
their current readings.

> run "wmic /namespace:\\root\wmi PATH MSAcpi_ThermalZoneTemperature get *"

```markscript
# Query hardware sensor readings
call("sysinfo_sensors")
# Result: newline-delimited sensor readings with name and value
```

---

## entropy

Get the kernel entropy pool size / available randomness.

> run "wmic os get FreePhysicalMemory"

```markscript
# Query available system entropy
call("sysinfo_entropy")
# Result: entropy bits available as integer
```

---

## procs

Get the total number of running processes on the system.

> run "tasklist /FI "STATUS eq RUNNING" | find /v /c "::""

```markscript
# Query total process count
call("sysinfo_procs")
# Result: running process count as integer
```

---

## fds

Get the total number of open file descriptors across the system (Unix) or
total open handles (Windows).

> run "wmic os get HandleCount"

```markscript
# Query open file descriptors / handles
call("sysinfo_fds")
# Result: open handle count as integer
```
