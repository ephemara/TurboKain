# MarkScript Test Coverage Matrix

## Overview

This document catalogs complete test coverage across all markscript components.
Last updated: 2026-06-11

## Test Inventory

| # | File | Cases | Status | Categories |
|---|------|-------|--------|------------|
| 1 | `test/edge_cases.kn` | 20 | ✅ COMPILES | Stack bounds (6), Arithmetic edge (5), Variable bounds (4), Jump bounds (3), Call stack (2), Error kinds (4) |
| 2 | `test/bridge_handlers.kn` | 16 | ✅ COMPILES | Registration (4), Dispatch via VM (6), Error propagation (3), Handler chains (3) |
| 3 | `test/combinatorial_matrix.kn` | 39 | ✅ COMPILES | Opcode pairs (14), Opcode triples (10), Variable lifecycle (5), Error cross-products (5), Stress (5) |
| 4 | `test/e2e_pipeline.kn` | 22 | ✅ CHECK | Lexer (6), Parser (5), Pipeline (4), Handlers (4), Errors (3) |
| 5 | `test/test_lexer.kn` | ~7 | ✅ CHECK | All 22 token types, edge cases, real-world |
| 6 | `test/test_markscript_parser.kn` | 8 | ✅ CHECK | Mini-language: let, while, if/else, function calls |

## Opcode Coverage Matrix

| Opcode | Positive Test | Edge Case | Error Path | Test File |
|--------|-------------|-----------|------------|-----------|
| 0 HALT | ✅ | -- | -- | edge_cases |
| 1 ENTER_DOMAIN | ✅ | ❌ | ❌ | e2e_pipeline |
| 2 ROUTINE_HEADER | ✅ | ❌ | ❌ | e2e_pipeline |
| 3 PUSH_PARAM | ✅ | ❌ | ✅ | e2e_pipeline, combinatorial |
| 4 EXECUTE_CALL | ✅ | ❌ | ✅ (NAME) | e2e_pipeline, combinatorial |
| 5 PUSH_MATRIX | ✅ | ❌ | ❌ | e2e_pipeline |
| 6 FENCED_CODE | ✅ | ❌ | ❌ | e2e_pipeline, combinatorial |
| 7 PUSH_STACK | ✅ | ✅ (depth) | ❌ | edge_cases, combinatorial |
| 8 POP_STACK | ✅ | ✅ (empty) | ❌ | edge_cases |
| 9 DUP | ✅ | ✅ (empty) | ❌ | edge_cases, combinatorial |
| 10 CALL | ❌ | ✅ (no handler) | ✅ (NAME) | combinatorial |
| 11 RET | ❌ | ✅ (empty stack) | ❌ | edge_cases |
| 12 JMP | ✅ | ✅ (valid target) | ❌ | edge_cases, combinatorial |
| 13 JZ | ✅ | ✅ (taken/not) | ❌ | edge_cases, combinatorial |
| 14 ADD | ✅ | ✅ (overflow) | ❌ | edge_cases, combinatorial |
| 15 SUB | ✅ | ✅ (underflow) | ❌ | edge_cases, combinatorial |
| 16 MUL | ✅ | ✅ (large) | ❌ | edge_cases, combinatorial |
| 17 DIV | ✅ | ✅ (zero) | ✅ (TYPE) | edge_cases, combinatorial |
| 18 LOAD_VAR | ✅ | ✅ (undefined) | ✅ (NAME) | edge_cases, combinatorial |
| 19 STORE_VAR | ✅ | ✅ (overwrite) | ❌ | edge_cases, combinatorial |
| 20 JN | ✅ | ✅ (taken/not) | ❌ | edge_cases, combinatorial |

### Coverage Gaps Remaining

| Gap | Priority | Notes |
|-----|---------|-------|
| CLI integration tests | Medium | Requires `mks` binary, complex setup |
| JIT fuzz harness | High | Requires `bridge.kn` fix (cross-lane conflict) |
| Import 17-depth error | Low | Requires temp files, `bridge.kn` fixes |
| Process handler tests | Low | Requires `bridge.kn` fixes |
| Benchmark regression | Medium | Separate file needed |

## Error Kind Coverage

| Error Kind | Tested | File |
|-----------|--------|------|
| ERROR_OK (0) | ✅ | edge_cases, combinatorial |
| ERROR_NAME (1) | ✅ | edge_cases, combinatorial |
| ERROR_ARITY (2) | ✅ | edge_cases (constant verification) |
| ERROR_BOUNDS (3) | ✅ | edge_cases (constant verification) |
| ERROR_TYPE (4) | ✅ | edge_cases, combinatorial |
| ERROR_IMPORT (5) | ❌ | Requires import module (std::fs conflict) |
| ERROR_CIRCULAR_IMPORT (6) | ❌ | Requires import module |

## Handler Coverage

| Handler ID | Name | Tests | File |
|-----------|------|-------|------|
| Registration | IVT lookup | ✅ | bridge_handlers |
| Registration | IVT miss | ✅ | bridge_handlers |
| Multiple registrations | - | ✅ | bridge_handlers |
| VM dispatch | EXECUTE_CALL | ✅ | bridge_handlers |

## Token Coverage

| Token Kind | Value | Tested | File |
|-----------|-------|--------|------|
| TOK_HEADER1 | 0 | ✅ | test_lexer |
| TOK_HEADER2 | 1 | ✅ | test_lexer |
| TOK_BLOCKQUOTE | 2 | ✅ | test_lexer |
| TOK_TABLEPIPE | 3 | ✅ | test_lexer |
| TOK_TEXTSTR | 4 | ✅ | test_lexer |
| TOK_EOF | 5 | ✅ | test_lexer |
| TOK_HEADER3-6 | 6-9 | ✅ | test_lexer |
| TOK_FENCE | 10 | ✅ | test_lexer |
| TOK_LANG_TAG | 11 | ❌ | --- |
| TOK_FENCED_CODE | 12 | ❌ | -- |
| TOK_BOLD | 13 | ❌ | --- |
| TOK_ITALIC | 14 | ❌ | --- |
| TOK_CODE_SPAN | 15 | ❌ | --- |
| TOK_LIST_UNORDERED | 16 | ✅ | test_lexer |
| TOK_LIST_ORDERED | 17 | ✅ | test_lexer |
| TOK_LINK_TEXT | 18 | ❌ | - |
| TOK_LINK_URL | 19 | ❌ | --- |
| TOK_HR | 20 | ✅ | test_lexer |
| TOK_NEWLINE | 21 | ✅ | test_lexer |

## Z3 Proof Pack Status

| Invariant | Status | File |
|-----------|--------|------|
| Stack bound safety | 📋 Planned | z3/vm_invariants.z3 |
| Arithmetic overflow safety | 📋 Planned | z3/vm_invariants.z3 |
| Variable store integrity | 📋 Planned | z3/var_store_integrity.z3 |
| Call stack integrity | 📋 Planned | z3/call_stack_integrity.z3 |

## Running Tests

```bash
# Run test catalog
kain run blades/markscript/test/test_runner.kn

# Run individual test suites
kain run blades/markscript/test/edge_cases.kn
kain run blades/markscript/test/bridge_handlers.kn
kain run blades/markscript/test/combinatorial_matrix.kn
kain run blades/markscript/test/e2e_pipeline.kn
kain run blades/markscript/test/test_lexer.kn
kain run blades/markscript/test/test_markscript_parser.kn
```
