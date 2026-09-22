# AGENTS.md — TurboKain

Onboarding + operating rules for any AI agent working in this repository.
Read this before touching code.

> **START HERE: `_objective/objective_1.md`** — the mission.
> This file describes *how to work in this repo*. The objective describes
> *what we are hunting and why* (bystander traffic, monuments from extinct
> civilisations, payloads). If a task does not serve Objective 1, say so.
>
> TurboKain is the **alien half** of the same hunt. SetiYeti next door is the
> Python/C truth. TurboKain is the raw-power build: one Kain file per tool,
> native `.exe`, arenas instead of churn, verified lanes instead of drift.
> Same sky, same mission, different instrument.

---

## What TurboKain is

A **Kain-only signal pipeline**. Pure `.kn` → native `.exe`, CPU brute force,
receipts for everything. It re-implements SetiYeti's hot path one tool at a
time behind **byte-identical CLI/CSV contracts**, so the Python/C truth next
door stays the judge until a Kain lane earns its receipt.

Backend Kain exes, scripted by **MarkScript campaign notebooks** (`.md`).
The markdown is the run log: domains scope the night, routines scope the sweep,
blockquotes fire Kain tools, tables carry geometry and RFI masks, fenced blocks
verify inline.

Why not just SetiYeti: it invokes Python-and-slowness vibes — GIL, numpy
fallbacks, pickling, thresholds as comments, pipeline as bash. TurboKain owns
the buffers, owns the lanes, owns the invariants, and proves equivalence. Raw
alien power applied to the same Objective 1.

**Guiding principle:** the same as SetiYeti — *a negative is a result only if
it comes with a noise-matched receipt.* TurboKain just makes the language
enforce it.

---

## What Kain is (so you don't mistake it for a toy)

Kain is a real, shipped systems language — **not** a scripting toy, a DSL, or
a research sketch. It compiles through **LLVM to native `.exe`** (also `.dll`,
`.so`, `.obj`, `.a`), has a full REPL/TUI, and is paranoid by design: **Z3
theorem provers and CBMC formal assertions are integrated throughout the
compiler and runtime** — 500+ Z3 proof packs, 380+ SMT-LIB2 files, 10,000+
CBMC assertions ship with it. The assumption is *all code is fundamentally
broken until mathematically proven otherwise.*

What makes it alien (and useful here) is the **compiler-owned semantic
stack**: 111 keywords, 15+ constructs where the *compiler*, not the programmer,
owns the truth about state, mutation, dispatch, timing, coupling, layout, and
handoff. Plain `fn`/`let` grab the same intuition you'd use in Rust; the point
is to reach for the higher construct when the problem fits.

The decision ladder, top-down (stop at the first rung that fits):

```
L7 systems    actor · collapse/observe/decay · spawn/send/ask
L6 stones     axiom · shatter · teleport
L5 temporal   pulse · resonate
L4 stage      orchestrate
L3 dispatch   converge
L2 integrity  patch · law
L1 authority  world · entangle
L0 plain      fn · struct · let · enum · trait · impl
```

Also real: **Erlang-style actors** (supervision trees, mailbox backpressure),
an **effects lattice** (`Pure`/`IO`/`Async`/`GPU`/`Reactive`/`Unsafe`),
`comptime`, hygienic macros, GPU shaders unified with host code, C `include`,
Python `import`, and `build.kn` as the project authority. Python-like syntax
is camouflage over an inverted machine — **Kain is not Rust; do not write
Rust-with-Kain-syntax.** For TurboKain the constructs that matter most are
`converge` (spec + verified fast lanes), `law` (witnessable invariants),
`world`/`patch` (journals), `orchestrate` (stage graphs), and
`collapse`/`observe`/`decay` over arenas.

## The Kain baseline (learn the language from here)

Agents do not know Kain. It is learned from this repo, never from the compiler
repo:

