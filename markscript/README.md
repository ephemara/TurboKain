# MarkScript - The Prose-Native Scripting Runtime for Kain

> **Your documentation is your program. Your README IS the executable.**

MarkScript is a **markdown-native bytecode VM** that serves as Kain's companion language for configuration, orchestration, UI scripting, build systems, and executable documentation. It compiles through Kain's LLVM backend to native code - a standalone `.exe` with zero runtime dependencies beyond the Kain native runtime.

**Core property:** Markdown has no syntax errors. Every `#`, `>`, `|`, and `` ``` `` is valid. The only errors are *runtime* errors - name not found, arity mismatch, bounds violation, import failure.

```
mks run README.md                  → 625 bytecode ops, 21 data tables → EXECUTED
mks run examples/pong.md           → 8 domains, 24 routines, 9 tables → EXECUTED
mks run examples/fizzbuzz.md       → 23 VM opcodes, full FizzBuzz     → EXECUTED
mks build Cargo.toml               → auto-detects Rust → cargo build  → EXECUTED
mks pipe < build.md                → stdin → markscript → stdout      → EXECUTED
```

**This README is a valid MarkScript program.** Running `mks run README.md` compiles itself -- the headings are domains, sections are routines, tables are data matrices, and code blocks are extracted.

---

## Quick Start

```bash
# Build the MarkScript runtime (requires Kain toolchain)
cd blades/markscript
kain build

# Run a markdown script
mks run examples/game_engine.md

# Build any project from prose
mks build Cargo.toml          # auto-detects Rust → cargo build
mks build CMakeLists.txt      # auto-detects C → cmake + make
mks build build.md            # runs a markscript build definition

# Validate a script without executing
mks check examples/data_pipeline.md --json

# Disassemble bytecode
mks disasm examples/servo_controller.md

# Watch a file and re-execute on change
mks watch build.md

# Use as a Unix filter
echo '> print "hello"' | mks pipe
```

### Prerequisites

- **Kain toolchain** (`kain build`, `kain check`)
- **Native runtime** -- auto-linked during `kain build`
- **Windows, Linux, or WSL** -- targets x86_64

---

## What's New in 2.0

MarkScript 2.0 is the result of a four-lane parallel strike hardening every subsystem. Key upgrades:

| Area | 1.0 | 2.0 |
|------|-----|-----|
| **VM Opcodes** | 20 | 23 (for-loops, fn calls, return) |
| **IVT Handlers** | 12 | 78 (stdlib, process lifecycle, UI events) |
| **CLI Subcommands** | 8 | 13 (pipe, watch, build, test, clean) |
| **Test Coverage** | 22 cases | 114 cases + 6 Z3 proofs + 17 benchmarks |
| **Embedding** | Manual API | `std::markscript` module + UI event bridge |
| **Config** | Tables only | Schema validation, code generation, layered merge |

Full details: [`CHANGELOG.md`](CHANGELOG.md)

---

## CLI Reference

### Subcommands

| Subcommand | Usage | Description |
|-----------|-------|-------------|
| `run` | `mks run <file.md>` | Compile and execute (default subcommand) |
| `check` | `mks check <file.md>` | Compile-only validation, no VM execution |
| `disasm` | `mks disasm <file.md>` | Dump bytecode opcodes and exit |
| `repl` | `mks repl` | Interactive REPL - type intents, see results |
| `eval` | `mks eval '<intent>'` | One-shot intent compilation and dispatch |
| `init` | `mks init <name>` | Scaffold a new markscript project directory |
| `handlers` | `mks handlers` | List all registered IVT handlers |
| `doc` | `mks doc <file.md>` | Render clean documentation (strip VM output) |
| `pipe` | `stdin \| mks pipe` | Read stdin, execute as markscript, write stdout |
| `watch` | `mks watch <file.md>` | Poll file mtime every 500ms, re-execute on change |
| `build` | `mks build [target]` | Auto-detect + build Rust/C/C++/Node/Python/Go/Kain |
| `test` | `mks test [target]` | Auto-detect + run tests for any project |
| `clean` | `mks clean [target]` | Auto-detect + clean artifacts |

### Flags

| Flag | Description |
|------|-------------|
| `-h, --help` | Show full usage text and exit |
| `-v, --version` | Print version string and exit |
| `-q, --quiet` | Suppress runtime logging and telemetry |
| `--json` | Output structured JSON (all subcommands) |

### Build Auto-Detection

`mks build` auto-detects project type and delegates to the correct tool:

| File Found | Build Command |
|-----------|---------------|
| `Cargo.toml` | `cargo build` |
| `CMakeLists.txt` | `cmake -B build && cmake --build build` |
| `package.json` | `npm run build` |
| `*.kn` / `build.kn` | `kain build` |
| `pyproject.toml` | `pip install -e .` |
| `Makefile` | `make` |
| `go.mod` | `go build` |
| `build.md` / `Mksfile.md` | `mks run` (markscript build pipeline) |

---

## Writing MarkScript -- Language Reference

### Domains - `# Title`

