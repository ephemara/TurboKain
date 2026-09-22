# MarkScript Examples -- Pushing the Prose-Native Boundary

> These aren't toys. Every example exercises real MarkScript capabilities - opcodes, IVT dispatch, mini-language computation, tables, imports, filesystem I/O, process spawning, and assertion-driven verification.

## The Examples

| Example | Lines | Ops | What It Does |
|---------|-------|-----|-------------|
| **`primality_master.md`** | ~200 | ~250 | Sieve of Eratosthenes, prime factorization, Goldbach verification --- all in markscript mini-language |
| **`iterative_physics.md`** | ~180 | ~200 | 2D particle system with Euler integration, gravity simulation, N-body tables |
| **`pipeline_palooza.md`** | ~150 | ~150 | Multi-stage ETL: ingest → transform → validate → report via all 8 IVT handlers |
| **`collatz_deep_dive.md`** | ~200 | ~300 | Collatz sequences, longest-path search, sequence graphing, conjecture verification |
| **`calculator_suite.md`** | ~150 | ~200 | Expression calculator with self-testing assertion harness |
| **`project_scaffolder.md`** | ~170 | ~150 | Reads metadata from tables, generates project files, tests output --- all through IVT |
| **`chaos_game.md`** | ~180 | ~250 | Barnsley Fern iterated function system --- chaos game computation in markscript |
| **`stress_test.md`** | ~250 | ~500 | Maximum-load stress test: deep nesting, many tables, all opcodes, all handlers |
| **`life_and_rules.md`** | ~200 | ~300 | 1D cellular automata (Rule 30) + Game of Life grid computation |
| **`metacompiler.md`** | ~220 | ~350 | A tiny DSL compiler written in markscript that compiles to markscript bytecode |

## How They Push Limits

| Technique | Examples |
|-----------|----------|
| **Nested while loops** | `primality_master`, `collatz_deep_dive`, `chaos_game`, `life_and_rules` |
| **Deep if/else chains** | `primality_master`, `chaos_game`, `life_and_rules` |
| **Tables as databases** | `iterative_physics`, `project_scaffolder`, `stress_test` |
| **All 8 IVT handlers** | `pipeline_palooza`, `project_scaffolder` |
| **Filesystem I/O** | `pipeline_palooza`, `project_scaffolder` |
| **Process spawning** | `pipeline_palooza`, `project_scaffolder` |
| **Equality workaround pattern** | `primality_master`, `collatz_deep_dive`, `life_and_rules` |
| **Self-verifying tests** | `calculator_suite`, `primality_master` |
| **@import composition** | All multi-file variants planned for imports/ |
| **Lexer/parser limits** | `stress_test`, `metacompiler` |

## Running

```bash
cd blades/markscript

# Build if you haven't already
kain build

# Run any example
mks run examples/primality_master.md
mks run examples/iterative_physics.md
mks run examples/chaos_game.md

# Validate without executing
mks check examples/stress_test.md

# Debug bytecode
mks disasm examples/calculator_suite.md
```
