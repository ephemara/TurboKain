# Cargo

Markscript Cargo integration --- Rust project management, builds, tests,
and tooling through shell dispatch.

---

## build

Compile the project in release or debug mode.

> run "cargo build --release"

```markscript
# Build with optimizations
push("cargo build --release")
call("run")
```

> run "cargo build"

```markscript
# Debug build
push("cargo build")
call("run")
```

---

## run

Build and run the binary.

> run "cargo run -- --port 9090"

```markscript
# Build and run with arguments
push("cargo run -- --port 9090")
call("run")
```

---

## test

Run the test suite.

> run "cargo test"

```markscript
# Run all tests
push("cargo test")
call("run")
```

> run "cargo test -- --nocapture"

```markscript
# Run tests with stdout visible
push("cargo test -- --nocapture")
call("run")
```

---

## check

Check the project for errors without producing artifacts.

> run "cargo check"

```markscript
# Fast compile check only
push("cargo check")
call("run")
```

---

## fmt

Format all Rust source files.

> run "cargo fmt"

```markscript
# Auto-format all source files
push("cargo fmt")
call("run")
```

> run "cargo fmt -- --check"

```markscript
# Check formatting without modifying
push("cargo fmt -- --check")
call("run")
```

---

## clippy

Run Clippy lints on the project.

> run "cargo clippy -- -D warnings"

```markscript
# Run lints and deny warnings
push("cargo clippy -- -D warnings")
call("run")
```

---

## publish

Publish the crate to crates.io.

> run "cargo publish"

```markscript
# Publish current version to crates.io
push("cargo publish")
call("run")
```

---

## update

Update dependencies in Cargo.lock.

> run "cargo update"

```markscript
# Update all deps within semver
push("cargo update")
call("run")
```

> run "cargo update serde"

```markscript
# Update a specific dependency
push("cargo update serde")
call("run")
```

---

## add_dep

Add a dependency to Cargo.toml.

> run "cargo add tokio --features full"

```markscript
# Add tokio with features
push("cargo add tokio --features full")
call("run")
```

> run "cargo add serde --features derive"

```markscript
# Add serde with derive feature
push("cargo add serde --features derive")
call("run")
```
