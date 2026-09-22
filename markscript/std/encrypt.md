# Encrypt

Markscript encryption --- symmetric and asymmetric ciphers via OpenSSL.
Dispatches through the IVT to OpenSSL for all cryptographic operations.

---

## aes_encrypt

Encrypt a file with AES-256-CBC. Prompts for passphrase via IVT.

> run "openssl enc -aes-256-cbc -salt -in plain.txt -out encrypted.bin"

```markscript
# AES-256-CBC encrypt a file
let input = "plain.txt"
let output = "encrypted.bin"
push("openssl enc -aes-256-cbc -salt -in \"" + input + "\" -out \"" + output + "\"")
call("run")
```

---

## aes_decrypt

Decrypt a file previously encrypted with AES-256-CBC.

> run "openssl enc -aes-256-cbc -d -in encrypted.bin -out decrypted.txt"

```markscript
# AES-256-CBC decrypt a file
let input = "encrypted.bin"
let output = "decrypted.txt"
push("openssl enc -aes-256-cbc -d -in \"" + input + "\" -out \"" + output + "\"")
call("run")
```

---

## aes_encrypt_string

Encrypt a plaintext string directly using AES-256-CBC and base64 encode.

> run "echo \"secret data\" | openssl enc -aes-256-cbc -salt -base64"

```markscript
# Encrypt a string to base64 ciphertext
let data = "secret data"
push("echo \"" + data + "\" | openssl enc -aes-256-cbc -salt -base64")
call("run")
```

---

## aes_decrypt_string

Decrypt a base64 AES ciphertext back to plaintext.

> run "echo \"U2FsdGVkX...\" | openssl enc -aes-256-cbc -d -base64"

```markscript
# Decrypt base64 ciphertext to string
let ciphertext = "U2FsdGVkX1..."  # placeholder
push("echo \"" + ciphertext + "\" | openssl enc -aes-256-cbc -d -base64")
call("run")
```

---

## rsa_encrypt

Encrypt a file with an RSA public key.

> run "openssl pkeyutl -encrypt -pubin -inkey public.pem -in plain.txt -out encrypted.bin"

```markscript
# RSA encrypt a file with a public key
let keypath = "public.pem"
let input = "plain.txt"
let output = "encrypted.bin"
push("openssl pkeyutl -encrypt -pubin -inkey \"" + keypath + "\" -in \"" + input + "\" -out \"" + output + "\"")
call("run")
```

---

## rsa_decrypt

Decrypt a file with the corresponding RSA private key.

> run "openssl pkeyutl -decrypt -inkey private.pem -in encrypted.bin -out decrypted.txt"

```markscript
# RSA decrypt a file with a private key
let keypath = "private.pem"
let input = "encrypted.bin"
let output = "decrypted.txt"
push("openssl pkeyutl -decrypt -inkey \"" + keypath + "\" -in \"" + input + "\" -out \"" + output + "\"")
call("run")
```

---

## keygen

Generate a 2048-bit RSA key pair and save both keys.

> run "openssl genrsa -out private.pem 2048"
> run "openssl rsa -pubout -in private.pem -out public.pem"

```markscript
# Generate RSA key pair
push("openssl genrsa -out private.pem 2048")
call("run")
push("openssl rsa -pubout -in private.pem -out public.pem")
call("run")
```

---

## iv

Generate a random 16-byte initialization vector and encode as hex.

> run "openssl rand -hex 16"

```markscript
# Generate random IV for AES
push("openssl rand -hex 16")
call("run")
```

---

## aes_gcm_encrypt

Encrypt with AES-256-GCM (authenticated encryption, includes tag).

> run "openssl enc -aes-256-gcm -salt -in plain.txt -out encrypted.bin"

```markscript
# AES-256-GCM encrypt a file
let input = "plain.txt"
let output = "encrypted.bin"
push("openssl enc -aes-256-gcm -salt -in \"" + input + "\" -out \"" + output + "\"")
call("run")
```

---

## aes_gcm_decrypt

Decrypt a file encrypted with AES-256-GCM.

> run "openssl enc -aes-256-gcm -d -in encrypted.bin -out decrypted.txt"

```markscript
# AES-256-GCM decrypt a file
let input = "encrypted.bin"
let output = "decrypted.txt"
push("openssl enc -aes-256-gcm -d -in \"" + input + "\" -out \"" + output + "\"")
call("run")
```

---

## chacha20_encrypt

Encrypt with ChaCha20 cipher (OpenSSL 1.1+).

> run "openssl enc -chacha20 -salt -in plain.txt -out encrypted.bin"

```markscript
# ChaCha20 encrypt a file
let input = "plain.txt"
let output = "encrypted.bin"
push("openssl enc -chacha20 -salt -in \"" + input + "\" -out \"" + output + "\"")
call("run")
```

---

## chacha20_decrypt

Decrypt a file encrypted with ChaCha20.

> run "openssl enc -chacha20 -d -in encrypted.bin -out decrypted.txt"

```markscript
# ChaCha20 decrypt a file
let input = "encrypted.bin"
let output = "decrypted.txt"
push("openssl enc -chacha20 -d -in \"" + input + "\" -out \"" + output + "\"")
call("run")
```
