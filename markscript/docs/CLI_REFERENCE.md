# MarkScript CLI Reference

> Complete reference for the `mks` command-line interface.

---

## Synopsis

```
mks [subcommand] [options] [args]
mks [file.md]                    # shorthand for mks run <file.md>
mks                              # no args → opens REPL
```

---

## Subcommands

### `run` --- Compile and Execute

**Default subcommand.** Compiles a `.md` file to bytecode and executes it through the VM.

```bash
mks run examples/game_engine.md
mks examples/game_engine.md      # equivalent
mks RUN examples/pong.md         # case-sensitive, must be lowercase
```

- Resolves `@import` directives before compilation
- Executes bytecode through 20-opcode stack VM
- Dispatches intents through the IVT handler loop
- Reports execution stats: op count, data tables, code blocks

### `check` --- Compile-Only Validation

Validates a `.md` file without executing it. Faster than `run` for CI and iteration.

```bash
mks check examples/data_pipeline.md
```

- Lexes and compiles to bytecode
- Resolves all `@import` directives
- Detects circular imports, missing files
- Reports bytecode operation count
- Exit code 0 = valid, 2 = error

### `disasm` --- Disassemble Bytecode

Compiles and dumps human-readable bytecode. No VM execution.

```bash
mks disasm examples/servo_controller.md
```

Output:
```
[DISASSEMBLY] 22 ops
  0: OP_ENTER_DOMAIN  operand=372818
  2: OP_ROUTINE_HEADER  operand=183492
  4: OP_PUSH_PARAM  operand=772341
  6: OP_EXECUTE_CALL
  7: OP_PUSH_MATRIX  handle=0  cols=3  rows=2  data_count=6
  ...
```

### `repl` -- Interactive REPL

Starts an interactive MarkScript session.

```bash
mks repl
```

Type intents and markdown. Each line is compiled and executed immediately through the full pipeline. Empty line exits.

### `eval` - One-Shot Intent

Compile and dispatch a single intent string. No file needed.

```bash
mks eval '> print "hello world"'
mks eval '> assert 42 42'
```

Quotes the entire intent to preserve it as one argument.

### `init` -- Scaffold a Project

Creates a new MarkScript project directory structure.

```bash
mks init my-pipeline
```

Creates:
```
my-pipeline/
├── main.md
├── KAIN.toml
└── examples/
```

### `handlers` --- List IVT Handlers

Prints all registered IVT handlers with their hash and ID.

```bash
mks handlers
# → Registered handlers (12):
# →   1: hash=...
# →   2: hash=...
```

### `doc` -- Render Clean Documentation

Renders the source markdown without VM execution artifacts.

```bash
mks doc examples/game_engine.md
```

Outputs: `--- file.md ---` + raw source + `--- end file.md ---`

---

## Flags

| Flag | Description |
|------|-------------|
| `-h, --help` | Show full usage text and exit |
| `-v, --version` | Print version string and exit |
| `-q, --quiet` | Suppress runtime logging and telemetry |
| `--json` | Output structured JSON (future, planned for check output) |
| `--` | Stop flag parsing - everything after is positional |

Flags can appear anywhere before `--`. After `--`, all arguments are positional.

---

## Exit Codes

| Code | Meaning | Typical Cause |
|------|---------|---------------|
| `0` | Success | All good |
| `1` | Info | `--help` or `--version` shown |
| `2` | Error | File not found, parse failure, import error, runtime crash |
| `3` | Unknown | Unrecognized subcommand or flag |

---

## Build Commands (Kain Toolchain)

These build the `mks` binary itself:

```bash
# Full native build (typecheck + LLVM IR + clang link)
kain build

# Typecheck only (fast)
kain check

# Build and sync to ~/.kain/bin/
kain build
kain_sync_binary
```

---

## Environment

No special environment variables needed. `mks` is a standalone native executable. It links against the same Kain native runtime as every other Kain program and accesses `std::fs`, `std::process`, etc. through the runtime.
