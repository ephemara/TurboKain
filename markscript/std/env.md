# Environment

Markscript environment variable management - get, set, list, delete, persist
dotenv files. Dispatches through the IVT to Kain's `std::env` bridge and OS
environment block.

---

## get

Retrieve the value of an environment variable by name.

> run "echo %MY_VAR%"

```markscript
# Get an env var by name
push("MY_VAR")
call("env_get")
# Result is the value string, or empty if not set
```

---

## set

Set an environment variable for the current process lifetime.

> run "set MY_VAR=new_value"

```markscript
# Set an env var to a new value
push("MY_VAR")
push("new_value")
call("env_set")
# Result is 1 on success
```

---

## list

List all environment variable names in the current process block.

> run "set"

```markscript
# List all env var names
call("env_list")
# Result is a newline-delimited string of VAR=NAME pairs
```

---

## delete

Remove an environment variable from the current process block.

> run "set MY_VAR="

```markscript
# Unset an environment variable
push("MY_VAR")
call("env_delete")
# Result is 1 if variable was removed, 0 if it didn't exist
```

---

## has

Check whether a specific environment variable is defined.

> run "if defined MY_VAR (echo 1) else (echo 0)"

```markscript
# Check if an env var exists
push("MY_VAR")
call("env_has")
# Result is 1 if defined, 0 if not
```

---

## load_dotenv

Load variables from a `.env` file into the environment. Each line is
`KEY=VALUE`; blank lines and `#` comments are ignored.

> run "for /f %i in (.env) do set %i"

```markscript
# Load dotenv file
push("/path/to/.env")
call("env_load_dotenv")
# Result is count of variables loaded
```

---

## save

Persist the current environment block to a file in KEY=VALUE format.

> run "set > /path/to/env.txt"

```markscript
# Write current env to a file
push("/path/to/env.backup")
call("env_save")
# Result is the number of variables written
```

---

## expand

Expand environment variable references within a string. Replaces `%VAR%`
patterns with their current values.

> run "echo %PATH%"

```markscript
# Expand env var references in a template string
push("Home directory: %HOME%")
call("env_expand")
# Result is the expanded string
```