- `docs/kain/KAIN_BY_EXAMPLE.md` — the tutorial. Read first.
- `docs/kain/training/kain_omni.kn` — one compilable file, all layers L0–L7,
  every effect, stdlib, actors, telemetry. The best teacher in the corpus.
- `docs/kain/examples/sieve-pattern.kn` — the mold every TurboKain exe follows
  (`converge` spec + AVX2 lanes + arena buffers).
- `docs/kain/examples/fusion_chain.kn` — the full causal-chain voice.
- `docs/kain/tsv/` — lookup truth (keywords, decision ladder, converge,
  orchestrate, laws, actors, stdlib, errors). Grep before guessing syntax.

Those are the vendored copies — they live in this repo so you never need to
leave it to write programs. The **full Kain compiler repo** sits *outside this
directory*, one level up, in a sibling folder named `kain/` — reference it as
**`../kain/`** to keep it distinct from this repo's own `kain/` source crate
dir. It is the source of truth for the language, the runtime, the prove corpus,
and the benchmarks. **Read from it if you need more depth; never edit it, never
build it, never treat its files as part of this project.** When referencing it
in docs or code, use the relative path `../kain/` — **do not hardcode a drive
letter** (keep it hermetic; the repo must survive being moved or checked out
anywhere).

## THE_MESSIAH.KN — the ultra file

`docs/kain/THE_MESSIAH.KN` is the language in one artifact: a **raw Kain
amalgamation** packing **6,029 files / 6,029 modules** into a single `.kn` —
**~795,000 lines, ~36 MB**. Every layer, every construct, every stdlib module
and benchmark crate, flattened into one searchable corpus. When the smaller
examples don't answer a question, this does: it is the ground truth for how
Kain is *actually written* at scale, across an ecosystem of real programs —
not toy snippets.

It is the **exemplar** — match its voice. But it is also enormous:

- **Never `read` the whole file.** Grep it, or read slices around a hit.
- It is a reference corpus, **not a dependency and not something to build.**
  Don't try to compile it, don't import it, don't copy it into `kain/`.
- Use it to settle syntax/semantics debates and to find production patterns
  (`converge` lanes, `orchestrate` graphs, actor fanout, arena ownership) that
  the smaller examples only sketch.
- It sits with the vendored baseline on purpose: agents learn from **programs**,
  never from the compiler repo.

```bash
grep -n "converge " docs/kain/THE_MESSIAH.KN | head        # find lane patterns
grep -n "actor " docs/kain/THE_MESSIAH.KN | head
```

---

## CLI commands (the ones that matter)

Full list: `docs/kain/tsv/cli_commands.tsv`. For TurboKain, this is the
whole useful surface:

```bash
kain check kain/tool.kn                 # typecheck, no artifacts
kain check kain/tool.kn --json          # machine-readable diagnostics

kain build kain/tool.kn --target llvm -o out/tool.exe   # THE build command
kain build kain/tool.kn --emit staticlib                # -> .lib / .a
kain build kain/tool.kn --emit sharedlib                # -> .dll / .so
kain build kain/tool.kn --emit object                   # -> .obj / .o

kain run kain/tool.kn --target llvm -- --flag arg   # compile + run, pass argv
kain run dev kain/tool.kn               # watch + re-run on change

kain test kain/ --json                  # run compiletest-directive tests
kain fmt kain/ --check                  # formatting check (--write to fix)
kain clean --scope build               # drop build artifacts
kain doctor                            # environment / wiring diagnostics
kain repl                              # TUI: edit + compile to LLVM live
kain amalgamate kain/ -o out.kn         # pack a crate into one capsule
kain init my-crate                     # scaffold a new crate
```

`--target llvm` is the default path for TurboKain — native CPU exes, no GPU.
Remember: **`kain build` is the gate**; `kain check` cannot verify `converge`
over `ptr` params.

## Where the stdlib is

