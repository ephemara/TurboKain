# Audit

Markscript security auditing -- logging, monitoring, compliance.
Dispatches to system tools for log analysis and scanning.

---

## log_event

Log a security event with timestamp.

> run "echo \"[$(date)] SECURITY: event description\" >> audit.log"

---

## watch_log

Watch a log file for new entries (tail follow).

> run "tail -f /var/log/audit.log"

---

## generate_report

Generate a summary report from audit logs.

> run "grep -c 'ERROR' /var/log/app.log"
> print "Total errors in log"

---

## alert_on_pattern

Alert when a specific pattern appears in logs.

> run "grep -q 'INTRUSION' /var/log/audit.log && echo 'ALERT: Intrusion detected'"

---

## compliance_check

Run basic compliance checks against a config file.

> read file "compliance_rules.txt"
> print "Running compliance checks"

---

## vulnerability_scan

Run nmap for basic vulnerability scanning.

> run "nmap -sV --script=vuln target_host"

---

## scan_remote

Run a remote security scan with nmap.

> run "nmap -A -T4 target_host"

---

## file_integrity

Check file integrity using SHA-256 comparison.

> run "openssl dgst -sha256 path/to/file.txt"

---

## baseline_compare

Compare current system state to a baseline.

> run "diff baseline.txt current_state.txt"

---

## failed_login_monitor

Monitor for failed login attempts.

> run "grep 'Failed password' /var/log/auth.log | wc -l"

---

## log_rotation_check

Verify log rotation is working.

> run "ls -la /var/log/app.log*"

---

## audit_trail

Generate a complete audit trail from multiple sources.

> run "cat /var/log/app.log /var/log/sys.log | grep -i 'audit' > audit_trail.txt"
