# Tls

Markscript TLS -- secure connection management, handshake inspection, cipher suite querying.
Dispatches through the IVT to OpenSSL for all secure channel operations.

---

## connect

Establish a TLS connection to a remote host and capture its certificate chain.

> run "openssl s_client -connect example.com:443 -servername example.com < /dev/null"

```markscript
# Connect to a TLS server
let host = "example.com"
let port = 443
push("openssl s_client -connect " + host + ":" + port + " -servername " + host + " < /dev/null")
call("run")
```

---

## verify

Verify a TLS connection against a specific CA bundle.

> run "openssl s_client -connect example.com:443 -CAfile ca.pem -verify_return_error < /dev/null"

```markscript
# Verify TLS with custom CA
let host = "example.com"
let ca = "ca.pem"
push("openssl s_client -connect " + host + ":443 -CAfile \"" + ca + "\" -verify_return_error < /dev/null")
call("run")
```

---

## handshake

Inspect the TLS handshake details -- protocol version, cipher suite, key exchange.

> run "openssl s_client -connect example.com:443 -msg < /dev/null"

```markscript
# Capture full handshake messages
let host = "example.com"
push("openssl s_client -connect " + host + ":443 -msg < /dev/null")
call("run")
```

---

## cipher_list

List all cipher suites supported by the system's OpenSSL library.

> run "openssl ciphers -v"

```markscript
# List available TLS cipher suites
push("openssl ciphers -v")
call("run")
```

---

## version

Display the system's OpenSSL and TLS library version.

> run "openssl version -a"

```markscript
# Show OpenSSL version info
push("openssl version -a")
call("run")
```

---

## cert_info

Extract and display the server certificate details from a TLS connection.

> run "openssl s_client -connect example.com:443 < /dev/null | openssl x509 -text -noout"

```markscript
# Get server certificate info
let host = "example.com"
push("openssl s_client -connect " + host + ":443 < /dev/null | openssl x509 -text -noout")
call("run")
```

---

## check_revocation

Check whether a server certificate has been revoked via OCSP.

> run "openssl ocsp -issuer ca.pem -cert cert.pem -url http://ocsp.example.com -resp_text"

```markscript
# OCSP revocation check
let cert = "cert.pem"
let ca = "ca.pem"
let ocsp_url = "http://ocsp.example.com"
push("openssl ocsp -issuer \"" + ca + "\" -cert \"" + cert + "\" -url " + ocsp_url + " -resp_text")
call("run")
```

---

## protocol_scan

Scan a server to determine which TLS protocol versions it supports.

> run "openssl s_client -connect host:443 -tls1_3 < /dev/null"
> run "openssl s_client -connect host:443 -tls1_2 < /dev/null"
> run "openssl s_client -connect host:443 -tls1_1 < /dev/null"

```markscript
# Probe which TLS versions a server supports
let host = "example.com"
push("openssl s_client -connect " + host + ":443 -tls1_3 < /dev/null")
call("run")
push("openssl s_client -connect " + host + ":443 -tls1_2 < /dev/null")
call("run")
```

---

## sni_check

Check if Server Name Indication (SNI) is configured for a specific hostname.

> run "openssl s_client -connect 1.2.3.4:443 -servername example.com < /dev/null"

```markscript
# Test SNI by connecting with explicit hostname
let host = "example.com"
let ip = "1.2.3.4"
push("openssl s_client -connect " + ip + ":443 -servername " + host + " < /dev/null")
call("run")
```

---

## ocsp_stapling

Check whether a server supports OCSP stapling.

> run "openssl s_client -connect example.com:443 -status < /dev/null"

```markscript
# Request OCSP stapling during handshake
let host = "example.com"
push("openssl s_client -connect " + host + ":443 -status < /dev/null")
call("run")
```

---

## weak_cipher_check

Check if a server allows any known weak cipher suites.

> run "openssl s_client -connect example.com:443 -cipher 'ALL:!HIGH:!MEDIUM' < /dev/null"

```markscript
# Test for weak cipher acceptance
let host = "example.com"
push("openssl s_client -connect " + host + ":443 -cipher 'ALL:!HIGH:!MEDIUM' < /dev/null")
call("run")
```

---

## start_ssl_inspection

Start a local packet capture to inspect encrypted traffic (placeholder).

> print "SSL/TLS inspection requires man-in-the-middle proxy setup"

```markscript
# SSL inspection placeholder
push("SSL/TLS inspection requires man-in-the-middle proxy setup")
call("print")
```
