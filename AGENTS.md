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
>
> **SetiYeti path: `E:/SetiYeti`** ← edit this one line per machine/build if
> it moves. That is the Python/C ground truth, the prove harnesses, and the
> `catalog.tsv` ledger TurboKain shadows.

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

kain build <tool>.kn --target llvm                # THE build command
                                                   # (run from the tool's dir:
                                                   #  exe lands beside source)
kain build <tool>.kn --emit staticlib              # -> .lib / .a
kain build <tool>.kn --emit sharedlib              # -> .dll / .so
kain build <tool>.kn --emit object                 # -> .obj / .o

kain run kain/tool.kn --target llvm -- --flag arg   # compile + run, pass argv
kain run dev kain/tool.kn               # watch + re-run on change

kain test kain/ --json                  # run compiletest-directive tests
kain fmt kain/ --check                  # formatting check (--write to fix)
kain clean --scope build               # drop build artifacts
kain doctor                            # environment / wiring diagnostics
kain repl                              # TUI: edit + compile to LLVM live
kain -c 'println("hi")' -r -t llvm  # one-shot probe, like python -c (no argv
                                     # allowed with -c; needs -r to execute)
kain amalgamate kain/ -o out.kn         # pack a crate into one capsule
kain init my-crate                     # scaffold a new crate
```

TurboKain repo helper — **log every file change** (see the Ledgers section):

```bash
cd scripts && kain build memlog.kn --target llvm && cd ..   # build once
scripts/memlog.exe <area> <type> "what changed and why" "path/one,path/two"
# e.g.
scripts/memlog.exe tool build "slice.kn at C parity" "kain/core/slice.kn"
```

`memlog` stamps the ISO date, seeds the `date area type description file`
header on a new ledger, and sanitizes tabs/newlines so a field can never break
the TSV. It appends to `./memory.tsv` — run it from the repo root.

`--target llvm` is the default path for TurboKain — native CPU exes, no GPU.
Remember: **`kain build` is the gate**; `kain check` cannot verify `converge`
over `ptr` params.

### Two commands, do not confuse them

| Command | What it is | Use it? |
|---|---|---|
| **`kain`** | the **fast** compiler binary (no Bazel, launches instantly) | ✅ **always, for all TurboKain work** |
| `kaindev` | the Bazel dev **auto-sync shim** (rebuilds the compiler from source) | only when deliberately working on the Kain compiler itself |

Agents: **never add `D:/kain/.kain/bin` or `D:/tools/bazel` to PATH expecting to
fix something, and never blindly prepend random paths.** `kain` is already on
PATH and is self-contained — it resolves its own `KAIN_HOME` and runtime
library via its wrapper, so it works even in a bare shell. If you see
`failed to start bazel`, you are running the dev shim (`kaindev`) by mistake;
use plain `kain` instead. Do not try to "fix" the toolchain — it is not broken.

Fast binary is a snapshot of the last compiler build. After rebuilding the
compiler, refresh it in one command:

```
D:\tools\kain\refresh.bat    # re-copies newest build to both tools/ and .kain/bin/
```

### Stdlib + runtime discovery (why the env vars exist)

Kain finds the standard library by searching, in order:

1. `KAIN_STDLIB_PATH` (explicit)
2. `$KAIN_HOME/stdlib`  → `D:\kain\.kain\stdlib` (junction to the repo stdlib)
3. ancestors of the running `kain.exe`
4. ancestors of the cwd (this is why running from inside `kain/` works)

**Builtins** (`print`, `fs_exists`, low-level `runtime_*`) are compiled into
the binary. **Module symbols** (`process_user_args`, `text_from_byte_array`,
`os_getenv`, `runtime_simd_*`, …) come from `stdlib/*.kn` **on disk**. If no
stdlib root is found, whole modules silently vanish and the compiler tells you
to "add `use std::…`" — even though it is already there. That hint is
misleading.

The native runtime archive is resolved the same way: `KAIN_RUNTIME_LIB_PATH`
→ `$KAIN_HOME/lib/kain_runtime.lib`.

**So: if a correctly-imported stdlib module shows as `Unknown identifier`, it
is an environment/discovery problem, not your code.** Do not rewrite the
import, do not edit the toolchain. Check `KAIN_HOME`, `KAIN_STDLIB_PATH`,
`KAIN_RUNTIME_LIB_PATH` are set (User + Machine scope are both configured on
this box), and that `D:\kain\.kain\stdlib` points at `D:\kain\stdlib`.

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
kain/core/*.kn  ──►  kain amalgamate --raw kain/core -o kain/core.kn  ──►  kain build kain/core.kn  ──►  core.exe (~1.2 MB)
 (modular source)                                                           (whole-program LLVM)          │
                                                                                                        ├── core <tool> [args...]
                                                                                                        ├── core help <tool>
                                                                                                        ├── core prove
                                                                                                        └── core sweep <f32>
                                                                                                                   │
                                                                                markscript/*.md  (campaigns, IVT dispatch)
```

One file per tool during development, fused into a single whole-program
executable (`core.exe`) for research runs, keeping byte-identical CLI/CSV
contracts against the SetiYeti spec oracle.

---

## The Core Suite Architecture — Modular Source → Amalgamated Totality

TurboKain's core follows the **SQLite / BusyBox doctrine**: *write in clean,
isolated modules while developing; amalgamate into a single, fully-searchable,
whole-program-optimized unit for execution and deep cross-tool coupling.*

### Resolving the God-Component vs. Micro-Sprawl Paradox

- **Why we avoid god components:** A 50,000-line monolithic file written by
  multiple hands creates tangled global states, implicit side effects, and
  brittle couplings where changing line 400 mysteriously breaks a math loop
  on line 12,000.
- **Why we avoid micro-file sprawl:** 500 files with 30 lines each force
  developers to jump through 18 editor tabs, navigate deep directory trees,
  and fight import drift just to trace a single buffer.
- **The Amalgamation sweet spot:**
  - In `kain/core/`, each of the 14 instruments lives in its own dedicated,
    decoupled file (`slice.kn`, `fam_god.kn`, `boxcar_bank.kn`, `xvm_sandbox.kn`,
    etc.). Each tool has a single responsibility, clean inputs/outputs, and
    exports `pub fn <tool>_usage()` and `pub fn <tool>_main(args: Array<String>)`.
  - `kain/core/_common.kn` is the single source of truth for all shared
    infrastructure (kernel32 FFI, constants, memory load/store helpers,
    number parsers, quickselect, FFT, text writers). The leading underscore
    `_` guarantees it sorts first in ASCII (`_` < `b`), ensuring shared
    primitives are declared before any tool references them in raw
    amalgamation.
  - `kain/core/dispatch.kn` owns the unified `main()` entry point. It hooks
    `GetCommandLineA()` to support both `core <tool> [args...]` subcommand
    syntax and direct `<tool>.exe` multi-call invocation (if copied or symlinked).

### The Build & Amalgamation Workflow

```bash
# 1. Pack the core crate into a single unified source file:
kain amalgamate --raw kain/core -o kain/core.kn

# 2. Compile to a portable native binary (~1.2 MB, 14 tools, 77 flags, 0 runtime dependencies):
kain build kain/core.kn --target llvm -o core.exe
```

### Driving `core.exe`

```bash
core help                  # Full directory of all 14 instruments + pipeline data-flow map
core help <tool>           # Detailed mathematical background, flags, and contract for any tool
core prove                 # Run all 9 formal self-test batteries in-memory in <3s
core sweep <f32>           # Run the 7-stage detector battery over a time series in a single pass
core <tool> [args...]      # Run any tool directly (e.g. core fam_god --in scan.f32 --segbank)
```

### The Yin & Yang Trajectory (Where this is heading)

Right now, tools reside in modular files under `kain/core/*.kn` while their
individual math kernels, prove batteries, and contracts are solidified.

Once these core instruments are hardened, **our primary development center of
gravity will shift directly into `kain/core.kn`**.

Working directly in `core.kn` allows the tools to interact like **yin and yang**:
- **Zero-serialization memory handoffs:** Instead of dumping `.f32` or `bits.bin`
  to disk between stages, arenas pass directly across memory boundaries (`slice`
  memory buffers flow directly into `fam_god` and `boxcar_bank`).
- **Cross-instrument lattice coupling:** `fam_god`'s detected cyclic baud rate
  ($\alpha$) steers `bitslice` and `xvm_sandbox` in-memory; `boxcar_bank`'s DM
  candidate primes dedoppler search ranges in `drift_hunt`; `xeno_scan`'s
  kurtosis flags dynamically gate `frame_hunt` and `lag_hunt`.
- **Total whole-program visibility:** LLVM optimizes across the entire signal
  processing chain simultaneously, dead-stripping unused paths, and a single
  `grep` searches the entire scientific instrument in 2 milliseconds.

---

## Ledgers — memory.tsv + catalog.tsv

Two append-mostly ledgers carry the history. Both are modeled on the Kain
repo's `memory.tsv` and SetiYeti's `catalog.tsv`. **Update them as part of the
change, not after.**

### `memory.tsv` — the change log

Columns: `date  area  type  description  file` (tab-separated).

- **Every file change gets a row.** Created, edited, deleted, moved — if it
  touched the tree, log it. No silent edits.
- `area`: subsystem (`repo`, `docs`, `env`, `tool`, `catalog`, `build`, …)
- `type`: `add` / `update` / `fix` / `build` / `verify` / `vendor` / `scaffold` / …
- `description`: what changed and **why**, in one line (include the receipt if
  there is one — a fix without its evidence is a rumor)
- `file`: affected paths, comma-separated

Append a new line; never rewrite history. Today's date comes from the script.
Use the Kain helper (built once, then run from the repo root):

```bash
kain build scripts/memlog.kn --target llvm     # once → scripts/memlog.exe
scripts/memlog.exe <area> <type> "what changed and why" "path/one,path/two"
```

It stamps the ISO date, seeds the header if the ledger is missing, and
sanitizes tabs/newlines so a field can never break the TSV. Prefer the Kain
helper for repo tooling; Python glue is now allowed where it earns its keep
(see **Python is allowed** below), but computation stays in Kain.

### `catalog.tsv` — the tool ledger

Columns: `tool  source  exe  kind  status  prove  receipt  consumes  produces  notes  updated`.

- One row per tool/artifact. Update it whenever a tool is built, proven, or
  changes status (`draft` → `builds` → `proven` → `retired`).
- **Sky-data files are NOT catalogued here.** SetiYeti's `catalog.tsv` is the
  single scientific record of every raw/slice file; reference it by filename.
  Do not fork it — one ledger for the sky, one for our tools.
- `prove` / `receipt` must be real: the prove harness and the actual result.
  `status=proven` with an empty receipt is a lie.

A tool is not done until both ledgers say so: a `memory.tsv` row for the
change, and a `catalog.tsv` row with its status and receipt.

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
kain/        source crates and unified core suite
  core/      modular source files (_common.kn, dispatch.kn, slice.kn, fam_god.kn...)
  core.kn    raw amalgamation (all 16 files packed into single unified source)
  core.exe   portable 1.2 MB binary containing all 14 instruments
markscript/  campaign notebooks (.md) + the markscript runtime
reports/     receipts, hits, evidence — machine-checkable outputs only
_tmp/        scratch, gitignored, nothing load-bearing
docs/        spec.md + the vendored Kain baseline under docs/kain/
_objective/  the mission (objective_1.md)
scripts/     Kain helpers (memlog.kn — append a memory.tsv row)
python/      Python orchestration layer (tk driver — wrap exes, unified scans)
memory.tsv   append-only change log — EVERY file change gets a row
catalog.tsv  TurboKain tool/artifact ledger (see the Ledgers section above)
AGENTS.md    this file
```

---

## Build & run

```bash
# 1. Amalgamate and build the portable core suite:
kain amalgamate --raw kain/core -o kain/core.kn
kain build kain/core.kn --target llvm -o tkc.exe
cp tkc.exe turbokain_core.exe
cp tkc.exe core.exe

# 2. Run tools via tkc (or core / turbokain_core):
tkc <tool> [args...]
tkc help <tool>
tkc prove
tkc sweep <file.f32>

# 3. Check individual modular source files during development:
kain check kain/core/<tool>.kn
```

### Where builds put things (read this before building)

`kain build <file>.kn --target llvm` **with no `-o`**:

- **the `.exe` is copied to the current working directory**, named after the
  source stem (`tool.kn` → `tool.exe`)
- **intermediates stay next to the source**: `<source-dir>/.kain/out/…` (`.ll`,
  `runtime_contract.json`, `kain-artifacts.json`) and
  `<source-dir>/.kain/reports/build/…`
- `-o` takes a **file path, not a directory** — `-o outdir` fails with a
  `copy_file` access-denied; pass `-o path/tool.exe`

**Convention: `cd` into the tool's own folder and build there.** Then the exe
lands right beside its source (`kain/lane_sieve/lane_sieve.kn` →
`…/lane_sieve.exe`) and nothing scatters. One-off tests especially: a temp
folder with a `.kn` in it, `cd` there, build, run — no hunting through
`.kain/out/` trees for the binary.

This is a **convention, not a requirement** — explicit `-o` is always valid,
and CI/release lanes may want a single `out/` dir. But for research work,
side-by-side is easier to find, easier to delete, and keeps `.kain/` strictly
for intermediate artifacts. Exact-build-location context matters when you are
comparing tools or proving parity with the C/numpy lane next door.

No Bazel in this repo. The pipeline is **Kain-first**: `.kn` computes, `.md`
orchestrates, helpers included. Python is now sanctioned as the orchestration
layer under `python/` (see **Python is allowed** below). C and everything else
still live next door in SetiYeti as the spec-truth lane; invoke them from
there, never add a helper in another language here. The Kain toolchain lives
outside this repo (warm) — `kain` is on PATH.

---

## Python is allowed (orchestration, not detection)

Python is **chill now**. The repo is still Kain-first — detectors and the
pipeline are `.kn` → native `.exe` — but Python is sanctioned as the
**orchestration layer**: wrapping those exes, running the unified sweep,
harvesting receipts, catalog tooling — glue, not signal processing.

The line is simple: **Python drives the exes; it never re-implements a lane.**
A new detector kernel is Kain. Python may parse a log, assemble argv,
fingerprint an input, chain stages, and write a manifest.

The sanctioned home is `python/` (stdlib only — no venv, no pip):

```bash
python python/tk.py list            # driveable exes + catalog status
python python/tk.py prove           # run every built-in self-test
python python/tk.py scan <raw|f32>  # unified sweep -> reports/<date>_<tag>_scan/
python python/tk.py run TOOL [args] # pass-through exec (inherit stdio)
python python/tk.py doctor          # env vars + registry drift
```

- `python/turbokain/registry.py` is the **one place** that knows each exe's
  CLI contract. Add a `Tool(...)` row when you add an exe; add it to
  `F32_DETECTORS` if it rides the default scan bundle.
- `tk scan` writes `manifest.json` (provenance: input fingerprint, git rev,
  argv, host) + `summary.tsv` (per-stage exit/time/receipt/verdicts). A scan
  is not done until those exist.
- Rules that did **not** move: thresholds are data, never baked into the
  wrapper; no hardcoded drive letters (registry is repo-relative, data paths
  come from `--data-dir` / `$SETIYETI_DATA`); the veto stays human-fed;
  Python records verdicts, it never decides dispositions.
- If you reach for a third-party dependency, stop and ask whether the job
  belongs in Kain instead. Stdlib-only is the default for a reason.

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

- **`failed to start bazel`** → you invoked the dev shim. Use `kain` (fast);
  `kaindev` is compiler-work only. Never prepend `.kain/bin`/`bazel` to PATH
  to "fix" it.
- `converge` over `ptr` params can never pass `check`; go through `build`.
- `use std::collections` is required for `int_max`; `std::io` was missing it.
- String interpolation `"{var}"` prints literally in some paths — use
  concatenation/`str()` when in doubt.
- Actors are for **coarse fanout** (channels × blocks × pols), never per-sample
  or per-bin. Tight math belongs in `shatter`/`collapse`/`observe`/`decay`
  buffers, single-threaded.
- GPU/shader/UI paths are out of scope for Objective 1 on this box. CPU lanes
  (`capability("cpu.x86.avx2")`) are the fast path.
- **Probes go through `kain -c`, not `_tmp` files.** `kain -c '<code>' -r -t llvm`
  runs inline Kain (multi-line + `use` fine). `kain repl` is for humans;
  agents use `-c`. Caveat: `-c` cannot take argv — argv tests still need a file.
- **Bulk bytes never ride `Array<Int>`.** `fs_read_bytes_range` /
  `fs_append_bytes` cost 1–21 us/B (measured, superlinear) — ~1000x off
  memcpy. Small reads (24 KB headers) are fine; payload-scale IO must use
  kernel32 handles + Byte arenas (below), never the `fs_*` bridge.
- **Over-allocate bulk Byte arenas by +32.** Bulk byte loops auto-vectorize
  (AVX2 32B stores) and overrun exact-size arenas by up to 31 bytes:
  arenas with `nbytes % 32 != 0` aborted 127, multiples of 32 pass (11/11
  sizes, `xvm_sandbox` mut_probe repro: 24600B crashes, 24576B fine).
  Debug heaps tolerate the overrun (passes under gdb) which hides it.
  Rule: `alloc_zeroed(n + 32, "Byte")` for any arena a bulk loop touches.
  Repro filed for the compiler owner (vectorizer tail or missing guard).
- **Fast bulk IO = `@extern` kernel32 + `ptr<Byte>` arenas** (KAINOS-proven,
  no C files, no headers, no `use std::fs`): `CreateFileA` / `GetFileSizeEx` /
  `SetFilePointer` (hi/lo slot for >4 GB) / `ReadFile` / `WriteFile` /
  `CloseHandle`, `null_ptr()` = `int_to_ptr(0, "ptr<Void>")`, validity =
  `ptr_to_int(h) == -1`. One handle per file, sequential chunk reads/writes.
- **Byte load/store semantics (exact, bled for):** read byte `i` as Int via
  Int-window load `mem_load(ptr_offset(buf, i, "Byte"), "Int") & 255`
  (NOT `mem_load "Byte" + as Int` — that reinterprets the 8-byte window).
  Store via `mem_store(ptr_offset(buf, i, "Byte"), v as Byte, "Byte")`
  for v in 0..255. `alloc_zeroed(n, "Byte")` arenas are byte-granular.
- **`str(Float)` truncates toward zero** in this lane — print `str(x * 10000.0)`
  as `x1e4` (or x1e5) instead of lying with decimals.
- **Reserved words that bite:** `out`, `share`, `match` cannot be identifiers
  (params, locals, or bindings). Rename to `outn`/`sharemode`/`hit`.
- **Never run tools bare in source dirs.** Default outputs (`pulse.md`, `.f32`)
  land in cwd and pollute the repo — always pass `--out` into `reports/<run>/`
  or `_tmp/`. Source dirs hold `.kn` + gitignored `.exe`, nothing else.
- **Keep loop kernels inline or in large callees (unexplained, workaround
  holds).** A small helper with loops over a `ptr` param crashed when
  called; the identical body inline runs. Cause undetermined — could be
  my misuse (arena lifetimes, effects) — repro shape is documented
  in `kain/core/boxcar_bank.kn` (f32 section) for whoever wants it.
  CONFIRMED 2nd instance: `lfsr_fill` in `xvm_sandbox.kn` segfaulted on
  call, inlined at both sites runs. Do NOT re-extract it.
- **`use std::audio::dsp` doesn't build on this snapshot** (its source binds
  `half`, now reserved — likely version skew, not a bug) — hand-roll the
  small FFT/DFT you need, rewire on refresh.
- **One `decay` per arena per `fn` (validator joins branch states).** Two
  `decay X` in one function fail `check` even with `return` between them
  (fil_reader 2026-09-22: prove-block + later decay flagged twice).
  Fix: prove blocks own their tables (own name, single decay, single
  `pcode` return); error paths LEAK (OS reclaims on exit — slice.kn does
  this too); exactly one decay site per arena on the success path.
  `build` tolerates what `check` flags (pre-existing double `decay hbi`
  in fold_sum built fine) — but keep `check` green anyway.
- **Every detector takes `--fs` (M7, no exceptions).** fold_sum hardcoded
  `FS_HZ` and silently ignored `--fs`, mis-decimating filterbank input
  and mislabeling every Hz (Sgr B2: phantom "1585.87 Hz"). Caught by
  cross-lane check (fam bins + python rfft said 25.00), fixed live.
  Any new lane gets `--fs` on day one; audit old ones per regime.
- **boxcar_bank blows up on quantized integer power data (G5).** A 6-level
  ramp fires 23.6σ, flat constant is CLEAN — periodic-quantized input
  nulls a sub-band (≈zero MAD → division blowup; Sgr B2 ch1363 phantom
  149σ at raw z≤2). Voltage floats unaffected. Required: MAD floor
  before robust-z (same family as xeno's floored ladder division).
- **gpuspec HDF5: `import hdf5plugin` (bitshuffle) + axes are
  (time, feed, freq) despite labels claiming (freq, feed, time).**
  Verify axis identity against `nchans` before any dump.
- **Never shadow an arena name with a same-named local (lag_hunt repro).**
  A `var vlag: Int` inside a loop body shadowing the `ptr<Int> vlag`
  arena corrupts ownership tracking: `check` passes silently, then a
  deterministic exit-127 crash lands on `decay vlag` — misdiagnosed for
  an hour as heap corruption (bisected 35 decays to find it). Grep for
  `var <arena-name>` before trusting any decay crash.
- **`share` needs a heap region owned by the sharing fn.** A parameter
  pointer is a stack region to the checker (`share is not supported for
  local_alloca`) — inline the `share`/`fanout` lanes into the fn that
  owns the arenas (fold_sum pattern), never behind a helper call.
- **Strong signals poison global noise units (lag_hunt repro).** A carrier
  inflates candidate-MAD and crushes every other peak (corr 0.80 scored
  z 1.7). z must be *local* contrast over the *theoretical* moment unit
  `sqrt(m4/(M·m2²))`, never over a measured global MAD — and moments must
  be winsorized (|w| cap) or the signal inflates its own unit (AM gate
  z 3.7 raw → ~11 capped).
- **Fold at phase, not index.** `bin = (i % lag) * nb / lag` — `i * nb /
  lag` piles the whole series into the last bin and mints fake fold-z
  (lag_hunt: 8448 bogus → 4.8 honest).
- **`kain -c` trig probes lie (unresolved).** `-c 'sin(pi/2)'` prints 0
  while file-compiled trig demonstrably works (frame_hunt FFT 9/9,
  lag_hunt BPSK carrier recovered at z 139). Do not trust `-c` for
  trig; verify in file code. Repro owed to the compiler owner.
- **`kain/core/_common.kn` is the shared helper module (migrated across all 14 tools).**
  The leading underscore ensures it sorts before `bitslice.kn`, `boxcar_bank.kn`,
  etc., during `kain amalgamate --raw kain/core -o kain/core.kn`, so shared infrastructure
  is declared before any tool references it. Tools import via `use _common::X`.
  Each tool exposes `pub fn <tool>_usage()` and `pub fn <tool>_main(args: Array<String>)`.
  `kain/core/dispatch.kn` provides the multi-call entry point (`main()`) dispatching
  `core <tool> [args...]` or direct `<tool>.exe [args...]` via `GetCommandLineA`.
  Building the portable core suite:
  ```bash
  kain amalgamate --raw kain/core -o kain/core.kn
  kain build kain/core.kn --target llvm -o core.exe
  ```
  Windows shells default to cp1252: every Python file write needs `encoding='utf-8'`
  or box-drawing comments corrupt the file.

---

## Status

Baseline scaffolded. SetiYeti remains the truth. A Python orchestration layer
(`python/tk.py`) now wraps the exes for unified scans (list / prove / run /
scan / doctor / catalog), stdlib-only. First targets, in order: boxcar/fold
sieve → power sieve → evidence journal → the MarkScript campaign layer. See
`docs/spec.md`.

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
