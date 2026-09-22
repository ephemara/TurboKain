# Cert

Markscript certificate management -- X.509 certificate operations via OpenSSL.
Dispatches through the IVT to OpenSSL for all certificate operations.

---

## generate

Generate a self-signed X.509 certificate with a new RSA key.

> run "openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj \"/CN=localhost\""

```markscript
# Generate a self-signed certificate
let cn = "localhost"
let keyfile = "key.pem"
let certfile = "cert.pem"
push("openssl req -x509 -newkey rsa:2048 -keyout \"" + keyfile + "\" -out \"" + certfile + "\" -days 365 -nodes -subj \"/CN=" + cn + "\"")
call("run")
```

---

## sign

Sign a certificate signing request (CSR) with a CA certificate.

> run "openssl x509 -req -in request.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out signed.pem -days 365"

```markscript
# Sign a CSR with a CA
let csr = "request.csr"
let ca = "ca.pem"
let cakey = "ca.key"
let output = "signed.pem"
push("openssl x509 -req -in \"" + csr + "\" -CA \"" + ca + "\" -CAkey \"" + cakey + "\" -CAcreateserial -out \"" + output + "\" -days 365")
call("run")
```

---

## verify

Verify a certificate against a CA chain.

> run "openssl verify -CAfile ca.pem cert.pem"

```markscript
# Verify a certificate
let cert = "cert.pem"
let ca = "ca.pem"
push("openssl verify -CAfile \"" + ca + "\" \"" + cert + "\"")
call("run")
```

---

## fingerprint

Compute the SHA-256 fingerprint of a certificate.

> run "openssl x509 -fingerprint -sha256 -in cert.pem -noout"

```markscript
# Get certificate fingerprint
let cert = "cert.pem"
push("openssl x509 -fingerprint -sha256 -in \"" + cert + "\" -noout")
call("run")
```

---

## info

Display human-readable information about a certificate.

> run "openssl x509 -in cert.pem -text -noout"

```markscript
# Show certificate details
let cert = "cert.pem"
push("openssl x509 -in \"" + cert + "\" -text -noout")
call("run")
```

---

## chain

Download and assemble the full certificate chain for a host.

> run "openssl s_client -connect example.com:443 -showcerts < /dev/null"

```markscript
# Fetch the full TLS certificate chain
let host = "example.com"
push("openssl s_client -connect " + host + ":443 -showcerts < /dev/null")
call("run")
```

---

## self_signed

Create a complete self-signed CA certificate with extensions.

> run "openssl req -x509 -newkey rsa:4096 -keyout ca.key -out ca.pem -days 3650 -nodes -extensions v3_ca -subj \"/CN=My Root CA\""

```markscript
# Create a root CA self-signed certificate
let keyfile = "ca.key"
let certfile = "ca.pem"
let subject = "/CN=My Root CA"
let days = 3650
push("openssl req -x509 -newkey rsa:4096 -keyout \"" + keyfile + "\" -out \"" + certfile + "\" -days " + days + " -nodes -extensions v3_ca -subj \"" + subject + "\"")
call("run")
```

---

## pem_to_der

Convert a PEM-encoded certificate to DER format.

> run "openssl x509 -in cert.pem -outform DER -out cert.der"

```markscript
# Convert PEM certificate to DER binary
let pem = "cert.pem"
let der = "cert.der"
push("openssl x509 -in \"" + pem + "\" -outform DER -out \"" + der + "\"")
call("run")
```

---

## der_to_pem

Convert a DER-encoded certificate to PEM format.

> run "openssl x509 -in cert.der -inform DER -out cert.pem -outform PEM"

```markscript
# Convert DER certificate to PEM text
let der = "cert.der"
let pem = "cert.pem"
push("openssl x509 -in \"" + der + "\" -inform DER -out \"" + pem + "\" -outform PEM")
call("run")
```

---

## expiry

Check when a certificate expires.

> run "openssl x509 -in cert.pem -noout -enddate"

```markscript
# Get certificate expiry date
let cert = "cert.pem"
push("openssl x509 -in \"" + cert + "\" -noout -enddate")
call("run")
```

---

## subject

Extract the subject DN from a certificate.

> run "openssl x509 -in cert.pem -noout -subject"

```markscript
# Get certificate subject
let cert = "cert.pem"
push("openssl x509 -in \"" + cert + "\" -noout -subject")
call("run")
```

---

## issuer

Extract the issuer DN from a certificate.

> run "openssl x509 -in cert.pem -noout -issuer"

```markscript
# Get certificate issuer
let cert = "cert.pem"
push("openssl x509 -in \"" + cert + "\" -noout -issuer")
call("run")
```
