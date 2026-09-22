# Firewall

Markscript firewall management - packet filtering rules, port management, and policy control.
Dispatches through the IVT to netsh (Windows) or iptables (Linux) for all operations.

---

## allow

Add an allow rule for a specific port and protocol.

> run "netsh advfirewall firewall add rule name=\"Allow HTTP\" dir=in action=allow protocol=TCP localport=80"

```markscript
# Allow inbound traffic on a port
let name = "Allow HTTP"
let port = 80
let proto = "TCP"
push("netsh advfirewall firewall add rule name=\"" + name + "\" dir=in action=allow protocol=" + proto + " localport=" + port)
call("run")
```

---

## deny

Add a deny rule for a specific port and protocol.

> run "netsh advfirewall firewall add rule name=\"Block Telnet\" dir=in action=block protocol=TCP localport=23"

```markscript
# Block inbound traffic on a port
let name = "Block Telnet"
let port = 23
let proto = "TCP"
push("netsh advfirewall firewall add rule name=\"" + name + "\" dir=in action=block protocol=" + proto + " localport=" + port)
call("run")
```

---

## list_rules

List all firewall rules currently configured on the system.

> run "netsh advfirewall firewall show rule name=all verbose"

```markscript
# List all firewall rules
push("netsh advfirewall firewall show rule name=all verbose")
call("run")
```

---

## save

Save the current firewall configuration for persistence.

> run "netsh advfirewall export \"C:\\firewall_policy.wfw\""

```markscript
# Export firewall policy to file
let path = "C:\\firewall_policy.wfw"
push("netsh advfirewall export \"" + path + "\"")
call("run")
```

---

## reload

Reload firewall rules from a saved policy file.

> run "netsh advfirewall import \"C:\\firewall_policy.wfw\""

```markscript
# Import and apply firewall policy
let path = "C:\\firewall_policy.wfw"
push("netsh advfirewall import \"" + path + "\"")
call("run")
```

---

## flush

Remove all custom firewall rules (reset to defaults).

> run "netsh advfirewall reset"

```markscript
# Reset firewall to defaults
push("netsh advfirewall reset")
call("run")
```

---

## port

Check whether a specific port is open and listening.

> run "netstat -an | findstr :80"

```markscript
# Check if port is in use
let port = 80
push("netstat -an | findstr :" + port)
call("run")
```

---

## service

Allow or deny a specific application through the firewall.

> run "netsh advfirewall firewall add rule name=\"Allow App\" dir=in action=allow program=\"C:\\App\\app.exe\""

```markscript
# Allow an application through firewall
let name = "Allow App"
let app_path = "C:\\App\\app.exe"
push("netsh advfirewall firewall add rule name=\"" + name + "\" dir=in action=allow program=\"" + app_path + "\"")
call("run")
```

---

## block_ip

Block all traffic from a specific IP address.

> run "netsh advfirewall firewall add rule name=\"Block IP\" dir=in action=block remoteip=10.0.0.5"

```markscript
# Block traffic from an IP
let name = "Block IP"
let ip = "10.0.0.5"
push("netsh advfirewall firewall add rule name=\"" + name + "\" dir=in action=block remoteip=" + ip)
call("run")
```

---

## allow_ip

Allow all traffic from a specific trusted IP address.

> run "netsh advfirewall firewall add rule name=\"Allow IP\" dir=in action=allow remoteip=192.168.1.100"

```markscript
# Allow traffic from a trusted IP
let name = "Allow IP"
let ip = "192.168.1.100"
push("netsh advfirewall firewall add rule name=\"" + name + "\" dir=in action=allow remoteip=" + ip)
call("run")
```

---

## enable

Enable the firewall if it is currently disabled.

> run "netsh advfirewall set allprofiles state on"

```markscript
# Turn firewall on for all profiles
push("netsh advfirewall set allprofiles state on")
call("run")
```

---

## disable

Disable the firewall (use with extreme caution).

> run "netsh advfirewall set allprofiles state off"

```markscript
# Turn firewall off (dangerous)
push("netsh advfirewall set allprofiles state off")
call("run")
```

---

## log_traffic

Enable firewall logging for dropped packets.

> run "netsh advfirewall set allprofiles logging filename \"C:\\fw.log\""

```markscript
# Enable firewall logging
let logpath = "C:\\fw.log"
push("netsh advfirewall set allprofiles logging filename \"" + logpath + "\"")
call("run")
```

---

## status

Show the current firewall status for all profiles.

> run "netsh advfirewall show allprofiles"

```markscript
# Show firewall status
push("netsh advfirewall show allprofiles")
call("run")
```