A top-level heading creates a **domain** - a named scope for routines and data.

```markdown
# PhysicsSim
# DataPipeline
# GameConfig
```

Compiles to: `OP_ENTER_DOMAIN hash("PhysicsSim")`

### Routines -- `## Subtitle`

A second-level heading creates a **routine** - a named executable block.

```markdown
## ComputeForces
## physics_tick
## render_frame
```

Compiles to: `OP_ROUTINE_HEADER hash("ComputeForces")`

### Intents -- `> phrase`

A blockquote is an **intent** -- a natural language command dispatched through the Intent Vector Table (IVT).

```markdown
> apply gravity
> compute pathfinding
> present swapchain
```

Compiles to:
```
OP_PUSH_PARAM hash("apply gravity")
OP_EXECUTE_CALL
```

The IVT maps phrase hashes to handler IDs at runtime. **81 built-in handlers** bridge to the Kain stdlib -- filesystem, process management, math, string operations, JSON, networking, time, regex, templates, random, and UI events. See [`docs/IVT_AND_HANDLERS.md`](docs/IVT_AND_HANDLERS.md) for the full registry.

### Data-Driven Intent Keyword Registry

Intent keywords are **data-driven** -- the single source of truth is [`std/intents.md`](std/intents.md), a markdown table with 57 single-word intent keywords. The module `src/registry.kn` reads this file at startup and populates an `IntentRegistry` world. The parser calls `is_keyword()` from this world instead of a hardcoded list.

**To add a new intent keyword:** edit `std/intents.md`, add a row to the table, register the handler in `bridge.kn`. No parser or compiler changes needed.

#### Three-Way Blockquote Classification

The parser classifies every blockquote (`> text`) into one of three categories:

| Category | Detection | Action |
|----------|-----------|--------|
| **Known intent keyword** | First word in `std/intents.md` registry | Emit `OP_PUSH_PARAM` + `OP_EXECUTE_CALL` |
| **Prose documentation** | First word in 57-word `PROSE_STARTERS` list (articles, prepositions, pronouns, conjunctions, interrogatives) | Skip -- no bytecode emitted |
| **Unknown word** | Not in registry, not a prose-starter | Skip --- treated as prose (fallback) |

This means standard markdown blockquotes like `> This is documentation` never trigger intent dispatch, while `> print "hello"` always will.

#### Intent Keyword Categories (57 keywords)

| Category | Count | Examples |
|----------|-------|----------|
| **File I/O** | 7 | `read`, `write`, `exists`, `mkdir`, `readdir`, `stat`, `touch`, `chmod` |
| **String** | 9 | `concat`, `split`, `join`, `substr`, `replace`, `upper`, `lower`, `trim`, `contains` |
| **Math** | 8 | `sin`, `cos`, `sqrt`, `abs`, `min`, `max`, `clamp`, `random` |
| **Random** | 4 | `randint`, `randfloat`, `randrange`, `randfrange`, `maybe`, `diceroll` |
| **JSON** | 2 | `parse`, `stringify` |
| **Time** | 2 | `time`, `sleep` |
| **Process** | 8 | `run`, `spawn`, `await`, `kill`, `exitcode`, `stdout`, `stderr`, `pipe`, `env`, `cwd` |
| **UI** | 4 | `click`, `key`, `focus`, `close`, `find`, `set`, `get`, `create` |
| **Template** | 1 | `template` |
| **Core** | 3 | `print`, `assert`, `import` |

### Process Lifecycle

```markdown
> spawn "cargo build"       # start + track PID
> await 0                    # wait for process[0]
> exitcode 0                 # push exit code
> assert 0                   # verify success

> env RUST_BACKTRACE=1 run "cargo test"

> pipe "cat data.txt" | "grep ERROR"
```

### UI Scripting

