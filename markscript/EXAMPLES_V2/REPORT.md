# EXAMPLES_V2 — Torture Battery Report

**Exe under test:** `mks-windows-x86_64.exe` rebuilt from `markscript.kn`
in THIS repo (post-surgery build). **Method:** `run` every file (build,
not check, is the reliable gate). Registry (`std/intents.md`) present.
Asserts are silent on pass — `Handler error` lines are real failures.

> **Corrections to v1 of this report:** early runs lacked the registry, so
> "silent" verdicts were vacuous. Everything below re-ran WITH registry on
> the fixed exe. `02_compute_gauntlet` does NOT pass — its asserts fail
> (F2). Integer math is verified only where in-fence prints show it
> (fizzbuzz loop/numbers).

## Results (fixed exe + registry)

| File | run | Verdict |
|---|---|---|
| 01_lexer_torture | exit 0 | ⚠️ Compiles everything (spec holds: zero syntax errors). fence→intent vars fail asserts (F2). Prints now whole (fix B) |
| 02_compute_gauntlet | exit 0 | ❌ ALL asserts fail (`fa != 832040`…) — F2. Nothing proven about VM math beyond fizzbuzz's loop |
| 03_intent_storm | exit 0 | ⚠️ Value intents run silent by design; prints/asserts evaluated. fs roundtrip created no files (paths CWD-relative — check CWD) |
| 04_matrix_madness | exit 0 | ❌ `matrix_tables != 7` — F2 |
| 05_error_alley | exit 0, graceful | ✅ Unknown intent, arity error, div-zero, assert-fail, import-fail all handled, no crash |
| 06_jit_brutal (VM) | exit 0, asserts evaluate | ⚠️ F2 fails as expected; former segfault GONE on fixed exe — error paths terminate safely |
| 06_jit_brutal (jit-run) | hangs (blocked, ~0 CPU) | ❌ Content-specific: sections/pairs/triples/padded loops all instant; full 436-op file parks. Pre-existing JIT driver issue, needs a native-debug session |
| 07_fuzz_corpus | exit 0 | ✅ Unclosed fence, nested quotes, adversarial nesting all survive. No crash, no hang |
| 08_operators | exit 0, **17/17 correct** | ✅ elif/==/!=/</<=/>/>=/%, while-<= all exact |
| fizzbuzz (full file) | 211 lines: 100 prove + 5 verify + 106 doc-fence | ✅ prove exact 6/27/14/53; verify prints real counts (doc expectations wrong); doc pseudo-fences execute by design |
| `jit` selftest | all op emitters OK | ✅ JIT backend alive |
| `repl` / `eval` / `pipe` | canned demo / nothing-to-execute / silent | ❌ Stubs. Files (`run`) are the only working execution path |

## Fixed in THIS repo's markscript.kn (all verified live)

**Fix A — string table reseed** (v1.0.1). `resume_execution` dropped
`string_constants` threading the VM through dispatch (exec entry saw len 0
 after the first dispatch). Reload from the parser table every re-entry.
Fizzbuzz: 74x `<invalid>` → zero.

**Fix B — print all args** (v1.0.1). `handler_println` printed `args[0]`
only; now space-joins. Multi-word strings print whole.

**Fix C — parser surgery** (this release). Mini-language gains:
`elif` (new MS_TOK_ELIF + branch loop in `ms_parse_if`), `==`/`!=`/
`<=`/`>=` (compound detection in `find_comparison`, JN/JZ lowering,
double-JN gates for `==`), `%` (new OP_MOD opcode: VM exec + disasm
tables + x86 JIT emitter mirrored off DIV + selftest case). Shared
`ms_emit_cond_jumps`/`ms_patch_all` helpers; legacy LT/GT lowering
preserved bit-for-bit. Fizzbuzz now scores exactly 6/27/14/53.

**Fix D — arg decoder hardening.** Leading stack-residue skip (the `"0 "`
prefix), bounds-hardened byte scan, and the `and`-without-short-circuit
OOB in `decode_and_split_args` converted to nested ifs (that one
segfaulted on empty arrays).

**Fix E — `08_operators.md`** regression file: 17 PRINT expectations,
all green.

**Fix F — string `+` concatenation.** `add_values` returned `mark_int(0)`
when either side was a string, so every `"a" + x` printed `0` (the five
verify-section zeros). String arm added: either side MARK_STRING →
concatenate string forms.

**Docs-vs-engine verdict (fizzbuzz).** With branches, modulo, strings,
and concat all working, the engine now audits its own documentation:
the file's claimed counts (14/27/20/39) are wrong — the machine says
6/27/14/53, total 100. Trust the machine. (Also: the `how_it_works`
section contains illustrative pseudo-fences that now EXECUTE — fences
are code, always. Pseudocode belongs in non-markscript fences.)

## Diagnosed, NOT yet fixed (precise mechanisms, repros included)

**F2 — fence→intent variable invisibility.** Vars set in ```markscript
fences read back unset in later `> assert` (`fa != 832040`,
`matrix_tables != 7`, `qq != 42`). In-fence reads work (fizzbuzz loop).
Suspect: assert name-resolution vs STORE_VAR hashing. Repro:
`## r` + fence `let qq = 42` + `> assert qq 42` → fails.

