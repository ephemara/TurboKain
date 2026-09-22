# TurboKain 📡 — listening for other people's phone calls

> *We are not looking for messages addressed to Earth. We are listening
> for interstellar communications traffic between other civilisations —
> links that happen to cross our line of sight. We are an ant on the
> forest floor listening for a truck on the highway.*

**What this is.** Nobody out there is shouting at us — and if they were,
that would be the easy case. Anyone talking to *each other* across
light-years optimises for bits per joule, and the optimal signal looks
like noise to everyone not holding the codebook. So we don't hunt tones
or beacons. We hunt **structure thermal noise cannot produce**: modulation
fingerprints in the cyclostationary plane, single pulses swept by plasma
dispersion, repeating frames, coded blocks, rastered pictures, programs
that compute. Three things are in scope — **traffic** (living links,
noise-like by design), **monuments** ("we were here" repeaters from
civilisations that may already be extinct), **payloads** (the content:
primers, rasters, executable code). The full mission lives in
`_objective/objective_1.md` — read it before anything else here.

**Why Kain.** TurboKain is written in
[Kain](https://github.com/kainlang/kain) — a systems language with Python
syntax and an inverted machine underneath. Instead of fighting hardware
with garbage collectors and defensive wrappers, Kain gives bare-metal
control and makes the *compiler* own the hard parts: memory lifecycle
(`collapse`/`observe`/`decay` — explicit ownership, no borrow checker),
fast-vs-correct dispatch (`converge` — a spec lane plus verified fast
lanes), witnessable invariants (`law`), state authority (`world`) and
journaled mutation (`patch`). It assumes all code is broken until proven
otherwise — Z3 provers and CBMC assertions ride along through compiler
and runtime. One `.kn` file compiles through LLVM to one native `.exe`
(also `.dll`/`.so`, GPU shaders, even WASM); `kain amalgamate` packs whole
toolsets into portable capsules. Each TurboKain tool is one file, one
binary, with its self-test built in — and the whole detector battery
sweeps a full telescope file in about a minute. New to the language?
Start with Kain By Example and the rulebook in the linked repo — given
a problem, the rulebook tells you exactly which construct to reach for.

**Provenance.** TurboKain shadows
[SetiYeti](https://github.com/ephemara/SetiYeti) — the Python/C prototype
this whole hunt was mapped in. Three days, full pipeline: ingest, nine
detectors, veto engine, prove harnesses, the dark-digitizer lesson, the
thicket lesson, the veto-inversion insight. Every Kain tool must reproduce
its SetiYeti oracle byte-for-byte before it earns its receipt. The
prototype found the science in days; this build makes it fast, provable,
and permanent. Nothing here was invented without first being discovered
there — just very, very quickly.

**Status: proven on the sky, working now.** Real campaigns below — repeater
scans, honest negatives, measured floors. Not a demo.

```bash
./markscript/markscript.exe run README.md          # nightly news digest
./markscript/markscript.exe check README.md        # validate, no execution
```

Run from the repo root (the intent registry resolves via `./std/`).

---

## nightly-news 📺

*Last broadcast: 2026-09-22 — FRB121102 repeater segment, full 128-block
file. No candidate, no WATCH. Burst #94 is not in this subband. Full record
in `reports/2026-09-22_frb121102_full/REPORT.md`.*

| tool | version | receipt | floor |
|------|---------|---------|-------|
| slice | 0.3.0 | PASS sliced=128, cmp-identical to C | full 17 GB file in 2.3 s |
| sk_gate | 0.1.0 | CLEAN, skdev 1.370 | deviant frac 4e-4, 0.15 s on 67M |
| boxcar_bank | 0.1.1 | 1/16 SHOT (quarantined impulse), 15/16 CLEAN | 14σ gate, ~3–4 s/tile |
| fold_sum | 0.1.0 | undetected, 19.82 Hz @12.17σ | 16σ gate, 24.3 s on 67M |
| fam_scan | 0.1.0 | CLEAN, top ratio 1.11–1.13 | ratio gate 3.0, 9.4 s on 67M |

<!-- news:slice:begin -->
slice 0.3.0 PASS sliced-128 cmp-identical-to-C full-17GB-in-2.3s
<!-- news:slice:end -->
<!-- news:sk:begin -->
sk_gate 0.1.0 PASS CLEAN skdev-1.370 frac-4e-4
<!-- news:sk:end -->
<!-- news:boxcar:begin -->
boxcar_bank 0.1.1 PASS 1-16-SHOT-quarantined 15-16-CLEAN gate-14sigma
<!-- news:boxcar:end -->
<!-- news:fold:begin -->
fold_sum 0.1.0 PASS undetected 19.82Hz-at-12.17sigma gate-16sigma
<!-- news:fold:end -->
<!-- news:fam:begin -->
fam_scan 0.1.0 PASS CLEAN ratio-1.13 gate-3.0
<!-- news:fam:end -->
<!-- news:campaign:begin -->
frb121102-full 2026-09-22 no-candidate no-WATCH floors-stated
<!-- news:campaign:end -->

## broadcast

```markscript
print("=== TURBOKAIN NIGHTLY NEWS ===")
print("latest: FRB121102 full-file sweep — no candidate, no WATCH")
print("slice:      kain/core/slice.exe (GUPPI to .f32, cmp vs C slicer)")
print("boxcar:     kain/core/boxcar_bank.exe --prove  (expect prove 4/4)")
print("sk_gate:    kain/core/sk_gate.exe --prove")
print("fold_sum:   kain/core/fold_sum.exe --prove")
print("fam:        kain/core/fam_god.exe --prove")
print("cadence:    kain/core/cadence_pair.exe (ON/OFF gate)")
print("receipts live in reports/ — a negative with a floor is a result")
```

## speed (measured, warm, receipts in reports/)

| step | TurboKain | old path |
|------|-----------|----------|
| slice full 17 GB file (128 blocks → 67M samples) | **2.3 s** | ~9 s per tile |
| SK gate on 67M samples | 0.15 s | numpy minutes-scale |
| DM/boxcar sweep, full coverage | ~3–4 s per tile | minutes per tile |
| full-segment sweep (slice+SK+boxcar+FAM) | **~1 min** (+24 s fold) | — |

*Old-path numbers are the SetiYeti Python/numpy battery on the same data.
Kain wins structurally: seek straight to the channel (14.6 MB touched vs
896 MB streamed), prefix-sum boxcars O(n) vs O(n·w) convolves, arenas vs
per-width temporaries — then static binaries with zero dependencies.*

## campaigns (the sky record)

| campaign | what | disposition |
|----------|------|-------------|
| `reports/2026-09-22_first-light/` | TRAPPIST-1 ON/OFF pair, all four tools | no-WATCH, honest negative |
| `reports/2026-09-22_frb121102/` | repeater shakedown | impulse quarantined, I2 max |
| `reports/2026-09-22_frb121102_full/` | FULL 17 GB file, 128/128 blocks, 5 tools | no candidate, no WATCH |
| `reports/2026-09-22_frb121102_multichan/` | adjacent-channel impulse census | see report |

## tools

| tool | source | what it does | oracle |
|------|--------|--------------|--------|
| slice 0.3.0 | `kain/core/slice.kn` | GUPPI raw to channel `.f32` + quarantine verdict | `c/seti_slice`, cmp-identical |
| sk_gate 0.1.0 | `kain/core/sk_gate.kn` | spectral-kurtosis anomaly gate, per-bin + 2% rule | `c/xeno_scan` SK leg |
| boxcar_bank 0.1.1 | `kain/core/boxcar_bank.kn` | DM sweep + boxcar pulse search, 14σ gate | `python/transient_dm.py`, exact |
| fold_sum 0.1.0 | `kain/core/fold_sum.kn` | periodicity fold + 8-harmonic sum, 16σ gate | `python/pulsar_fold.py` |
| fam_god 0.1.0 | `kain/core/fam_god.kn` | cyclostationary fingerprint, ratio gate 3.0 | `c/fam_scan` |
| cadence_pair | `kain/core/cadence_pair.kn` | ON/OFF gate — the only WATCH to CANDIDATE path | `python/cadence_pair.py` |

One tool = one agent = one file in `kain/core/`. Same CLI, same columns
as the oracle; scalar parity before fast lanes; prove harness is the
judge. Single files cap at grade I2 — only cadence gates CANDIDATE, and
the veto stays human-fed. Full law in `AGENTS.md`.

## quickstart

```bash
# build (exe lands beside source — always cd into kain/core first)
cd kain/core && kain build boxcar_bank.kn --target llvm && cd ../..

# self-test (every tool carries one; exit 0 + receipt=PASS or it didn't happen)
./kain/core/boxcar_bank.exe --prove

# slice one channel across 7 blocks to .f32
./kain/core/slice.exe --in <raw> --chan 44 --pol 0 --out leg.f32 --blocks 7

# sweep it for pulses (md table + csv mirror for MarkScript)
./kain/core/boxcar_bank.exe --in leg.f32 --out pulse --format both
```

## repo-functions

```bash
# ledgers — every change logs both, or it didn't happen
./scripts/memlog.exe tool update "what + receipt" "path/one,path/two"
# catalog.tsv: update the tool row by hand — status/prove/receipt
```


## repo-law (short version)

1. Kain measures, markdown remembers. `.kn` computes, `.md` orchestrates.
2. Prove before replace. No receipt, didn't happen.
3. Thresholds are data, never magic numbers.
4. The veto stays human-fed. Kain feeds it; it never decides.
5. `build` is the gate. No hardcoded paths. Don't overclaim.
