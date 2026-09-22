# ProjectBuild

Canonical build definition format for MarkScript projects.
Adopted by `mks build`, `mks test`, and `mks clean`.
This markdown IS the build script -- compiled and executed by the MarkScript VM.

---

@schema "schemas/build_schema.md"

## Metadata
| Property | Value |
|----------|-------|
| Name | my-project |
| Language | rust |
| BuildTool | cargo |
| Version | 0.1.0 |

## Stages
| Stage | Command | DependsOn | TimeoutSec |
|-------|---------|-----------|------------|
| clean | cargo clean | -- | 30 |
| check | cargo check | - | 60 |
| build | cargo build | check | 120 |
| test | cargo test | build | 180 |
| bench | cargo bench | build | 300 |
| lint | cargo clippy | check | 60 |
| fmt | cargo fmt --check | - | 30 |
| doc | cargo doc | build | 60 |
| package | cargo package | test | 120 |

## Build

> print "=== BUILD: "ProjectBuild" ==="

> run "cargo build"

> print "Build complete"

## Test

> print "=== TEST: "ProjectBuild" ==="

> run "cargo test"

> print "Tests complete"

## Clean

> print "=== CLEAN: "ProjectBuild" ==="

> run "cargo clean"

> print "Clean complete"

## Check

> print "=== CHECK: "ProjectBuild" ==="

> run "cargo check"

> print "Check complete"

---

## How to use

```bash
# Run the full build pipeline
mks run build.md

# Or use the dedicated subcommands (auto-discover build.md)
mks build                    # → reads Stage: Build → runs cargo build
mks test                     # → reads Stage: Test → runs cargo test
mks clean                    # → reads Stage: Clean → runs cargo clean
```

## Supported Languages

| Language | Build File | Build Command | Test Command | Clean Command |
|----------|-----------|---------------|--------------|---------------|
| Rust | Cargo.toml | cargo build | cargo test | cargo clean |
| C/C++ | CMakeLists.txt | cmake -B build && cmake --build build | ctest | rm -rf build |
| Node | package.json | npm run build | npm test | npm run clean |
| Python | pyproject.toml | pip install -e . | pytest | rm -rf dist |
| Go | go.mod | go build | go test | go clean |
| Kain | build.kn / *.kn | kain build | kain test | rm -rf .kain/out |
| Make | Makefile | make | make test | make clean |
| MarkScript | build.md | mks run build.md | mks test | mks clean |

## Process Lifecycle (GAMMA handlers 51-59)

Track long-running builds with PID tracking:

```markscript
# Spawn a tracked process
> spawn "cargo build"

# Wait for completion
> await 0

# Check exit code
> exitcode 0

# Assert success
> assert 0 0

# Inspect output
> stdout 0

# Inspect errors
> stderr 0

# Kill a stuck build
> kill 0
```