```markdown
> create widget button "submit"
> set widget "submit" "text" "Click Me"
> find widget "input.hex"
> get widget "input.hex" "text"
```

### Data Tables --- `| col1 | col2 |`

A markdown table is a **matrix** --- parsed into a contiguous `Array<Int>` stored in the VM's data table. Tables support schema validation via `@schema`.

```markdown
@schema "schemas/server_schema.md"

| Host | Port | Workers | TLS |
|------|------|---------|-----|
| 0.0.0.0 | 8080 | 4 | false |
```

Compiles to:
```
OP_PUSH_MATRIX handle=0 cols=4 rows=1 data_count=4
```

**Properties:**
- Separator rows (`|---|`) are detected and skipped
- The row before the separator is the header (column names)
- Values are stored contiguous in bytecode --- zero copy, zero indirection
- Tables are accessible at runtime by handle ID via `mks_table_get_*()`
- Schema validation catches type errors, missing required fields, and constraint violations

### Config → Code Generation

```bash
mks gen config.md --target json       # → config.json
mks gen config.md --target toml       # → config.toml
mks gen config.md --target env        # → .env
mks gen config.md --target kain       # → Kain struct + loader
mks gen config.md --target typescript # → TypeScript interface
```

### The Markscript Mini-Language (Inside ` ```markscript ` Blocks)

Within ` ```markscript ` fenced blocks, you can write imperative code:

```markscript
let n = 1
while n <= 100:
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    n = n + 1
```

Supports: variables, `while`/`for` loops, `if/elif/else`, arithmetic (`+`, `-`, `*`, `/`, `%`), `print()`, `str()`, `len()`, array literals `[1, 2, 3]`, dict literals `{key: value}`, function definitions `fn name():`, `return`.

### `@import` --- Multi-File Composition

The `@import` directive merges external markdown files at compile time. Paths resolve relative to the importing file, imported domains and routines merge into the calling namespace, and circular imports are detected at compile time (max depth: 16).

Imports are resolved at compile-time, before bytecode emission. Rules:
- Paths resolve relative to the importing file
- Imported domains and routines merge into the calling namespace
- Duplicate domain names: last import wins (warning emitted)
- Circular imports: hard error at compile time
- Max depth: 16

---

## Architecture

### Pipeline

```
.md source
    │
    ▼ ┌───────────────────────────┐
    │  LEXER (lexer.kn)           │
    │  22 token types - headings, │
    │  blockquotes, tables, fences│
    └──────────┬──────────────────┘
               │ tokens
               ▼
    ┌─────────────────────────────────┐
    │ INTENT REGISTRY (registry.kn)   │
    │ Reads std/intents.md →           │
    │ IntentRegistry world             │
    │ is_keyword() lookup for parser   │
    └────────────┬────────────────────┘
                 │ keyword set
                 ▼
    ┌───────────────────────────────┐
    │ PARSER + COMPILER (parser.kn) │
    │ Single-pass: tokens→bytecode  │
    │ • Tables → OP_PUSH_MATRIX     │
    │ • Intents → OP_PUSH_PARAM +   │
    │              OP_EXECUTE_CALL   │
    │ • Prose/intent disambiguation │
    │ • @import resolution          │
    │ • Mini-language → VM opcodes  │
    └──────────┬────────────────────┘
               │ bytecode (Array<Int>)
               ▼
    ┌──────────────────────────────┐
    │ VIRTUAL MACHINE (vm.kn)      │
    │ 23 opcodes, stack-based      │
    │ IVT dispatch for intents     │
    │ Data table, call stack, vars │
    │ Processes, widgets, arrays   │
    │ JMP/JZ/JN for control flow   │
    └──────────┬───────────────────┘
               │ ExecResult
               ▼
    ┌──────────────────────────────┐
    │ HANDLER DISPATCH             │
    │ bridge.kn (78 handlers)      │
    │ bridge_stdlib.kn (stdlib)    │
    │ Core, BETA, GAMMA, DELTA     │
    └──────────────────────────────┘
