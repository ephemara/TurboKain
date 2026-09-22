# Gpg

Markscript GPG - GNU Privacy Guard encryption, signing, key management.
Dispatches through the IVT to gpg for all cryptographic operations.

---

## encrypt

Encrypt a file symmetrically with a passphrase using GPG.

> run "gpg --symmetric --cipher-algo AES256 -o encrypted.gpg plain.txt"

```markscript
# Symmetrically encrypt a file
let input = "plain.txt"
let output = "encrypted.gpg"
push("gpg --symmetric --cipher-algo AES256 -o \"" + output + "\" \"" + input + "\"")
call("run")
```

---

## encrypt_public

Encrypt a file for a specific recipient using their public key.

> run "gpg --encrypt --recipient alice@example.com -o encrypted.gpg plain.txt"

```markscript
# Encrypt for a recipient
let recipient = "alice@example.com"
let input = "plain.txt"
let output = "encrypted.gpg"
push("gpg --encrypt --recipient \"" + recipient + "\" -o \"" + output + "\" \"" + input + "\"")
call("run")
```

---

## decrypt

Decrypt a GPG-encrypted file.

> run "gpg --decrypt -o decrypted.txt encrypted.gpg"

```markscript
# Decrypt a GPG file
let input = "encrypted.gpg"
let output = "decrypted.txt"
push("gpg --decrypt -o \"" + output + "\" \"" + input + "\"")
call("run")
```

---

## sign

Sign a file with your GPG private key (clearsign).

> run "gpg --clearsign -o document.sig document.txt"

```markscript
# Clearsign a file
let input = "document.txt"
let output = "document.sig"
push("gpg --clearsign -o \"" + output + "\" \"" + input + "\"")
call("run")
```

---

## verify

Verify a GPG signature against a signed file.

> run "gpg --verify document.sig"

```markscript
# Verify a GPG signature
let sigfile = "document.sig"
push("gpg --verify \"" + sigfile + "\"")
call("run")
```

---

## keygen

Generate a new GPG key pair (batch mode for unattended generation).

> run "gpg --batch --passphrase '' --quick-gen-key 'Alice <alice@example.com>' default default"

```markscript
# Generate a new GPG key
let user = "Alice <alice@example.com>"
push("gpg --batch --passphrase '' --quick-gen-key '" + user + "' default default")
call("run")
```

---

## import_key

Import a GPG key from an ASCII-armored key file.

> run "gpg --import public-key.asc"

```markscript
# Import a GPG key
let keyfile = "public-key.asc"
push("gpg --import \"" + keyfile + "\"")
call("run")
```

---

## export_key

Export your public GPG key in ASCII-armored format.

> run "gpg --export --armor -o public-key.asc alice@example.com"

```markscript
# Export public key
let identity = "alice@example.com"
let output = "public-key.asc"
push("gpg --export --armor -o \"" + output + "\" \"" + identity + "\"")
call("run")
```

---

## export_private

Export your private GPG key in ASCII-armored format.

> run "gpg --export-secret-keys --armor -o private-key.asc alice@example.com"

```markscript
# Export private key
let identity = "alice@example.com"
let output = "private-key.asc"
push("gpg --export-secret-keys --armor -o \"" + output + "\" \"" + identity + "\"")
call("run")
```

---

## list_keys

List all public keys in your GPG keyring.

> run "gpg --list-keys"

```markscript
# List public keys
push("gpg --list-keys")
call("run")
```

---

## list_secret_keys

List all secret (private) keys in your GPG keyring.

> run "gpg --list-secret-keys"

```markscript
# List private keys
push("gpg --list-secret-keys")
call("run")
```

---

## delete_key

Delete a GPG key from your keyring.

> run "gpg --delete-key alice@example.com"

```markscript
# Delete a public key
let identity = "alice@example.com"
push("gpg --delete-key \"" + identity + "\"")
call("run")
```

---

## encrypt_symmetric_aes256

Encrypt a file symmetrically using AES-256 (no keyring needed).

> run "gpg --symmetric --cipher-algo AES256 --no-symkey-cache -o encrypted.gpg secret.txt"

```markscript
# AES-256 symmetric encryption without caching
let input = "secret.txt"
let output = "encrypted.gpg"
push("gpg --symmetric --cipher-algo AES256 --no-symkey-cache -o \"" + output + "\" \"" + input + "\"")
call("run")
```

---

## trust_key

Set the trust level for an imported GPG key.

> run "echo -e '5\ny\n' | gpg --command-fd 0 --edit-key alice@example.com trust"

```markscript
# Set ultimate trust on a key
let identity = "alice@example.com"
push("echo -e '5\\ny\\n' | gpg --command-fd 0 --edit-key \"" + identity + "\" trust")
call("run")
```

---

## encrypt_sign

Encrypt and sign a file for authenticity and confidentiality.

> run "gpg --encrypt --sign --recipient alice@example.com -o encrypted.gpg message.txt"

```markscript
# Simultaneously encrypt and sign
let recipient = "alice@example.com"
let input = "message.txt"
let output = "encrypted.gpg"
push("gpg --encrypt --sign --recipient \"" + recipient + "\" -o \"" + output + "\" \"" + input + "\"")
call("run")
```

---

## refresh_keys

Refresh all keys from a keyserver.

> run "gpg --refresh-keys"

```markscript
# Update keys from keyserver
push("gpg --refresh-keys")
call("run")
```