The standard library lives in the **sibling Kain repo** at `../kain/stdlib/`
(directory name only — no drive letter). It is **71 `.kn` modules**, each pure
Kain source we can read. The ones TurboKain touches: `alloc`, `memory`, `fs`,
`io`, `math`, `collections`, `runtime` (the `runtime_simd_*` AVX2/AVX512
intrinsics), `process`, `actor`, `atomic`, `hash`, `json`, `fmt`, `bytes`,
`machine`, `time`, `random`.

Signature lookup without reading source: **`docs/kain/tsv/stdlib.tsv`**
(`module · symbol · kind · signature · purpose`) — grep it before guessing a
function. Prefer stdlib over hand-rolled kernels; the intrinsics are the
proven fast lane.

## Pipeline

```
.kn source  ──►  kain build --target llvm  ──►  .exe  ──►  receipts
                                                              │
                        markscript/*.md  (campaigns, IVT dispatch)
```

One file per tool, same argv, same CSV columns as the SetiYeti tool it
shadows. The C/numpy version stays as the `spec` lane's oracle until the prove
harness says the Kain lane matches.

---

## Where the data is

The bulk raw firehose lives on **`D:/data/`** — an external ~1 TB tier
**outside this repo**, gitignored by definition. As of now it holds roughly
**492 GB**: **93 GUPPI `.raw` files in `D:/data/raw/`** (about 17 GB each),
plus `D:/data/gc/` (7.6 GB), `D:/data/gt.bin` (7.9 GB), derived/slice tiers,
and `D:/data/runs/` campaign output. There is a **metric fuck ton** of raw
data there — this is the archive, not a sample.

```
D:/data/
  raw/       GUPPI .raw files as downloaded (~476 GB, 93 files)
  slices/    per-channel .f32 extractions (seti_slice output)
  derived/   .npz / .npy / .csv intermediates
  runs/      campaign + scan output
  gc/  tmp/  aria logs, manifests, misc bulk
```

Rules: **never hardcode `D:/` in committed code** — take `--data-dir` /
`$SETIYETI_DATA` so the repo still runs when the drive is unplugged. Never
commit raw data. Check `D:/data/download_manifest.csv` and the SetiYeti
`catalog.tsv` before downloading or rescanning anything — most files are
already accounted for. Raw downloads land on `D:/data/`; only the current
working set lives beside the code.

## Downloading — permitted, encouraged, and fast

This box is a **VPS with ~5000 Mbps (5 Gbps) download**. Bandwidth is not a
constraint here — **agents are cleared to download whatever the search needs,
whenever they need it**, straight into `D:/data/`. Do not ask first for data;
do ask before anything destructive. Pull the whole scan. Pull the cadence OFF
leg. Pull the other polarisations. Pull the deeper coverage. Dwell time is
sensitivity, and we have the pipe to buy it.

Use the SetiYeti tooling (public BL archive, **no AWS credentials needed**):

```bash
# what targets exist
python python/bl_download.py targets --grep <NAME>

# files for a target + direct URLs
python python/bl_download.py query --target <NAME> --file-types 'baseband data' --limit 50

# download (aria2c -x16 for full speed; single conn is throttled ~4 MB/s,
# multi-conn gets ~90 MB/s server-side — the 5 Gbps cap is not the limit)
python python/bl_download.py get --target <NAME> --file-types 'baseband data' \
    --limit 4 --outdir D:/data/raw --jobs 3 --conns 16
```

- `https://seti.berkeley.edu/opendata/api/...` — target + file listing (`list-targets`, `query-files`).
- `http://blpd0.ssl.berkeley.edu/<dir>/<file>.raw` — bulk raw mirror (supports HTTP Range).
- `https://storage.googleapis.com/gbt_guppi/` — fast, but only a few targets.

Preflight cheap with **Range GETs**: pull 64 KB, check `PROJID` / `NBITS` /
byte entropy / payload liveness *before* paying for 17 GB. Record new pulls in
`D:/data/download_manifest.csv` and update SetiYeti's `catalog.tsv` — a
download is not done until the ledger says so.

## Repo layout

