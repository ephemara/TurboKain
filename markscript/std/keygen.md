# Keygen

Markscript key generation --- RSA, ECDSA, Ed25519, Diffie-Hellman keys and passphrase management.
Dispatches through the IVT to OpenSSL for all key generation operations.

---

## rsa

Generate an RSA private key with configurable bit size.

> run "openssl genrsa -out private.pem 4096"

```markscript
# Generate 4096-bit RSA key
let bits = 4096
let out = "private.pem"
push("openssl genrsa -out \"" + out + "\" " + bits)
call("run")
```

---

## rsa_extract_public

Extract the RSA public key from a private key.

> run "openssl rsa -in private.pem -pubout -out public.pem"

```markscript
# Extract public key from private key
let priv = "private.pem"
let pub = "public.pem"
push("openssl rsa -in \"" + priv + "\" -pubout -out \"" + pub + "\"")
call("run")
```

---

## ecdsa

Generate an ECDSA key pair using the P-256 (prime256v1) curve.

> run "openssl ecparam -genkey -name prime256v1 -out ecdsa.pem"

```markscript
# Generate ECDSA key on P-256
let curve = "prime256v1"
let out = "ecdsa.pem"
push("openssl ecparam -genkey -name \"" + curve + "\" -out \"" + out + "\"")
call("run")
```

---

## ecdsa_secp384r1

Generate an ECDSA key pair using the P-384 (secp384r1) curve.

> run "openssl ecparam -genkey -name secp384r1 -out ecdsa_384.pem"

```markscript
# Generate ECDSA key on P-384
let curve = "secp384r1"
let out = "ecdsa_384.pem"
push("openssl ecparam -genkey -name \"" + curve + "\" -out \"" + out + "\"")
call("run")
```

---

## ed25519

Generate an Ed25519 key pair.

> run "openssl genpkey -algorithm ED25519 -out ed25519.pem"

```markscript
# Generate Ed25519 private key
let out = "ed25519.pem"
push("openssl genpkey -algorithm ED25519 -out \"" + out + "\"")
call("run")
```

---

## ed25519_extract_public

Extract the Ed25519 public key from a private key.

> run "openssl pkey -in ed25519.pem -pubout -out ed25519_pub.pem"

```markscript
# Extract Ed25519 public key
let priv = "ed25519.pem"
let pub = "ed25519_pub.pem"
push("openssl pkey -in \"" + priv + "\" -pubout -out \"" + pub + "\"")
call("run")
```

---

## dhparams

Generate Diffie-Hellman parameters for key exchange.

> run "openssl dhparam -out dhparams.pem 2048"

```markscript
# Generate DH parameters
let bits = 2048
let out = "dhparams.pem"
push("openssl dhparam -out \"" + out + "\" " + bits)
call("run")
```

---

## passphrase_protect

Add a passphrase to an existing private key.

> run "openssl rsa -aes256 -in private.pem -out private_enc.pem -passout pass:"

```markscript
# Encrypt a private key with a passphrase
let input = "private.pem"
let output = "private_enc.pem"
push("openssl rsa -aes256 -in \"" + input + "\" -out \"" + output + "\" -passout pass:")
call("run")
```

---

## passphrase_remove

Remove a passphrase from an encrypted private key.

> run "openssl rsa -in private_enc.pem -out private_dec.pem"

```markscript
# Decrypt a passphrase-protected key
let input = "private_enc.pem"
let output = "private_dec.pem"
push("openssl rsa -in \"" + input + "\" -out \"" + output + "\"")
call("run")
```

---

## convert_format

Convert a private key between PEM and DER formats.

> run "openssl pkey -in key.pem -outform DER -out key.der"

```markscript
# Convert PEM private key to DER
let input = "key.pem"
let output = "key.der"
push("openssl pkey -in \"" + input + "\" -outform DER -out \"" + output + "\"")
call("run")
```

---

## ec_curves

List all available elliptic curves supported by the system's OpenSSL.

> run "openssl ecparam -list_curves"

```markscript
# List available EC curves
push("openssl ecparam -list_curves")
call("run")
```

---

## key_info

Display detailed information about a private key.

> run "openssl pkey -in private.pem -text -noout"

```markscript
# Show key algorithm, size, curves, etc.
let keypath = "private.pem"
push("openssl pkey -in \"" + keypath + "\" -text -noout")
call("run")
```