**F3 — `elif` falls through.** The mini-language tokenizer has NO ELIF token
(`MS_TOK_IF/ELSE` exist, ELIF doesn't) and `ms_parse_if` only looks for
`ELSE` — elif lines compile as plain statements, bodies run unconditionally.
Fizzbuzz's 25/25/25/absent split is this bug. Fix needs token + branch
patching in `ms_parse_if` (~15 lines, needs care).

**F4 — top-level `if/else` ignores conditions.** `if cv%2==0` with cv=5
takes the if-branch. Disasm shows the condition compiled to bare
`LOAD cv; JZ` — `find_comparison` doesn't handle `%`-containing LHS, so it
falls back to truthiness of the first operand. Same family as F3 (expression
finder gaps). In-loop conditions behave differently — needs a second look.

**F5 — `"0 "` arg prefix.** `> print hello` → `[PRINT] 0 hello`;
`> print 42` → `[PRINT] 0 42`. A stray count/int leaks from the
count+bytes stack encoding (`run_handler_loop` pops the WHOLE stack as
args, including non-arg temporaries). Quoted multi-word strings decode
clean; bare words don't.

**F6 — segfault after assert failures** (06, `0xC0000005`). Error path
corrupts the dispatch loop. Highest severity here.

**F7 — `jit-run` compiles, never executes.** No output, exit 0, on input
that fails loudly under `run`.

**F8 — `repl`/`eval`/`pipe` stubs** (canned demo / nothing-to-execute /
silent). **F9 — `disasm` vs `run` op counts disagree** (943 vs 414, same
file). **F10 — `kain check` is not the gate**: 482 namespace-collision
errors on input `build` compiles cleanly. Build, don't check.

## Portability note (good news)

No `../std/intents.md` beside the input → exe falls back to 95 embedded
handlers and runs. Registry file is enhancement, not requirement.

---

# OMEGA_ALPHA session (v1.0.3) — the god-file + two engine fixes

**File:** `OMEGA_ALPHA.md` (repo root). One document exercising every
feature: prose-skipping, 9 markscript fences (arithmetic, elif/all-six
comparisons, 3-deep nesting, fib30/collatz/primes/100k-spin/triple loops,
full FizzBuzz 1–100 + self-count, strings, 2 data matrices, kain/python/rust
vault fences, break-me abuse, unknown-intent survival), 11 blockquote
intents, final receipt. **Result: 155 dispatches, 0 failed, 0 FAIL lines,
32 PASS lines, `receipt=PASS`.** FizzBuzz counts exact (27/14/6).

## Fixed in this release (verified live)

**Fix F — dispatch cap 100 → 100000** (`run_handler_loop`, `cmd_pipe`,
`cmd_watch` loops). The old cap cut any file with >100 prints mid-stream
(OMEGA's rite alone spends 100). Safety limit retained, god-files run whole.

**Fix G — `handler_println` now decodes args** via
`decode_count_bytes_args` before space-joining. Killed the cross-dispatch
stack-residue `"0 "` prefix on fence prints (`0 PASS mul`,
`0 OMEGA-ALPHA COMPLETE`) — windowed args shed residue, raw values pass
through untouched. OMEGA output is byte-clean.

**Fix H — quote parity.** The compile-side outer-quote strip inverted
`split_blockquote_string` parity for multi-quoted lines (verified by
tracing: `"A" "B C"` split into 11 fragments). Strip removed; splitter
handles fully-quoted input correctly. `write_region` splices perfectly.

**Fix I — CRLF normalization at ingest.** `read_source` maps CRLF/CR to
LF once, centrally — stray `\r` bytes poisoned tokenizers, splitters,
and sentinels (CRLF vs LF runs diverged). Windows checkouts now behave
identically.

**Fix J — split normalization.** Single-part split results were discarded,
keeping quotes (`"BOOT"` printed with quotes). Always normalize through
the splitter.

**Fix K — string `+` concat (F11).** `add_values` returned `mark_int(0)`
when either side was a string. String arm added; `print("hello" + " " +
"world")` works.

**Fix L — intent result POP.** Intent calls never emitted the `OP_POP_STACK`
that fence calls get, so handler results lingered into the next dispatch
as phantom args. One-line emit fix.

**Fix M — unary minus (F13).** `ms_parse_factor` silently dropped leading
`-`, so `== -2` compared against garbage. `0 - x` lowering added.

## New findings (open)

**F12 — `--section` slices wrong.** `run --section <routine>` reports a
tiny op window (32 ops for a ~200-op routine) and executes only the first
dispatch; `disasm --section` ignores the flag entirely (dumps all ops).
Full runs are the supported path until the slicer remaps jumps.

## Shipped-but-not-mine (pre-existing working-copy WIP, kept as found)

The tree held uncommitted work when this session started: a `write_region`
intent (registry row 81 + full handler + dispatch + exe-dir registry
candidates + loud missing-registry warning + `handlers` name resolution).
Kept, with two leftover `[DBG]` printlns removed. Status as of this
release: **PROMOTED — splice verified perfect** (sentinels preserved,
tail intact, loud errors on missing file/sentinels). The arg-parity bug
it shipped with (outer-quote strip inverting the splitter) is fixed —
see Fix I below. Related caveat: the exe-dir registry candidate can load
a STALE `std/intents.md` that happens to sit beside the binary (seen:
72-row copy shadowing the 73-row repo file). Ship assets alone, not
beside old checkouts.