```
kain/        backend exes — every folder is its own crate with its own build.txt
             (`kain/_examples/` holds working sample tools)
markscript/  campaign notebooks (.md) + the markscript runtime
reports/     receipts, hits, evidence — machine-checkable outputs only
_tmp/        scratch, gitignored, nothing load-bearing
docs/        spec.md + the vendored Kain baseline under docs/kain/
_objective/  the mission (objective_1.md)
AGENTS.md    this file
```

---

## Build & run

```bash
# Build one tool to native
kain build kain/<tool>.kn --target llvm -o out/<tool>.exe

# Check (parse + types; cannot verify ptr lanes — see rules)
kain check kain/<tool>.kn

# Run
out/<tool>.exe <args...>
```

No Bazel in this repo. No Python in the hot path. The Kain toolchain lives
outside this repo (warm) — `kain` is on PATH.

---

## Non-negotiable rules

1. **You write programs in Kain, never work on the Kain compiler.** The
   toolchain is external and warm. If code fails, assume your program is wrong
   first. Blame the compiler only with a minimal repro + receipt. Never edit
   the toolchain, never propose new keywords unless asked.
2. **Prove before replace.** A Kain lane promotes to runner only when it
   matches the C/numpy truth on the prove harness. Report the floor.
3. **Thresholds are data, not magic numbers.** No new hardcoded constants.
   Geometry comes from argv or campaign files; if a value must freeze, it goes
   in config with a comment saying why.
4. **Every detection emits a receipt. No receipt, didn't happen.** A `BLOCK`
   is a claim we can be audited on — name the rule, the margin, the mechanism.
5. **The veto stays human-fed, never replaced.** Kain feeds it; it never
   decides dispositions.
6. **`build` is the gate for exes.** `kain check` cannot verify `converge` over
   `ptr` params (verify can't synthesize pointers) — equivalence receipts live
   in `main()` exit codes.
7. **`and`/`or` don't short-circuit.** Guard argv with nested `if`s, never
   `len(args) > 0 and args[0]...` — that crashes on empty argv.
8. **No hardcoded paths or drive letters** in committed code. Take `--data-dir`
   / `$SETIYETI_DATA` style flags.
9. **Never hide a flag.** Re-score it, quarantine it, name it — don't drop it.
10. **Don't overclaim.** "No candidates, here is the floor, here is the
    coverage" is a successful shift. Inflated enthusiasm is not.

---

## Common pitfalls (bled for — do not rediscover)

- `converge` over `ptr` params can never pass `check`; go through `build`.
- `use std::collections` is required for `int_max`; `std::io` was missing it.
- String interpolation `"{var}"` prints literally in some paths — use
  concatenation/`str()` when in doubt.
- Actors are for **coarse fanout** (channels × blocks × pols), never per-sample
  or per-bin. Tight math belongs in `shatter`/`collapse`/`observe`/`decay`
  buffers, single-threaded.
- GPU/shader/UI paths are out of scope for Objective 1 on this box. CPU lanes
  (`capability("cpu.x86.avx2")`) are the fast path.

---

## Status

Baseline scaffolded. No TurboKain exes yet. SetiYeti remains the truth. First
targets, in order: boxcar/fold sieve → power sieve → evidence journal → the
MarkScript campaign layer. See `docs/spec.md`.

---

## What "found something" looks like

Same language as SetiYeti (`INTERSTELLAR_HIT_CRITERIA.md`): structure where
thermal noise cannot produce it. Kain's role is to make that structure cheap to
express and hard to fool yourself about — `converge` (verified lanes), `law`
(witnessable gates), `world`/`patch` (journals). The veto, cadence gate, and
I0–I5 grades do not move. Single files cap at I2; cadence gates CANDIDATE.

---

## Critical

Don't just run a pipeline and report that the CSV exists. **Analyze the data
critically and report back** — the weird shit, anything novel, anything worth a
deeper look — and explain what it means on a universal level, assuming the user
is an outsider to the field. The pipeline exists because the user is an
outsider; the agent's job is to be the interpreter and the skeptic, with proof.
