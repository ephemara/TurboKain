# Vault

Markscript secret vault - encrypted storage for secrets, keys, and sensitive configuration.
Dispatches through the IVT to filesystem operations with OpenSSL-based encryption.

---

## read

Read a secret from the vault by key name. Decrypts the stored value.

> run "openssl enc -aes-256-cbc -d -in vault/secret.bin -pass pass:vaultkey 2>nul"

```markscript
# Read and decrypt a vault secret
let key = "api_key"
let path = "vault/" + key + ".bin"
push("openssl enc -aes-256-cbc -d -in \"" + path + "\" -pass pass:vaultkey 2>nul")
call("run")
```

---

## write

Write a secret to the vault by key name. Encrypts before storing.

> run "openssl enc -aes-256-cbc -salt -in plain.txt -out vault/secret.bin -pass pass:vaultkey"

```markscript
# Encrypt and store a vault secret
let key = "api_key"
let value = "sk-1234567890abcdef"
let tmp = "__vault_tmp.txt"
let path = "vault/" + key + ".bin"
# Write plaintext to temp file
push("echo \"" + value + "\" > \"" + tmp + "\"")
call("run")
# Encrypt and store in vault
push("openssl enc -aes-256-cbc -salt -in \"" + tmp + "\" -out \"" + path + "\" -pass pass:vaultkey")
call("run")
# Remove plaintext temp file
push("del \"" + tmp + "\"")
call("run")
```

---

## delete

Delete a secret from the vault by key name.

> run "del vault/api_key.bin"

```markscript
# Remove a secret from the vault
let key = "api_key"
let path = "vault/" + key + ".bin"
push("del \"" + path + "\"")
call("run")
```

---

## list

List all secret keys currently stored in the vault.

> run "dir /b vault\\*.bin"

```markscript
# List all vault secrets
push("dir /b vault\\*.bin")
call("run")
```

---

## seal

Seal the vault -- encrypt the vault index and flush all cached plaintext keys.

> run "openssl enc -aes-256-cbc -salt -in vault_index.json -out vault_index.enc -pass pass:sealkey"
> run "del vault_index.json"

```markscript
# Seal the vault for secure storage
push("openssl enc -aes-256-cbc -salt -in vault_index.json -out vault_index.enc -pass pass:sealkey")
call("run")
push("del vault_index.json")
call("run")
```

---

## unseal

Unseal the vault --- decrypt the vault index and load keys into memory.

> run "openssl enc -aes-256-cbc -d -in vault_index.enc -out vault_index.json -pass pass:sealkey"

```markscript
# Unseal the vault, loading key index
push("openssl enc -aes-256-cbc -d -in vault_index.enc -out vault_index.json -pass pass:sealkey")
call("run")
```

---

## status

Check whether the vault is sealed or unsealed.

> file exists "vault_index.json"

```markscript
# Check vault status
push("vault_index.json")
call("file exists")
# Result is 1 if unsealed (index exists), 0 if sealed
```

---

## policy

Display the access control policy for the vault.

> read file "vault_policy.json"

```markscript
# Read vault policy
push("vault_policy.json")
call("read file")
```

---

## rotate_master_key

Re-encrypt all vault secrets with a new master key.

> run "python -c \"# Rotate all vault keys with new master secret\""

```markscript
# Re-encrypt every secret with a new key
let old_key = "oldvaultkey"
let new_key = "newvaultkey"
push("Rotating vault master key")
call("print")
# In practice: decrypt each secret with old_key, re-encrypt with new_key
```

---

## read_json

Read a secret from the vault and parse it as structured JSON.

> run "openssl enc -aes-256-cbc -d -in vault/config.bin -pass pass:vaultkey"

```markscript
# Read and decrypt a JSON config from the vault
let key = "config"
let path = "vault/" + key + ".bin"
push("openssl enc -aes-256-cbc -d -in \"" + path + "\" -pass pass:vaultkey")
call("run")
# Result is decrypted JSON string
```

---

## write_json

Write a structured JSON value as an encrypted vault secret.

> run "echo {\"url\":\"https://example.com\"} > tmp.json"
> run "openssl enc -aes-256-cbc -salt -in tmp.json -out vault/config.bin -pass pass:vaultkey"

```markscript
# Encrypt and store a JSON secret
let key = "config"
let json = "{\"url\":\"https://example.com\",\"port\":443}"
let tmp = "__vault_tmp.json"
let path = "vault/" + key + ".bin"
push("echo " + json + " > \"" + tmp + "\"")
call("run")
push("openssl enc -aes-256-cbc -salt -in \"" + tmp + "\" -out \"" + path + "\" -pass pass:vaultkey")
call("run")
push("del \"" + tmp + "\"")
call("run")
```

---

## init

Initialize a new empty vault directory and index.

> run "mkdir vault"
> run "echo {} > vault_index.json"

```markscript
# Create a new vault
push("mkdir vault 2>nul")
call("run")
push("echo {} > vault_index.json")
call("run")
push("echo {} > vault_policy.json")
call("run")
```
