# CSRF

Markscript CSRF protection --- token generation, validation, embedding.
Dispatches to openssl for random token generation.

---

## generate_token

Generate a cryptographically random CSRF token.

> run "openssl rand -hex 32"

---

## generate_per_session

Generate a CSRF token tied to the user session.

> run "openssl rand -base64 32"

---

## validate_token

Validate a submitted CSRF token against the expected value.

> assert submitted_token session_token

---

## hidden_field

Generate an HTML hidden input field with CSRF token.

> run "echo '<input type=\"hidden\" name=\"csrf_token\" value=\"'$(openssl rand -hex 32)'\">'"

---

## double_submit_cookie

Generate CSRF token for double-submit cookie pattern.

> run "openssl rand -hex 32"

---

## same_site_check

Check if a cookie has SameSite attribute set.

> print "Verify cookie has SameSite=Strict or SameSite=Lax"

---

## origin_check

Validate the Origin or Referer header matches expected host.

> print "Checking Origin header matches allowed origin"

---

## header_check

Generate token and validate via custom header.

> run "openssl rand -hex 32"

---

## expiry

Generate a CSRF token with a short expiry time.

> run "openssl rand -hex 16"

---

## regenerate

Regenerate CSRF token after privilege escalation.

> run "openssl rand -hex 32"
