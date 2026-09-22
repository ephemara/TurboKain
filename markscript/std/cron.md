# Cron

Markscript cron integration -- job scheduling, listing, editing, and
log inspection through shell dispatch.

---

## list

List all cron jobs for the current user.

> run "crontab -l"

```markscript
# Show current user's crontab
push("crontab -l")
call("run")
```

> run "crontab -l -u deploy"

```markscript
# Show another user's crontab (requires sudo)
push("sudo crontab -l -u deploy")
call("run")
```

---

## add

Add a new cron job.

> run "(crontab -l 2>/dev/null; echo \"0 2 * * * /usr/local/bin/backup.sh\") | crontab -"

```markscript
# Append a daily backup job at 2 AM
push("(crontab -l 2>/dev/null; echo \"0 2 * * * /usr/local/bin/backup.sh\") | crontab -")
call("run")
```

> run "(crontab -l 2>/dev/null; echo \"*/5 * * * * /usr/bin/healthcheck.sh\") | crontab -"

```markscript
# Add a health check every 5 minutes
push("(crontab -l 2>/dev/null; echo \"*/5 * * * * /usr/bin/healthcheck.sh\") | crontab -")
call("run")
```

---

## remove

Remove a specific cron job by pattern or clear all.

> run "crontab -l | grep -v \"/usr/local/bin/backup.sh\" | crontab -"

```markscript
# Remove the backup job from crontab
push("crontab -l | grep -v \"/usr/local/bin/backup.sh\" | crontab -")
call("run")
```

> run "crontab -r"

```markscript
# Remove all cron jobs for current user
push("crontab -r")
call("run")
```

---

## edit

Open the crontab in the default editor.

> run "crontab -e"

```markscript
# Edit crontab interactively
push("crontab -e")
call("run")
```

> run "EDITOR=nano crontab -e"

```markscript
# Edit crontab with a specific editor
push("EDITOR=nano crontab -e")
call("run")
```

---

## schedule

Define a cron schedule with standard frequencies.

> run "echo \"0 6 * * 1 /usr/local/bin/weekly-report.sh\" | crontab -"

```markscript
# Schedule weekly report every Monday at 6 AM
push("echo \"0 6 * * 1 /usr/local/bin/weekly-report.sh\" | crontab -")
call("run")
```

> run "(crontab -l 2>/dev/null; echo \"@reboot /usr/local/bin/start-services.sh\") | crontab -"

```markscript
# Schedule a job at system boot
push("(crontab -l 2>/dev/null; echo \"@reboot /usr/local/bin/start-services.sh\") | crontab -")
call("run")
```

---

## log

View the cron syslog to check job execution.

> run "grep CRON /var/log/syslog | tail -50"

```markscript
# Show last 50 cron entries from syslog
push("grep CRON /var/log/syslog | tail -50")
call("run")
```

> run "sudo journalctl -u cron --since "1 hour ago""

```markscript
# Show cron logs from the last hour using journalctl
push("sudo journalctl -u cron --since \"1 hour ago\"")
call("run")
```