```

### Source Map

| File | LOC | Role |
|------|-----|------|
| `src/lexer.kn` | ~350 | Tokenizer -- 22 token types, value semantics |
| `src/registry.kn` | ~250 | Data-driven intent keyword loader from std/intents.md |
| `src/parser.kn` | ~500 | Single-pass bytecode compiler, @import, prose/intent disambiguation, mini-language |
| `src/vm.kn` | ~847 | Virtual Machine - 23 opcodes, stack, IVT, processes, widgets, arrays |
| `src/main.kn` | ~1,406 | CLI driver, 13 subcommands, --json, auto-discovery |
| `src/cli.kn` | ~664 | Argument parser, build auto-detection, JSON output |
| `src/bridge.kn` | ~1,331 | IVT handler registry - 78 handlers, dispatch, registration |
| `src/bridge_stdlib.kn` | ~414 | BETA: 35 stdlib handler functions across 10 domains |
| `src/types.kn` | ~436 | MarkValue (10 kinds), MatrixRecord, ProcessRecord, WidgetRecord |
| `src/error.kn` | ~150 | MarkError (6 kinds), formatting, did-you-mean |
| `src/import.kn` | ~220 | @import resolution, cycle detection |
| `src/jit.kn` | ~670 | x86-64 JIT compiler for all opcodes |
| `src/std_markscript.kn` | ~321 | Clean embedding API for Kain programs |
| `src/markscript_ui.kn` | ~295 | UI event binding bridge |
| `src/schema.kn` | ~345 | Config schema validation |
| `src/gen.kn` | ~524 | Config → code generator (json/toml/env/kain/typescript) |
| `src/config.kn` | ~409 | Layered config merging |
| **Total** | **~7,500** | |

### Handler Registry

| Range | Count | Owner | Category |
|-------|-------|-------|----------|
| 1-12 | 12 | Core | Filesystem, process, assert, print, str, len, push, pop |
| 13-50 | 38 | BETA | Stdlib: string, math, json, fs, process, time, net, regex, template, random |
| 51-59 | 9 | GAMMA | Process lifecycle: spawn tracked, await, kill, pipe, env, cwd |
| 71-78 | 8 | DELTA | UI scripting: click, key, focus, close, find widget, get/set property, create widget |
| **Total** | **78** | | |

---

## Embedding MarkScript in Kain

Any Kain program can embed the MarkScript VM via `std::markscript`:

```kain
use std::markscript

let vm = markscript.mks_new_vm()
let vm = markscript.mks_run_file("config.md")

// Access parsed tables as typed data
let host = markscript.mks_table_get_string(vm, 0, 0, 0)  // "0.0.0.0"
let port = markscript.mks_table_get_int(vm, 0, 0, 1)     // 8080

// Iterate all tables
let tables = markscript.mks_tables(vm)
```

For UI apps, use `std::markscript_ui` to bind markscript intents to widget events:

```kain
use std::markscript_ui

