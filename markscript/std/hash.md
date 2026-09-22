# Hash

Markscript hashing - cryptographic and checksum hashing via openssl CLI.
All hashes are computed by dispatching to `openssl dgst` through the IVT.

---

## md5

Compute MD5 hash of a string.

> run "echo -n 'hello' | openssl dgst -md5"

---

## sha1

Compute SHA-1 hash of a string.

> run "echo -n 'hello' | openssl dgst -sha1"

---

## sha256

Compute SHA-256 hash of a string.

> run "echo -n 'hello' | openssl dgst -sha256"

---

## sha512

Compute SHA-512 hash of a string.

> run "echo -n 'hello' | openssl dgst -sha512"

---

## blake2

Compute BLAKE2b hash of a string.

> run "echo -n 'hello' | openssl dgst -blake2b512"

---

## file_hash

Compute SHA-256 hash of a file.

> run "openssl dgst -sha256 path/to/file.txt"

---

## hmac

Compute HMAC-SHA256 of a message with a key.

> run "echo -n 'message' | openssl dgst -sha256 -hmac 'secret_key'"

---

## compare

Compare two hashes for equality.

> read file "hash1.txt"
> read file "hash2.txt"
> assert hash1 hash2

---

## sha256_multi

Hash multiple strings and compare.

> run "for s in hello world test; do echo -n \$s | openssl dgst -sha256; done"

---

## ripemd160

Compute RIPEMD-160 hash.

> run "echo -n 'hello' | openssl dgst -ripemd160"
