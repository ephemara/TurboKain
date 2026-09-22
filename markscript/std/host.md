# Host

Markscript host machine information -- hostname, IP addresses, network
interfaces, DNS resolution. Dispatches through the IVT to Kain's
`std::net` and system bridge.

---

## name

Get the hostname of the machine.

> run "hostname"

```markscript
# Query the system hostname
call("host_name")
# Result: the hostname string
```

---

## ip

Get the primary IPv4 address of the machine.

> run "ipconfig | findstr IPv4"

```markscript
# Query the primary IP address
call("host_ip")
# Result: dotted-decimal IPv4 string like "192.168.1.42"
```

---

## fqdn

Get the fully qualified domain name of the machine.

> run "hostname --fqdn 2>nul || echo %COMPUTERNAME%.%USERDNSDOMAIN%"

```markscript
# Query the FQDN
call("host_fqdn")
# Result: FQDN string like "alice-laptop.example.com"
```

---

## interfaces

List all network interfaces with their IP addresses and MACs.

> run "ipconfig /all"

```markscript
# List all network interfaces
call("host_interfaces")
# Result: newline-delimited interface list with name, IP, MAC per entry
```

---

## resolve

Resolve a hostname to its IP address(es).

> run "ping -n 1 google.com 2>nul | findstr "Pinging""

```markscript
# Resolve a hostname to IPv4 addresses
push("google.com")
call("host_resolve")
# Result: newline-delimited IP addresses
```

---

## localhost

Get the canonical localhost address.

> run "ping -n 1 localhost 2>nul | findstr "Pinging""

```markscript
# Get the localhost address
call("host_localhost")
# Result: "127.0.0.1" (IPv4) or "::1" (IPv6)
```

---

## mac

Get the MAC address of the primary network interface.

> run "getmac"

```markscript
# Query the primary MAC address
call("host_mac")
# Result: MAC address string like "AA:BB:CC:DD:EE:FF"
```

---

## reachable

Check whether a remote host is reachable on the network.

> run "ping -n 1 -w 1000 192.168.1.1 >nul 2>&1 && echo 1 || echo 0"

```markscript
# Check if a host is reachable
push("192.168.1.1")
call("host_reachable")
# Result: 1 if reachable within timeout, 0 otherwise
```
