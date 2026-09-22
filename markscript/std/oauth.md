# OAuth

Markscript OAuth 2.0 --- authorization flows, token management.
Dispatches to curl for HTTP requests and openssl for PKCE.

---

## authorize

Start the authorization code flow.

> run "curl -s -X GET 'https://auth.example.com/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=CALLBACK&scope=SCOPE'"

---

## token_exchange

Exchange authorization code for access token.

> run "curl -s -X POST 'https://auth.example.com/token' -d 'grant_type=authorization_code&code=AUTH_CODE&client_id=ID&client_secret=SECRET&redirect_uri=CALLBACK'"

---

## refresh

Refresh an expired access token.

> run "curl -s -X POST 'https://auth.example.com/token' -d 'grant_type=refresh_token&refresh_token=TOKEN&client_id=ID&client_secret=SECRET'"

---

## revoke

Revoke an access or refresh token.

> run "curl -s -X POST 'https://auth.example.com/revoke' -d 'token=TOKEN&client_id=ID&client_secret=SECRET'"

---

## client_credentials

Get a token using client credentials grant.

> run "curl -s -X POST 'https://auth.example.com/token' -d 'grant_type=client_credentials&client_id=ID&client_secret=SECRET'"

---

## pkce_challenge

Generate a PKCE code challenge from a verifier.

> run "echo -n 'CODE_VERIFIER' | openssl dgst -sha256 -binary | base64 | tr -d '=' | tr '+/' '-_'"

---

## implicit_flow

Start the implicit grant flow.

> run "curl -s -X GET 'https://auth.example.com/authorize?response_type=token&client_id=ID&redirect_uri=CALLBACK'"

---

## introspect

Introspect an access token to check validity.

> run "curl -s -X POST 'https://auth.example.com/introspect' -d 'token=TOKEN&client_id=ID&client_secret=SECRET'"

---

## device_flow

Start the device authorization flow.

> run "curl -s -X POST 'https://auth.example.com/device/code' -d 'client_id=ID'"

---

## validate_bearer

Validate a Bearer token by calling the API.

> run "curl -s -H 'Authorization: Bearer TOKEN' https://api.example.com/userinfo"
