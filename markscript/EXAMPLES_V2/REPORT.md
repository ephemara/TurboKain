# EXAMPLES_V2 — Torture Battery Report

**Exe under test:** `mks-windows-x86_64.exe` rebuilt from `markscript.kn`
in THIS repo (post-fix build). **Method:** `run` every file (build, not
check, is the reliable gate — see note), `jit-run` + `jit` where applicable.
Registry (`std/intents.md`) present: without it all intents silently parse
as prose — if nothing fires at all, check the registry first.

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
| 06_jit_brutal (VM) | **SEGFAULT 0xC0000005** | ❌❌ 2 assert fails (F2) then access violation |
| 06_jit_brutal (jit-run) | exit 0, no execution evidence | ❌ Compiles to x86-64, then silence. Asserts that fail under VM should fail here |
| 07_fuzz_corpus | exit 0 | ✅ Unclosed fence, nested quotes, adversarial nesting all survive. No crash, no hang |
| `jit` selftest | all op emitters OK | ✅ JIT backend alive |
| `repl` / `eval` / `pipe` | canned demo / nothing-to-execute / silent | ❌ Stubs. Files (`run`) are the only working execution path |

## Fixed in THIS repo's markscript.kn (verified live)

**Fix A — string table reseed.** `OP_PUSH_STRING_REF` past index 0 rendered
`<invalid`: table intact at exec entry (len 3, verified via instrumented
debug build) but EMPTY on every re-entry — `resume_execution` drops
`string_constants` threading the VM through dispatch. Fix: reload from the
parser world table on every re-entry (one line). Result: fizzbuzz prints
`FizzBuzz`/`Fizz`/`Buzz`, **zero invalids** (was 74).

**Fix B — print all args.** `handler_println` printed `args[0]` only; intent
tokenizers split quoted strings, so multi-word strings could never print
whole. Now space-joins all args. `> print "LEXER TORTURE DONE"` works.

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
