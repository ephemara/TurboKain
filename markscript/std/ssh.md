# SSH

Markscript SSH integration -- remote connections, key management, tunnels,
and configuration through shell dispatch.

---

## connect

Connect to a remote host via SSH.

> run "ssh user@hostname -p 22"

```markscript
# Standard SSH connection
push("ssh user@hostname -p 22")
call("run")
```

> run "ssh -i ~/.ssh/deploy_key user@hostname"

```markscript
# Connect with a specific identity file
push("ssh -i ~/.ssh/deploy_key user@hostname")
call("run")
```

---

## keygen

Generate an SSH key pair.

> run "ssh-keygen -t ed25519 -C \"user@email.com\" -f ~/.ssh/id_ed25519 -N \"\""

```markscript
# Generate ed25519 key pair without passphrase
push("ssh-keygen -t ed25519 -C \"user@email.com\" -f ~/.ssh/id_ed25519 -N \"\"")
call("run")
```

> run "ssh-keygen -t rsa -b 4096 -C \"deploy-bot\" -f ~/.ssh/deploy_key -N \"\""

```markscript
# Generate RSA 4096-bit deploy key
push("ssh-keygen -t rsa -b 4096 -C \"deploy-bot\" -f ~/.ssh/deploy_key -N \"\"")
call("run")
```

---

## copy_id

Copy a public key to a remote host's authorized_keys.

> run "ssh-copy-id -i ~/.ssh/id_ed25519.pub user@hostname"

```markscript
# Install public key on remote host
push("ssh-copy-id -i ~/.ssh/id_ed25519.pub user@hostname")
call("run")
```

---

## tunnel

Create an SSH tunnel for port forwarding.

> run "ssh -L 8080:localhost:80 user@remote-host"

```markscript
# Local port forwarding: local:8080 -> remote:80
push("ssh -L 8080:localhost:80 user@remote-host")
call("run")
```

> run "ssh -R 9000:localhost:3000 user@remote-host"

```markscript
# Remote port forwarding: remote:9000 -> local:3000
push("ssh -R 9000:localhost:3000 user@remote-host")
call("run")
```

---

## config

Manage SSH configuration entries.

> run "cat ~/.ssh/config"

```markscript
# Show the SSH config file
push("cat ~/.ssh/config")
call("run")
```

> run "echo -e \"Host my-server\\n  HostName 192.168.1.100\\n  User admin\\n  IdentityFile ~/.ssh/id_ed25519\" >> ~/.ssh/config"

```markscript
# Append a host configuration block
push("echo -e \"Host my-server\\n  HostName 192.168.1.100\\n  User admin\\n  IdentityFile ~/.ssh/id_ed25519\" >> ~/.ssh/config")
call("run")
```

---

## agent

Manage the SSH agent for key forwarding.

> run "eval \"$(ssh-agent -s)\" && ssh-add ~/.ssh/id_ed25519"

```markscript
# Start agent and add a key
push("eval \"$(ssh-agent -s)\" && ssh-add ~/.ssh/id_ed25519")
call("run")
```

> run "ssh-add -l"

```markscript
# List keys currently loaded in the agent
push("ssh-add -l")
call("run")
```

> run "ssh-agent -k"

```markscript
# Kill the SSH agent
push("ssh-agent -k")
call("run")
```
