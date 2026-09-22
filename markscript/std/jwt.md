# JWT

Markscript JWT (JSON Web Token) --- encode, decode, verify.
Dispatches to openssl for HMAC signing and verification.

---

## encode_hs256

Encode a JWT with HS256 (HMAC-SHA256) signing.

> run "echo -n 'header.payload' | openssl dgst -sha256 -hmac 'secret' | xxd -r -p | base64 | tr -d '=' | tr '+/' '-_'"

---

## decode

Decode a JWT payload (base64url decode the middle segment).

> run "echo 'PAYLOAD_SEGMENT' | base64 -d 2>/dev/null || echo 'PAYLOAD_SEGMENT===' | base64 -d"

---

## verify_hs256

Verify a JWT signature against a secret.

> run "echo -n 'header.payload' | openssl dgst -sha256 -hmac 'secret'"
> assert computed_signature provided_signature

---

## claims

Extract claims from a decoded JWT payload.

> run "echo 'DECODED_PAYLOAD' | python -c \"import sys,json; print(json.dumps(json.load(sys.stdin), indent=2))\""

---

## header_info

Extract and decode the JWT header.

> run "echo 'HEADER_B64' | base64 -d 2>/dev/null"

---

## sign_rs256

Sign a JWT with RS256 (RSA-SHA256).

> run "echo -n 'header.payload' | openssl dgst -sha256 -sign private_key.pem | base64 | tr -d '=' | tr '+/' '-_'"

---

## verify_rs256

Verify an RS256 JWT signature.

> run "echo -n 'header.payload' | openssl dgst -sha256 -verify public_key.pem -signature signature.bin"

---

## expiry_check

Check if a JWT has expired based on the exp claim.

> print "Checking JWT exp claim against current time"

---

## es256_sign

Sign a JWT with ES256 (ECDSA P-256).

> run "echo -n 'header.payload' | openssl dgst -sha256 -sign ecdsa_key.pem | base64 | tr -d '=' | tr '+/' '-_'"
