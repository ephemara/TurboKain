# TurboKain — Spec

Kain-only signal pipeline. No Python in the hot path. No GPU required.
Raw systems power: arenas, AVX2 lanes, actors, receipts.

## What it is

TurboKain is the alien half of the search. SETIYETI stays as spec truth
next door. TurboKain re-implements the hot path in pure `.kn` → native
`.exe`, one file per tool, byte-identical CLI/CSV contracts. When a Kain
lane earns its receipt against the C/numpy truth, it becomes the runner.

## Why not just SETIYETI

SETIYETI invokes Python-and-slowness vibes: GIL, numpy fallbacks,
multiprocessing pickling, thresholds as comments, pipeline as bash.
TurboKain invokes brute force: own the buffers, own the lanes, own the
invariants, prove the equivalence. Same sky, different instrument.

## Flow

```
.kn source → kain build --target llvm → .exe → receipts → reports/
                                    ↑
                        markscript campaigns (.md)
```

- `kain/` — backend exes. Every folder is its own crate with its own
  `build.txt`. Kain-only, CPU-only (`x86_64 + AVX2`). Working examples live in
  `kain/_examples/` (e.g. `lane_sieve.kn`, `cadence_pair.kn`).
- `markscript/` — campaign notebooks. Markdown dispatches to backend
  exes through the IVT. The `.md` is the run log.
- `reports/` — receipts, hits, evidence. Machine-checkable outputs only.
- `_tmp/` — scratch, gitignored. Nothing load-bearing lives here.
- `docs/` — this spec + per-crate notes.

## Semantics

Open game. The full language is on the table — every keyword, every
layer, anything that serves the search. No allow-list, no drop-list.
Reach for whatever the problem wants: `converge` lanes, `law` gates,
`world`/`patch` journals, `orchestrate` graphs, `shatter` buffers,
`actors`, `pulse`, `axiom`, GPU dispatch, whatever. If it helps find
signals, it's in bounds.

## New stones (prototype as patterns first, promote to keywords later)

- `baseline` — the noise model as a scoped, revocable fact (L2).
- `quarantine` — a verdict with a receipt, journaled (L2/L4).
- `revisit` — cross-observation recurrence query over the journal (L4/L1).

## Rules

1. Prove before replace. C/numpy stays truth until the Kain lane matches.
2. Thresholds are data, never magic numbers.
3. Every detection emits a receipt. No receipt, didn't happen.
4. Veto stays human. Kain feeds it, never replaces it.
5. `build` is the gate for exes (`check` can't verify `ptr` lanes).
6. No hardcoded paths. Geometry comes from argv / campaign files.
