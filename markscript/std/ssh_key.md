# Ssh

Markscript SSH key management -- generate, fingerprint, convert, and manage SSH keys.
Dispatches through the IVT to ssh-keygen and OpenSSL.

---

## generate

Generate an RSA SSH key pair with configurable bit size.

> run "ssh-keygen -t rsa -b 4096 -f id_rsa -N \"\" -C \"user@host\""

```markscript
# Generate SSH RSA key pair
let bits = 4096
let file = "id_rsa"
let comment = "user@host"
push("ssh-keygen -t rsa -b " + bits + " -f \"" + file + "\" -N \"\" -C \"" + comment + "\"")
call("run")
```

---

## generate_ecdsa

Generate an ECDSA SSH key pair on the NIST P-256 curve.

> run "ssh-keygen -t ecdsa -b 256 -f id_ecdsa -N \"\" -C \"user@host\""

```markscript
# Generate ECDSA SSH key
let bits = 256
let file = "id_ecdsa"
let comment = "user@host"
push("ssh-keygen -t ecdsa -b " + bits + " -f \"" + file + "\" -N \"\" -C \"" + comment + "\"")
call("run")
```

---

## generate_ed25519

Generate an Ed25519 SSH key pair (modern, fastest).

> run "ssh-keygen -t ed25519 -f id_ed25519 -N \"\" -C \"user@host\""

```markscript
# Generate Ed25519 SSH key (recommended)
let file = "id_ed25519"
let comment = "user@host"
push("ssh-keygen -t ed25519 -f \"" + file + "\" -N \"\" -C \"" + comment + "\"")
call("run")
```

---

## fingerprint

Extract the fingerprint of an SSH public key.

> run "ssh-keygen -lf id_rsa.pub"

```markscript
# Get SSH key fingerprint
let pubkey = "id_rsa.pub"
push("ssh-keygen -lf \"" + pubkey + "\"")
call("run")
```

---

## fingerprint_hash

Extract the SHA-256 hash fingerprint of an SSH key.

> run "ssh-keygen -lf id_rsa.pub -E sha256"

```markscript
# Get SHA-256 fingerprint
let pubkey = "id_rsa.pub"
push("ssh-keygen -lf \"" + pubkey + "\" -E sha256")
call("run")
```

---

## convert_openssh_to_pem

Convert an OpenSSH private key to PEM format for OpenSSL compatibility.

> run "ssh-keygen -p -m PEM -f id_rsa -N \"\""

```markscript
# Convert to PEM format
let keyfile = "id_rsa"
push("ssh-keygen -p -m PEM -f \"" + keyfile + "\" -N \"\"")
call("run")
```

---

## convert_pem_to_openssh

Convert a PEM private key to OpenSSH format.

> run "ssh-keygen -p -m RFC4716 -f id_rsa -N \"\""

```markscript
# Convert to OpenSSH format
let keyfile = "id_rsa"
push("ssh-keygen -p -m RFC4716 -f \"" + keyfile + "\" -N \"\"")
call("run")
```

---

## agent_add

Add an SSH private key to the SSH agent for passwordless authentication.

> run "ssh-add id_rsa"

```markscript
# Add key to SSH agent
let keyfile = "id_rsa"
push("ssh-add \"" + keyfile + "\"")
call("run")
```

---

## agent_list

List all keys currently loaded in the SSH agent.

> run "ssh-add -l"

```markscript
# List SSH agent keys
push("ssh-add -l")
call("run")
```

---

## agent_remove

Remove a specific key from the SSH agent.

> run "ssh-add -d id_rsa.pub"

```markscript
# Remove key from SSH agent
let keyfile = "id_rsa.pub"
push("ssh-add -d \"" + keyfile + "\"")
call("run")
```

---

## agent_remove_all

Remove all keys from the SSH agent.

> run "ssh-add -D"

```markscript
# Remove all keys from agent
push("ssh-add -D")
call("run")
```

---

## sign

Sign a file using an SSH private key.

> run "ssh-keygen -Y sign -f id_rsa -n file data.txt"

```markscript
# Sign a file with SSH key
let key = "id_rsa"
let file = "data.txt"
let namespace = "file"
push("ssh-keygen -Y sign -f \"" + key + "\" -n " + namespace + " \"" + file + "\"")
call("run")
```

---

## verify_sig

Verify an SSH signature against a public key.

> run "ssh-keygen -Y verify -f allowed_signers -I user@host -n file -s data.txt.sig < data.txt"

```markscript
# Verify SSH signature
let pubkeys = "allowed_signers"
let identity = "user@host"
let sig = "data.txt.sig"
let data = "data.txt"
push("ssh-keygen -Y verify -f \"" + pubkeys + "\" -I " + identity + " -n file -s \"" + sig + "\" < \"" + data + "\"")
call("run")
```

---

## generate_passphrase_protected

Generate an SSH key with a passphrase for encryption at rest.

> run "ssh-keygen -t ed25519 -f id_protected -N \"passphrase123\" -C \"user@host\""

```markscript
# Generate passphrase-protected SSH key
let file = "id_protected"
let passphrase = "passphrase123"
let comment = "user@host"
push("ssh-keygen -t ed25519 -f \"" + file + "\" -N \"" + passphrase + "\" -C \"" + comment + "\"")
call("run")
```