let session = markscript_ui.mks_ui_create_from_file("ui.md")
// ui.md tables define window, layout, presets, event bindings
// Changing the UI means editing ui.md -- not the Kain code
markscript_ui.mks_ui_run(session)
```

See `mks/ui.md` + `mks/src/main.kn` for a working hex color mixer that loads its entire UI spec from markscript tables at runtime.

---

## Project Structure

```
markscript/
├── README.md                  ← this file (self-executing docs)
├── CHANGELOG.md               ← full version history (self-validating)
├── MARKSCRIPT.MD              ← canonical specification & contract
├── build.kn                   ← Kain project authority
├── docs/                      ← authoring guides
│   ├── GETTING_STARTED.md
│   ├── AUTHORING_GUIDE.md
│   ├── CLI_REFERENCE.md
│   ├── IVT_AND_HANDLERS.md
│   ├── POSSIBILITIES.md
│   ├── JIT_DESIGN.md
│   └── TEST_MATRIX.md         ← complete opcode/error/handler coverage
├── src/                       ← Kain source (the VM implementation)
│   ├── main.kn                - CLI (13 subcommands), handler loop, --json
│   ├── cli.kn                 - argument parser, auto-detection, MksConfig
│   ├── lexer.kn               --- 22-token tokenizer
│   ├── registry.kn            --- data-driven intent keyword loader (std/intents.md)
│   ├── parser.kn              --- single-pass bytecode compiler, prose/intent disambiguation
│   ├── vm.kn                  - 23-opcode stack VM, IVT, state management
│   ├── types.kn               --- MarkValue (10 kinds), MatrixRecord, WidgetRecord
│   ├── bridge.kn              -- 81-handler IVT registry + dispatch
│   ├── bridge_stdlib.kn       - BETA: 35 stdlib handler functions
│   ├── error.kn               - runtime error formatting, did-you-mean
│   ├── import.kn              --- @import resolution
│   ├── jit.kn                 -- x86-64 JIT compiler
│   ├── std_markscript.kn      --- clean embedding API for Kain programs
│   ├── markscript_ui.kn       --- UI event binding bridge
│   ├── schema.kn              - config schema validation
│   ├── gen.kn                 - config → code generator
│   └── config.kn              --- layered config merging
├── std/                       ← Markscript stdlib (93 markdown files)
│   ├── build.md               - canonical build definition format
│   ├── process.md             - full process lifecycle intents
│   ├── math.md, string.md, fs.md, time.md, json.md
│   ├── git.md, docker.md, k8s.md, ci.md
│   └── ... (93 total, 10 wired to real IVT handlers)
├── test/                      ← Test suite (114 cases)
│   ├── e2e_pipeline.kn        - 22-case end-to-end pipeline test
│   ├── edge_cases.kn          --- 20 boundary/error cases
│   ├── bridge_handlers.kn     - 16 handler dispatch tests
│   ├── combinatorial_matrix.kn --- 39 combinatorial coverage tests
│   ├── test_runner.kn         - unified test runner with filtering
│   ├── jit_*.kn               -- JIT integration tests
│   └── test_lexer.kn, test_markscript_parser.kn
├── z3/                        ← Z3 proof packs (6 files)
│   ├── vm_invariants.z3       - stack + arithmetic safety
│   ├── var_store_integrity.z3 --- variable store correctness
│   └── call_stack_integrity.z3 - call/ret pairing
├── benchmarks/                ← Benchmark suite (17 benchmarks)
├── attrition/                 ← Sabotage definitions (20 cases)
├── examples/                  ← executable example scripts
│   ├── verified/              ★ Verified examples (all pass mks run)
│   │   ├── intent_registry_demo.md    --- 57-keyword registry + prose disambiguation
│   │   ├── full_stdlib_exercise.md    --- all 8 intent categories
│   │   ├── markscript_mini_language_demo.md - mini-language: vars, if/else, functions
│   │   ├── table_parser_demo.md       --- pipe tables with type inference
│   │   ├── import_directive_demo.md   - @import resolution
│   │   └── prose_vs_intent_demo.md    -- 3-way classification with 50+ prose-starters
│   ├── pong.md                --- complete Pong game (8 domains, 24 routines, 9 tables)
│   ├── fizzbuzz.md            --- mini-language: loops, if/else, vars
│   ├── game_engine.md         --- physics/AI/rendering loop
│   └── ... (25+ total)
├── mks/                       ← Hex color mixer (markscript-driven Kain UI)
│   ├── ui.md                  --- UI spec in markscript tables
│   ├── readme.md              -- markscript build orchestrator
│   └── src/                   -- Kain UI implementation (loads ui.md at runtime)
└── schemas/                   ← Config schema definitions
```

---

## What MarkScript Is NOT

| Not This | Because |
|----------|---------|
| A general-purpose language | That's Kain. MarkScript orchestrates Kain |
| A replacement for Kain | No type system, memory model, ownership, or effects |
| A compiler platform | Cannot express generics or code generation (but can dispatch TO Kain's compiler) |
| A package manager | Dependency management belongs to Kain |

**What MarkScript IS:**
- ✅ A build system for any language (auto-detects Rust/C/C++/Node/Python/Go/Kain)
- ✅ A config format with schema validation and code generation
- ✅ A UI scripting engine embeddable in Kain apps
- ✅ A CI/CD pipeline definition language
- ✅ A process orchestrator with full lifecycle management
- ✅ Executable documentation - your README is your test suite

---

## Further Reading

- **`CHANGELOG.md`** --- Full version history (self-validating markscript)
- **`MARKSCRIPT.MD`** --- Canonical specification, invariants, 1.0 contract
- **`docs/GETTING_STARTED.md`** -- Build, run, first script in 2 minutes
- **`docs/AUTHORING_GUIDE.md`** - Complete markdown→semantics mapping
- **`docs/CLI_REFERENCE.md`** -- Full subcommand and flag reference
- **`docs/IVT_AND_HANDLERS.md`** -- The 78-handler intent dispatch system
- **`docs/POSSIBILITIES.md`** - What you can build with MarkScript
- **`docs/JIT_DESIGN.md`** --- x86-64 JIT architecture
- **`docs/TEST_MATRIX.md`** --- Complete coverage documentation

---

*Built with [Kain](https://kain-lang.org) -- the non-Von Neumann systems language with a compiler-owned semantic stack.*

*"Your documentation is your program."*
