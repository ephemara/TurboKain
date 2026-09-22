# Systemd

Markscript systemd integration - service lifecycle, unit management,
and journal inspection through shell dispatch.

---

## start

Start a systemd service immediately.

> run "sudo systemctl start nginx"

```markscript
# Start the nginx service
push("sudo systemctl start nginx")
call("run")
```

> run "systemctl --user start my-user-service"

```markscript
# Start a user-scoped service
push("systemctl --user start my-user-service")
call("run")
```

---

## stop

Stop a running systemd service.

> run "sudo systemctl stop nginx"

```markscript
# Stop the nginx service
push("sudo systemctl stop nginx")
call("run")
```

---

## restart

Restart a systemd service.

> run "sudo systemctl restart nginx"

```markscript
# Restart nginx (stop + start)
push("sudo systemctl restart nginx")
call("run")
```

> run "sudo systemctl reload nginx"

```markscript
# Reload config without restarting (if supported)
push("sudo systemctl reload nginx")
call("run")
```

---

## enable

Enable a service to start at boot.

> run "sudo systemctl enable nginx"

```markscript
# Enable nginx on boot
push("sudo systemctl enable nginx")
call("run")
```

> run "sudo systemctl enable --now nginx"

```markscript
# Enable and start immediately
push("sudo systemctl enable --now nginx")
call("run")
```

---

## disable

Disable a service from starting at boot.

> run "sudo systemctl disable nginx"

```markscript
# Disable nginx from auto-starting
push("sudo systemctl disable nginx")
call("run")
```

---

## status

Show the current status of a service.

> run "systemctl status nginx"

```markscript
# Show nginx status with logs
push("systemctl status nginx")
call("run")
```

> run "systemctl --failed"

```markscript
# List all failed services
push("systemctl --failed")
call("run")
```

---

## journal

View service logs via journald.

> run "sudo journalctl -u nginx -n 50 --no-pager"

```markscript
# Show last 50 lines of nginx logs
push("sudo journalctl -u nginx -n 50 --no-pager")
call("run")
```

> run "sudo journalctl -u nginx -f"

```markscript
# Follow nginx logs live
push("sudo journalctl -u nginx -f")
call("run")
```

> run "sudo journalctl -u nginx --since "1 hour ago" --until "10 minutes ago""

```markscript
# Show logs from a time window
push("sudo journalctl -u nginx --since \"1 hour ago\" --until \"10 minutes ago\"")
call("run")
```
