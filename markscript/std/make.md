# Make

Markscript Make integration -- build system targets, variables, and
workflow commands through shell dispatch.

---

## build

Build the default target.

> run "make"

```markscript
# Run default target
push("make")
call("run")
```

> run "make build"

```markscript
# Run the 'build' target explicitly
push("make build")
call("run")
```

---

## clean

Remove build artifacts.

> run "make clean"

```markscript
# Clean build outputs
push("make clean")
call("run")
```

---

## test

Run the test target.

> run "make test"

```markscript
# Run tests
push("make test")
call("run")
```

---

## install

Install build artifacts to system paths.

> run "make install"

```markscript
# Install to prefix (default /usr/local)
push("make install")
call("run")
```

> run "make install DESTDIR=./pkg"

```markscript
# Install to a staging directory
push("make install DESTDIR=./pkg")
call("run")
```

---

## all

Build all targets.

> run "make all"

```markscript
# Build everything defined in the Makefile
push("make all")
call("run")
```

---

## targets

List all available targets.

> run "make help"

```markscript
# Show help targets (convention)
push("make help")
call("run")
```

> run "make -qp 2>/dev/null | grep -E '^[a-zA-Z0-9_-]+:' | cut -d: -f1"

```markscript
# Extract target names from Makefile
push("make -qp 2>/dev/null | grep -E '^[a-zA-Z0-9_-]+:' | cut -d: -f1")
call("run")
```

---

## variables

Override Makefile variables at invocation.

> run "make build CC=clang CFLAGS="-O2 -march=native""

```markscript
# Build with custom compiler and flags
push("make build CC=clang CFLAGS=\"-O2 -march=native\"")
call("run")
```

> run "make build JOBS=8"

```markscript
# Override parallelism variable
push("make build JOBS=8")
call("run")
```
