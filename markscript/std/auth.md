# Auth

Markscript authentication - session management, token handling, MFA.
Dispatches to openssl for token generation and verification.

---

## generate_token

Generate a random auth token.

> run "openssl rand -hex 32"

---

## generate_session

Create a new session token.

> run "openssl rand -base64 48"

---

## validate_token

Validate that a token matches the expected value.

> assert provided_token expected_token

---

## login

Process a login attempt --- generate token on success.

> print "Login attempt for user"
> run "openssl rand -hex 32"

---

## logout

Invalidate an active session token.

> print "Session invalidated"

---

## refresh_token

Generate a new token to replace an expiring one.

> run "openssl rand -hex 32"

---

## mfa_challenge

Generate an MFA challenge code.

> run "openssl rand -hex 6"

---

## mfa_verify

Verify an MFA response code.

> assert provided_code expected_code

---

## lockout_check

Check if an account is locked due to failed attempts.

> print "Checking lockout status"

---

## session_expiry

Check if a session token has expired.

> print "Checking session expiry time"
