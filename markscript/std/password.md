# Password

Markscript password management - hashing, verification, and generation.
Dispatches to openssl and Python bcrypt/argon2 through the IVT.

---

## hash_sha256

Hash a password with SHA-256.

> run "echo -n 'mypassword' | openssl dgst -sha256"

---

## hash_bcrypt

Hash a password with bcrypt via Python.

> run "python -c \"import bcrypt; print(bcrypt.hashpw(b'mypass', bcrypt.gensalt()).decode())\""

---

## verify_bcrypt

Verify a password against a bcrypt hash.

> run "python -c \"import bcrypt; print(bcrypt.checkpw(b'mypass', b'STORED_HASH'))\""

---

## verify_sha256

Verify a password against a stored SHA-256 hash.

> run "echo -n 'entered_pass' | openssl dgst -sha256"
> assert computed_hash stored_hash

---

## strength

Check password strength (length, complexity).

> print "Password must be 8+ chars with upper, lower, digit, special"

---

## generate

Generate a random password with openssl.

> run "openssl rand -base64 16"

---

## generate_readable

Generate a readable password (no ambiguous chars).

> run "openssl rand -base64 12 | tr -dc 'A-Za-z0-9'"

---

## argon2_hash

Hash with argon2 via Python.

> run "python -c \"from argon2 import PasswordHasher; print(PasswordHasher().hash(b'mypass'))\""

---

## argon2_verify

Verify an argon2 hash via Python.

> run "python -c \"from argon2 import PasswordHasher; print(PasswordHasher().verify('HASH', 'mypass'))\""

---

## entropy

Estimate password entropy.

> run "echo -n 'mypassword' | ent"
