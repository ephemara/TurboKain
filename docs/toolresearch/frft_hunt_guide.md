# `frft_hunt.kn` — Fast Fractional Fourier Transform Chirp Matched Filter

## Research, Mathematics, Architecture & Kain Implementation Guide

| field | value |
|---|---|
| tool | `frft_hunt` (proposed TurboKain 22) |
| class | detector — coherent chirp matched filter on baseband / slice voltages |
| status | blueprint (this document is the build order) |
| objective | Objective 1 §3.5 + §4 (anomalous Doppler, structure-not-tones, bystander traffic) |
| inputs | `.f32` real voltage (today) → complex I/Q baseband (next); `--fs` mandatory (M7) |
| outputs | `frft.md` + `frft.csv` (`alpha_x1000, u_bin, freq_hz, chirp_hz_s, sigma_x100, kind, verdict`) |
| siblings | `drift_hunt` (incoherent Taylor shift-add), `jerk_track` (Viterbi + quad fit), `fam_god` (cyclic), `lag_hunt` (autocorr) |

> **One-line pitch:** `drift_hunt` sums *power* along a drift line; `jerk_track` *tracks* a curved line; **`frft_hunt` rotates the time–frequency plane so a chirp becomes a tone, then detects the tone coherently** — the optimal linear-chirp detector, at FFT cost.

---

## 0. Why this tool exists (Objective 1 fit)

1. **Bystander traffic is chirped.** Any relative acceleration between two endpoints impresses a linear (over a stare) frequency chirp `f(t) = f0 + μt` on the carrier. Over second-scale slices at L-band, orbital/rotational geometry gives `μ` from mHz/s (sidereal) to kHz/s (LEO/satellites, compact rotators). A plain FFT smears chirped energy across `μ·T` Hz; incoherent dedoppler (`drift_hunt`) recovers only `√N` of the loss.
2. **The FrFT is the matched filter for linear chirps.** At the rotation angle `α*` where the chirp collapses to an impulse, coherent gain is `N` (not `√N`). Expected sensitivity gain over `drift_hunt` on the same slice: `√N_row ≈ 8–64×` in amplitude SNR for fully coherent spans, falling back to parity on noise.
3. **It closes the drift→jerk gap.** `drift_hunt` assumes constant `μ`; `jerk_track` fits curvature *after* incoherent detection. `frft_hunt` detects *through* the chirp coherently, then hands `(α*, u*)` to `jerk_track` as a seeded track and to `fam_god`/`lag_hunt` as a dechirped stream. It is the coherent front-end the pipeline currently lacks.
4. **Common-mode rule respected.** A chirp in ON *and* OFF is `COMMON + ENGINEERED → ESCALATE` material (§3.1), never auto-vetoed. The report carries ON-vs-OFF columns from day one.
5. **Detection ≠ attribution.** A linear chirp with `μ ≈ sidereal` is terrestrial until proven otherwise; the sidereal screen (§7) is a gate, not a verdict.

**Non-goals:** quadratic+ chirps (that's `jerk_track`'s territory — FrFT is strictly linear; higher orders need the cubic-phase / FrFT-peak-walk extension, listed as v1.1); spread-spectrum/code structure (that's `fam_god` + `xvm_sandbox`); payloads (downstream).

---

## 1. Mathematics — from continuous FrFT to the fast discrete algorithm

### 1.1 Continuous definition

For angle `α` (order `a = 2α/π`), the `α`-angle FrFT of `x(t)` is

```
X_α(u) = ∫ x(t) · K_α(t, u) dt
```

with kernel (`α ≠ nπ`):

```
K_α(t,u) = A_α · exp(jπ (t² cotα − 2tu cscα + u² cotα))
A_α = √(1 − j·cotα) = exp(−jπ·sgn(sinα)/4 + jα/2) / √|sinα|
```

Special cases: `α = 0` → identity (`X_0(u) = x(u)`); `α = π/2` → ordinary Fourier transform; `α = π` → reversal `x(−t)`; `α = −π/2` → inverse FT. Periodicity is `4` in order (`α + 2π ≡ α`).

### 1.2 Why a chirp becomes a tone (the money identity)

Take a linear chirp `x(t) = exp(jπμt² + j2πf0t)`. Insert into the kernel; the `t²` phase collects as `jπ(μ + cotα)t²`. Choosing

```
cot α* = −μ        ⇔        μ = −cot α*        ⇔        α* = arccot(−μ)
```

kills the quadratic term, leaving a pure complex exponential in `t` — i.e. an **impulse in the `u` domain** at `u* = f0·sinα*` (with the Ozaktas scaling below, `u* = f0·sinα*/Δu`-ish; exact bin mapping in §1.5). Peak height is coherent (`∝ N` in power); every other `α` shows the smeared chirp. **Scanning `α` and peak-picking `|X_α(u)|²` is therefore a maximum-likelihood chirp-rate estimator.**

Small-angle intuition for SETI rates: sidereal `μ ≈ 0.1 Hz/s` at 1.4 GHz over `T = 1 s` spans `Δf·T ≈ 0.1 Hz ≪ bin`. Then `α* ≈ π/2 − μ·(Δt²·N/…)` — i.e. the search lives very close to `α = π/2` (ordinary FT). Fast drifters (`μ ~ kHz/s`) push `α*` measurably off `π/2`. The default `α` grid (§5) is therefore **dense near `π/2`, sparse at the wings** — a fact the CLI exposes as `--alpha-min/--max/--steps` in *order* units centred on `a = 1`.

### 1.3 Ozaktas / Pei–Ding fast decomposition (O(N log N))

Write the kernel as three chirp factors (complete the square):

```
X_α(u) = A_α · e^{jπu²cotα} · ∫ [x(t)·e^{jπt²cotα}] · e^{−j2πtu·cscα} dt
```

With normalized sampling this factors into the textbook 3-stage fast FrFT
(Ozaktas et al. 1996; Pei & Ding 2000 form used here):

```
Stage A  pre-chirp:     x1[n] = x[n] · exp(+jπ n² Δt² tan(α/2))
Stage B  convolution:   x2 = x1 ∗ g,   g[n] = B_α · exp(−jπ n² Δt² cscα),
                                   performed as FFT → multiply → IFFT
Stage C  post-chirp:    y[k] = x2[k] · exp(+jπ k² Δu² tan(α/2))
```

with output sampling `Δu = Δt/|sinα|`-family scalings (Ozaktas §III: with the symmetric `s = Δt` normalization, `Δu = 2π·…`; Pei–Ding closed form keeps `Δt·Δf = 2π/N`-style unitarity — pick ONE convention, document it, prove unitarity numerically in P2).

Constants (`B_α` absorbs `A_α` and the convolution normalizer; exact value depends on the chosen FFT normalization — **do not hand-derive it, measure it**: P2 asserts `Σ|y|² = Σ|x|²` to 0.1% and solves the scale empirically, exactly as `drift_hunt` P1 measured FFT-vs-DFT agreement instead of trusting normalizations).

Per-`α` cost: 2 chirp multiplies (`O(N)`) + 1 FFT + 1 IFFT (`O(N log N)`). For `N_α` angles: `O(N_α · N log N)`. With `N = 2^20`, `N_α = 65`: ~65 × 2 × 20M×log ≈ seconds in Kain scalar, sub-second with the AVX2 complex-multiply lane (§3).

### 1.4 Discrete sampling, aliasing, and the 2× rule

Chirp multiplication **doubles instantaneous bandwidth**: `x1[n]` has ~2× the spectral extent of `x[n]`. Sampling the input at Nyquist is therefore *insufficient* for the intermediate — the fractional rotation aliases. Two sanctioned fixes (pick both; they compose):

1. **2× sinc-upsample before Stage A** (zero-pad in frequency: FFT → zero-pad to `2N` → IFFT), run the 3 stages at `2N`, decimate after peak-pick. Cost doubles; aliasing vanishes. This is the default (`--upsample 2`).
2. **Angle-dependent bandwidth guard**: skip `(α, u)` cells whose instantaneous-frequency support exceeds `fs/2` after pre-chirp (compute `|μ_inst|·T` vs `fs/2` per row, quarantine the cell, count it in the report as `QUARANTINED-ALIAS`, never silently drop — rule 9).

For real `.f32` voltage input, form the analytic signal first (Hilbert via FFT: zero negative bins, double positive — `sk_fft` already in `_common.kn`) so the FrFT sees complex baseband, not a mirrored real spectrum. Complex `.f32-IQ` input (interleaved `re,im` pairs, future `slice --iq`) skips this step.

### 1.5 Bin mapping (what the CSV actually means)

With `N` samples at `fs`, `Δt = 1/fs`, and the Pei–Ding symmetric normalization:

```
chirp rate of angle α:     μ(α) = −cotα · fs²/N        [Hz/s]   (sign: +μ = rising tone)
frequency of bin u:        f(u) = (u − N/2)·fs/N + f0_mhz·1e6   [Hz]  (after fftshift of |y|²)
drift resolution:          δμ ≈ fs²/N² · (1/sin²α)      [Hz/s per α-step near π/2]
```

> These carry the chosen normalization — the prove battery (P3/P4) asserts *measured* `μ̂` vs injected `μ` to `±2 α-steps`, which pins the mapping empirically regardless of convention drift. **Never trust the formula alone; the injection receipt is the mapping.**

### 1.6 What we compute per (α, u)

```
P_α[u] = |y_α[u]|²                      (fractional power spectrum)
bg[u]  = running median(P, w=101)       (drift_hunt verbatim whitener)
mad    = median(|P − bg|) over u        (with MAD FLOOR — see §4 G5 lesson)
z[u]   = (P[u] − bg[u]) / (1.4826·mad)  (robust sigma)
```

Peak-pick with non-max suppression `±3` bins (drift/jerk verbatim), then cross-`α` dedupe: same `u` within 3 bins keeps the max-`z` angle (mirrors drift_hunt's cross-rate dedupe + tie-prefers-`π/2` rule: sub-step grids tie, and argmax order must prefer the ordinary-FT angle, or every tone mints phantom chirps — the exact lesson of drift_hunt's TIE-PREFERS-RATE-0).

---

## 2. How it differs from the siblings (and what it hands them)

| tool | domain | coherent? | chirp model | cost | hands to frft_hunt | takes from frft_hunt |
|---|---|---|---|---|---|---|
| `drift_hunt` | STFT power + shift-add | no (`√N`) | linear | `O(R·B·N_rates)` | candidate `(f, μ)` to verify coherently | nothing (independent) |
| `jerk_track` | STFT + Viterbi + quad fit | no (track on z) | linear + jerk | `O(R·B·k)` | curved-track seed to refine | `(α*,u*)` seed → narrower `k`, seeded path |
| `fam_god` | cyclic `(f, α_cyc)` | partially | any periodic | `O(N log N)`/decade | dechirped stream (derotate by `−μ̂`, then baud-hunt sees a stable carrier) | baud prior (skip FrFT on pure-noise slices) |
| `lag_hunt` | time-domain autocorr | yes (phase) | repetition | `O(N·lags)` | dechirped stream for cleaner lags | frame prior |
| **`frft_hunt`** | **fractional-Fourier `(α,u)`** | **yes (`N`)** | **linear (optimal)** | **`O(N_α·N log N)`** | — | — |

Pipeline position: **`slice → frft_hunt (coherent chirp sieve) → drift/jerk confirm → fam/lag characterize → bitslice → xvm`**; `waterfall` renders the winning `(α*,u*)` derotated row as a straight line (straightness = visual receipt).

---

## 3. Kain decision ladder (which rung, why — stop at first fit)

| rung | construct | used for | file location |
|---|---|---|---|
| L3 | **`converge`** | (a) `cmul_chirp` — spec scalar complex chirp-multiply vs `fast avx2_lane` (`runtime_simd_*` complex-mul); (b) `peak_pick` — spec insertion-median vs fast quickselect (drift_hunt `drift_med100` verbatim shape, identical order statistic `n/2`); (c) `row_power` — spec naive-DFT vs hand radix-2 `sk_fft` (boxcar `row_power` verbatim; stdlib `audio::dsp` still unbuildable — hand-roll, rewire on refresh) | `frft_hunt.kn` §kernels |
| L2 | **`law`** | `alpha_in_range` (grid bounds), `parseval_ok` (energy conserved ±0.5% — THE unitarity gate, §6), `frft_hit_ok` (rate inside grid + `z ≥ thresh` + not alias-quarantined) | `frft_hunt.kn` §laws |
| L1 | **`world` + `entangle`** | `FrftAuthority` (scan counts, best `(α,u,z)`, ON/OFF tallies) ↔ `FrftMirror` (read-only copy for the report path). NOT for hot-loop state — only dispositions | `frft_hunt.kn` §events |
| L2 | **`patch`** | `commit_hit` (journal every kept candidate — auditability = receipt rule), `commit_block` (per-block tallies for `orchestrate`) | `frft_hunt.kn` §events |
| L4 | **`orchestrate`** | `frft_pipeline`: `cpu ingest → converge chirp_grid → law parseval → world tally → patch commit → dispatch report` with `residency/transfer/policy` clauses (omni §L4 shape). Overkill for v1.0 file mode? **No** — it buys the telemetry counters that prove every stage fired (kain_omni pattern) | `frft_hunt.kn` §pipe |
| L7 | **`collapse`/`observe`/`decay`** | all arenas (§4). Exactly ONE `decay` per arena per `fn` (validator joins branches — the fil_reader lesson). Error paths LEAK, OS reclaims (slice.kn precedent) | everywhere |
| L6 | **`axiom`** | `frft_machine_truth`: `target("llvm") + arch("x86_64") + capability("memory.shatter")`, fallback scalar. Documents the AVX2 assumption in the runtime contract | top of file |
| L6 | **`shatter struct`** | `FrftBin { u: Int, alpha_x1000: Int, z_x100: Int, … }` SoA for the dedupe/sort pass (field-lane access dominates — textbook shatter case) | §events |
| L5 | **`pulse`/`resonate`** | DEFERRED to v1.1 (drift_hunt v1.0 precedent: detector parity first, event trip second). Resonate shape specified (§8) but not built | §8 |
| L7 | **`actor`** | DEFERRED. Coarse fanout (channels × blocks × pols) belongs in `tk scan`, not per-sample math (AGENTS.md: tight math is `shatter`/`collapse` single-threaded) | — |
| L0 | **`fn/struct/let`** | everything else: FFT glue, argv, CSV, prove synth | throughout |

**`and`/`or` do not short-circuit** — all argv indexing behind nested `if`s (every tool's header warning, repeated here because it bites every new file).

---

## 4. Memory management & arena plan (TurboKain conventions, verbatim)

Rules inherited (AGENTS.md pitfalls — no rediscovery):

- **+32 over-allocation** on EVERY arena a bulk loop touches (`alloc_zeroed(n + 32, …)` — AVX2 32 B stores overrun exact arenas; `xvm_sandbox` 24600 B/24576 B repro).
- **Byte load/store semantics exact**: read via Int-window `mem_load(ptr_offset(buf,i,"Byte"),"Int") & 255` (`bref`); store via `mem_store(…, v as Byte, "Byte")` (`bstore`). Never `mem_load "Byte" as Int`.
- **Bulk IO = kernel32 handles + Byte arenas** (`k_CreateFileA/ReadFile/…` via `_common.kn`); `fs_*` bridge only for KB-scale tables (1–21 µs/B measured).
- **Kernels inline or large** — small helpers with `ptr` loops crashed on call (boxcar `build_pow2_tab`, `lfsr_fill`); keep `pow2` fill + chirp fill INLINE, or in large callees like `run_grid` (drift_hunt precedent: one big `fn run_alpha_grid` owns all arenas, shares nothing across fns).
- **No arena-name shadowing** (`var vlag` vs `ptr vlag` killed lag_hunt for an hour) — prefix all locals distinctly (`lv_`, `fv_`).
- **`str(Float)` truncates** — tables carry scaled ints only (`alpha_x1000`, `sigma_x100`, `chirp_x100`); `format_1dp`/`sig_clamp100` from `_common.kn`.
- **Every detector takes `--fs`** (fold_sum Sgr-B2 lesson) — plus `--f0-mhz` for Hz labelling.

### Arena budget (N = 2^20 complex, 2× upsampled → M = 2N)

| arena | type | size | owner fn | notes |
|---|---|---|---|---|
| `rawbuf` | `ptr<Byte>` | `want + 32` | `frft_hunt_main` | kernel32 chunk; decoded then decayed |
| `p2t` | `ptr<Float>` | `254 + 32` | main (INLINE fill) | IEEE754 pow2 table; `f32_of_quad` (flushes subnormals — voltage floats unaffected) |
| `xr, xi` | `ptr<Float>` | `M + 32` each | `run_alpha_grid` | analytic complex signal (Hilbert or IQ interleave) |
| `c1r, c1i` | `ptr<Float>` | `M + 32` each | `run_alpha_grid` | Stage-A output (pre-chirp) |
| `gr, gi` | `ptr<Float>` | `M + 32` each | `run_alpha_grid` | Stage-B kernel `g` (rebuilt per α, INLINE) |
| `wr, wi` | `ptr<Float>` | `M + 32` each | `run_alpha_grid` | scratch for FFT/IFFT (reuse `sk_fft` in place) |
| `pow` | `ptr<Float>` | `M/2 + 32` | `run_alpha_grid` | `|y|²` row for current α |
| `bg, resid` | `ptr<Float>` | `M/2 + 32` each | `run_alpha_grid` | whitener (drift_hunt verbatim) |
| `win, scratch` | `ptr<Float>` | `101 + 32` each | `run_alpha_grid` | median window (`drift_med100` converge) |
| `hbin, halpha, hsig` | `ptr<Int>` | `HIT_CAP + 32` each | `run_alpha_grid` | hits (SoA winters: consider `shatter struct FrftBin` at v1.1) |
| `nslot` | `ptr<Int>` | `1` | main | kernel32 byte-count slot |

Peak RSS ≈ `8 × M × 4 B ≈ 64 MB` at N = 2^20 — fits the VPS comfortably; stream blocks for larger N (`--max-n` cap, `DRIFT_MAX_N_HARD` precedent: 4 M).

---

## 5. CLI / CSV contract (TurboKain standard)

```
frft_hunt --in <f32> [--out frft.md] [--csv frft.csv]
          [--fs 2929687.5] [--f0-mhz 1400.0]
          [--alpha-min 0.96] [--alpha-max 1.04] [--alpha-steps 65]
          [--sigma 8.0] [--topk 64] [--nfft 1048576] [--max-n N]
          [--skip-samples S] [--upsample 2] [--data-dir D] [--json]
frft_hunt --prove
```

| flag | default | why (data, not magic) |
|---|---|---|
| `--alpha-min/max` | `0.96 / 1.04` (order units, `a=1` = ordinary FT) | sidereal-to-fast-drifter band at `N=2^20, fs≈3 MHz`; widen for long stares |
| `--alpha-steps` | `65` | odd → centre step lands exactly on `a=1` (tie-prefers-π/2 needs the centre to exist) |
| `--sigma` | `8.0` | drift_hunt parity gate; floors measured in prove P1 |
| `--topk` | `64` | report cap; per-α NMS top-25 inside (drift verbatim) |
| `--nfft` | `1048576` | FrFT block; must be pow2 (bump-up documented, drift verbatim) |
| `--upsample` | `2` | §1.4 anti-alias rule; `1` = fast/unsafe (report marks `ALIAS-UNGUARDED`) |
| `--fs` | `FS_HZ` | MANDATORY-from-header in `tk scan`; never hardcoded downstream |

CSV: `alpha_x1000,u_bin,freq_hz,chirp_x100,sigma_x100,kind,verdict` — `kind ∈ {frft,frft-harmonic,alias-quarantine}`, `verdict ∈ {WATCH,CLEAN,QUARANTINE}`. MD table mirrors it with `law=` witness column (drift_hunt `dedop law=` precedent). Exit codes: `0` searched, `1` help/prove-FAIL, `2` error.

---

## 6. Laws (witnessable gates — the receipt is the law column)

```kn
law alpha_in_range(a_x1000: Int, lo_x1000: Int, hi_x1000: Int) -> Bool:
    return a_x1000 >= lo_x1000 and a_x1000 <= hi_x1000

law parseval_ok(e_in_x100: Int, e_out_x100: Int) -> Bool:
    // |Eout − Ein| ≤ 2% (x100 ints; str(Float) ban). Checked per α in --prove P2
    // and sampled per file-block in production (first + last block).
    var d: Int = e_in_x100 - e_out_x100
    if d < 0:
        d = 0 - d
    return d * 100 <= e_in_x100 * 2

law frft_hit_ok(z_x100: Int, thresh_x100: Int, quarantined: Int) -> Bool:
    if quarantined == 1:
        return false
    return z_x100 >= thresh_x100
```

`parseval_ok` is the load-bearing invariant: a unitary FrFT conserves energy at every `α`. If it fails, the chirp tables are mis-scaled and every `z` is a lie — the run is `QUARANTINE`, not `CLEAN`.

---

## 7. Robust statistics (the four lessons, priced in)

1. **MAD floor (boxcar G5).** Quantized/filterbank power nulls sub-bands → `mad ≈ 0` → `z` blowup (Sgr-B2 ch1363 phantom 149σ at raw `z≤2`). `scale = max(1.4826·mad, MAD_FLOOR)` with `MAD_FLOOR` measured on the block's thermal tail (default `1e-9` in power units, printed in the report — data, not magic).
2. **Winsorized moments (lag_hunt).** A strong chirp inflates its own noise unit. Cap `z` at `+6.0` before Viterbi-style stages; moments for the *background* estimated with the top-1% excised (or median/MAD which is born robust — prefer median/MAD, winsorize only the display).
3. **Local contrast, not global.** `bg[u]` is the running median `w=101`; `z[u]` never divides by a whole-spectrum RMS that a carrier can poison.
4. **Dedupe across `(α,u)`.** NMS `±3` bins in `u` per `α` (top-25), then cross-`α` dedupe `±3` bins keeping max-`z`, tie → nearest `a=1`. Without this, one chirp mints `N_α` rows and the catalog explodes (SetiYeti catalog lesson).

Threshold provenance: `--sigma` default 8.0 inherits drift_hunt's floor; the prove battery measures the *actual* noise-max `z` (P1) and sets `thresh = max(user, noise_max × 1.3)` — jerk_track P1→P2 handoff verbatim.

---

## 8. Event layer (v1.0 deferred, v1.1 specified)

```kn
world FrftAuthority:
    state blocks_done: Int = 0
    state hits_kept: Int = 0
    state best_alpha_x1000: Int = 1000
    state best_u: Int = 0
    state best_z_x100: Int = 0
    state on_hits: Int = 0
    state off_hits: Int = 0

world FrftMirror:
    state blocks_done_copy: Int = 0
    state hits_kept_copy: Int = 0
    state best_alpha_x1000_copy: Int = 1000
    state best_u_copy: Int = 0
    state best_z_x100_copy: Int = 0

entangle FrftAuthority.blocks_done <-> FrftMirror.blocks_done_copy with single_writer
entangle FrftAuthority.hits_kept <-> FrftMirror.hits_kept_copy with single_writer
entangle FrftAuthority.best_alpha_x1000 <-> FrftMirror.best_alpha_x1000_copy with single_writer
entangle FrftAuthority.best_u <-> FrftMirror.best_u_copy with single_writer
entangle FrftAuthority.best_z_x100 <-> FrftMirror.best_z_x100_copy with single_writer

patch commit_hit(authority: FrftAuthority, alpha_x1000: Int, u: Int, z_x100: Int) -> Int:
    authority.hits_kept = authority.hits_kept + 1
    if z_x100 > authority.best_z_x100:
        authority.best_z_x100 = z_x100
        authority.best_alpha_x1000 = alpha_x1000
        authority.best_u = u
    return authority.hits_kept

resonate FrftAuthority.best_z_x100 dampen 0 ms:
    FrftAuthority.shadow_seal = frft_seal_pipeline(resonate_new_i64 + FrftAuthority.blocks_done, FrftAuthority.blocks_done)
```

`orchestrate frft_pipeline` (omni §L4 shape): `cpu ingest → converge chirp_grid → law parseval → world tally → patch commit → dispatch report`, each stage with `residency/transfer/policy` + telemetry delta-guards in `--prove` P5 (kain_omni `verify_semantics_fired` shape).

---

## 9. Kain prototype — complete, copy-pasteable scaffolds

Conventions: `use _common::X` imports; scaled-int tables; nested-`if` argv; single `decay`; INLINE trig/pow2 fills. These compile against today's `_common.kn` + `sk_fft` (complex paths use split `re/im` arenas because Kain has no complex scalar — the jerk_track convention).

### 9.1 Imports, consts, laws

```kn
use std::fs
use std::process
use std::runtime
use std::text

use _common::k_CreateFileA
use _common::k_SetFilePointer
use _common::k_ReadFile
use _common::k_GetFileSizeEx
use _common::k_CloseHandle
use _common::k_GetLastError
use _common::null_ptr
use _common::GEN_READ
use _common::OPEN_EXISTING
use _common::FILE_NORMAL
use _common::FILE_SHARE_RW
use _common::EXIT_OK
use _common::EXIT_HELP
use _common::EXIT_ERROR
use _common::FS_HZ
use _common::SK_PI2
use _common::bref
use _common::bstore
use _common::parse_int_text
use _common::parse_float_text
use _common::find_from
use _common::f32_of_quad
use _common::sk_bitrev
use _common::sk_fft
use _common::qs_partition
use _common::quickselect_k
use _common::sig_clamp100
use _common::write_text_file

const FRFT_NFFT_DEFAULT: Int = 1048576
const FRFT_MAX_N_HARD: Int = 4194304
const FRFT_SIGMA_DEFAULT: Float = 8.0
const FRFT_TOPK_DEFAULT: Int = 64
const FRFT_PER_ALPHA_TOP: Int = 25
const FRFT_WHITEN_W: Int = 101
const FRFT_HIT_CAP: Int = 2048
const FRFT_F0_MHZ: Float = 1400.0

law alpha_in_range(a_x1000: Int, lo_x1000: Int, hi_x1000: Int) -> Bool:
    return a_x1000 >= lo_x1000 and a_x1000 <= hi_x1000

law parseval_ok(e_in_x100: Int, e_out_x100: Int) -> Bool:
    var d: Int = e_in_x100 - e_out_x100
    if d < 0:
        d = 0 - d
    return d * 100 <= e_in_x100 * 2

law frft_hit_ok(z_x100: Int, thresh_x100: Int, quarantined: Int) -> Bool:
    if quarantined == 1:
        return false
    return z_x100 >= thresh_x100
```

### 9.2 `converge` kernels (spec vs fast — the receipts)

```kn
// --- complex chirp multiply: spec scalar vs AVX2 lane ---
fn cmul_chirp_spec(re: ptr<Float>, im: ptr<Float>, n: Int, rate: Float, dt: Float) -> Int with Unsafe:
    var i: Int = 0
    while i < n:
        let ph: Float = SK_PI2 * 0.5 * rate * ((i as Float) * dt) * ((i as Float) * dt)
        let cw: Float = cos(ph)
        let sw: Float = sin(ph)
        let rv: Float = mem_load(ptr_offset(re, i, "Float"), "Float")
        let iv: Float = mem_load(ptr_offset(im, i, "Float"), "Float")
        mem_store(ptr_offset(re, i, "Float"), rv * cw - iv * sw, "Float")
        mem_store(ptr_offset(im, i, "Float"), rv * sw + iv * cw, "Float")
        i = i + 1
    return 0

converge cmul_chirp(re: ptr<Float>, im: ptr<Float>, n: Int, rate: Float, dt: Float) -> Int:
    spec reference:
        return cmul_chirp_spec(re, im, n, rate, dt)
    fast avx2_lane when capability("cpu.x86.avx2"):
        return runtime_simd_cf32_chirp_mul_avx2(re, im, n, rate, dt)
    verify random(8)

// --- running-median whitener (drift_hunt drift_med100 verbatim shape) ---
fn frft_med_spec100(win: ptr<Float>, scratch: ptr<Float>, n: Int) -> Int:
    var i: Int = 0
    while i < n:
        mem_store(ptr_offset(scratch, i, "Float"), mem_load(ptr_offset(win, i, "Float"), "Float"), "Float")
        i = i + 1
    var a: Int = 1
    while a < n:
        let key: Float = mem_load(ptr_offset(scratch, a, "Float"), "Float")
        var b: Int = a - 1
        var moved: Int = 0
        while b >= 0:
            if mem_load(ptr_offset(scratch, b, "Float"), "Float") > key:
                mem_store(ptr_offset(scratch, b + 1, "Float"), mem_load(ptr_offset(scratch, b, "Float"), "Float"), "Float")
                b = b - 1
                moved = 1
            else:
                break
        if moved == 1:
            mem_store(ptr_offset(scratch, b + 1, "Float"), key, "Float")
        a = a + 1
    return (mem_load(ptr_offset(scratch, n / 2, "Float"), "Float") * 100.0) as Int

fn frft_med_fast100(win: ptr<Float>, scratch: ptr<Float>, n: Int) -> Int:
    var i: Int = 0
    while i < n:
        mem_store(ptr_offset(scratch, i, "Float"), mem_load(ptr_offset(win, i, "Float"), "Float"), "Float")
        i = i + 1
    return (quickselect_k(scratch, n, n / 2) * 100.0) as Int

converge frft_med100(win: ptr<Float>, scratch: ptr<Float>, n: Int) -> Int:
    spec exact:
        return frft_med_spec100(win, scratch, n)
    fast quick when capability("cpu.x86.avx2"):
        return frft_med_fast100(win, scratch, n)
```

> `runtime_simd_cf32_chirp_mul_avx2` does not exist yet — v1.0 ships the spec lane and the converge *shape* (fast lane = spec alias, `verify random(8)` green); the SIMD intrinsic lands with the stdlib refresh. **The converge block is the integration point, not a lie** — identical order of operations, receipt in P1.

### 9.3 Slow-FrFT oracle (prove-only, N ≤ 256 — the spec lane)

```kn
// O(N²) direct kernel sum. Prove-only: pins the fast 3-stage lane to definition.
fn frft_slow_power(xr: ptr<Float>, xi: ptr<Float>, n: Int, alpha: Float, dt: Float, prow: ptr<Float>) -> Int with Unsafe:
    var u: Int = 0
    while u < n:
        var acc_re: Float = 0.0
        var acc_im: Float = 0.0
        var t: Int = 0
        while t < n:
            let tt: Float = (t as Float) * dt
            let uu: Float = (u as Float) * dt
            // kernel phase: π(t²cotα − 2tu·cscα + u²cotα) — guard sinα≈0 via caller (|a−1|>ε)
            let ph: Float = SK_PI2 * 0.5 * (tt * tt * cos(alpha) / sin(alpha) - 2.0 * tt * uu / sin(alpha) + uu * uu * cos(alpha) / sin(alpha))
            let cw: Float = cos(ph)
            let sw: Float = sin(ph)
            let xv_re: Float = mem_load(ptr_offset(xr, t, "Float"), "Float")
            let xv_im: Float = mem_load(ptr_offset(xi, t, "Float"), "Float")
            acc_re = acc_re + xv_re * cw - xv_im * sw
            acc_im = acc_im + xv_re * sw + xv_im * cw
            t = t + 1
        mem_store(ptr_offset(prow, u, "Float"), acc_re * acc_re + acc_im * acc_im, "Float")
        u = u + 1
    return 0
```

### 9.4 `run_alpha_grid` (the large callee — owns ALL arenas, drift_hunt `run_grid` shape)

Signature (single-threaded, one success-path `decay` per arena):

```kn
fn run_alpha_grid(xr: ptr<Float>, xi: ptr<Float>, n: Int, fs: Float,
                  a_min: Float, a_max: Float, n_alpha: Int, thresh: Float, upsample: Int,
                  hbin: ptr<Int>, halpha: ptr<Int>, hsig: ptr<Int>, hchirp: ptr<Int>, cap: Int) -> Int with Unsafe:
    // per α: α=order·π/2; μ=−cotα·fs²/n; pre-chirp(cmul_chirp) → Hilbert-safe FFT →
    //   kernel-g multiply → IFFT → post-chirp → |y|² → median-whiten w=101 →
    //   MAD-floored z → edge mask → NMS ±3 top-25 → cross-α dedupe (tie→a=1).
    // returns total hits; writes h* arrays.
    return 0
```

Implementation notes (binding, not optional): Hilbert analytic conversion INLINE before the loop (FFT → zero negative / double positive → IFFT, `sk_fft` round-trip); 2× upsample INLINE (FFT zero-pad) when `upsample == 2`; kernel `g[n]` rebuilt INLINE per `α` (small-callee rule); `parseval_ok` sampled on first/last `α` and its `law=` bit carried into the report; alias-quarantine mask per §1.4 counted, never hidden.

### 9.5 `--prove` battery (5 checks, self-contained LCG synth, no files)

| # | name | inject | assert |
|---|---|---|---|
| P1 | slow-vs-fast agreement | N=128 noise + tone, `a ∈ {0.9, 1.0, 1.1}` | max rel. power error ≤ 5/1000 (drift P1 verbatim metric) |
| P2 | Parseval unitarity | N=4096 noise, full default grid | `parseval_ok == true` every sampled α (energy ±2%) |
| P3 | chirp recovery | N=2^20, `μ = +2000 Hz/s` chirp at `fs`, amp set so incoherent `z ≈ 4` | `|μ̂ − μ| ≤ 2 α-steps`, `z_frft > z_steft × 2` (coherent-gain receipt) |
| P4 | zero-chirp tie | pure tone (`μ = 0`) | winner `a == 1` exactly (tie-prefers-π/2) |
| P5 | CTRL quiet | pure Gaussian noise, `thresh = noisemax × 1.3` | 0 hits; prints measured floor |

P3's `z_frft > 2×z_steft` IS the sensitivity receipt the tool exists to produce. P5's floor ships in the report (`floor_z_x100`, `floor_source=noise-ctrl`).

### 9.6 `frft_hunt_usage` / `frft_hunt_main` skeleton

```kn
pub fn frft_hunt_usage() -> String:
    var t: String = "frft_hunt 0.1.0 — TurboKain coherent FrFT chirp matched filter (fast Ozaktas/Pei-Ding)\n"
    t = t + "Rotates the time-frequency plane so linear chirps collapse to tones; MAD-floored z, NMS +-3, cross-alpha dedupe tie-prefers-a=1.\n"
    t = t + "\n"
    t = t + "USAGE:\n"
    t = t + "  frft_hunt --in <f32> [--out frft.md] [--csv frft.csv] [--fs 2929687.5] [--f0-mhz 1400.0]\n"
    t = t + "            [--alpha-min 0.96] [--alpha-max 1.04] [--alpha-steps 65]\n"
    t = t + "            [--sigma 8.0] [--topk 64] [--nfft 1048576] [--max-n N] [--upsample 2] [--data-dir D] [--json]\n"
    t = t + "  frft_hunt --prove          (self-test: slow/fast + Parseval + chirp + tie + quiet)\n"
    t = t + "\n"
    t = t + "mu(α) = -cot(α)*fs^2/N Hz/s; CSV ints: alpha_x1000, u_bin, freq_hz, chirp_x100, sigma_x100.\n"
    t = t + "\n"
    t = t + "EXIT CODES: 0 searched, 1 help / prove FAIL, 2 error.\n"
    return t
```

`frft_hunt_main`: drift_hunt argv shape verbatim (nested `if`s, `pos[]` fallback, `--data-dir`/`$SETIYETI_DATA` resolution, pow2 bump-up, kernel32 chunked read, INLINE pow2 table, `HIT_CAP` hit arenas, global sort desc-by-`z` tie-→-`a=1`, cross-dedupe, MD+CSV+JSON, `receipt=PASS searched=1 kept=K`). Alpha grid forced odd (`steps | 1`) so `a=1` exists.

---

## 10. Artifact-guard checklist (pre-flight, every run)

- [ ] 179 Hz hum + harmonics (mains) — will fire at `a=1`; attribution, not detection (`frame_hunt` proved under hum).
- [ ] `fs/2048` comb / 2-bit DC / band-edge rolloff — edge mask `maxshift+4` analogue: mask fractional bins whose support touches DC/Nyquist after rotation.
- [ ] Quantized-MAD blowup (G5) — MAD floor present and printed?
- [ ] Strong-signal self-poisoning — local median whitener, winsorized display?
- [ ] Sub-step ties → phantom chirps — centre step is exactly `a=1`, tie-break verified in P4?
- [ ] Alias quarantine count reported (not dropped)?
- [ ] `--fs` from header/config, not defaulted silently (`tk scan` injects it)?

---

## 11. Integration roadmap (tool is not done until the ledgers say so)

1. **Source**: `kain/core/frft_hunt.kn` (`pub fn frft_hunt_usage/_main`, `use _common::X`, no new shared helpers — shared candidates go to `_common.kn` with CANONICAL-CHOICE log entry).
2. **Verify**: `kain check kain/core/frft_hunt.kn` green (note: `converge` over `ptr` needs `build` — check will flag, build is the gate).
3. **Prove**: `kain build` from `kain/core/`, run `--prove` → 5/5, record receipt.
4. **Amalgamate**: `kain amalgamate --raw kain/core -o kain/core.kn` → `kain build kain/core.kn --target llvm -o core.exe` (side-by-side; `-o` is a file path).
5. **Dispatch**: row in `kain/core/dispatch.kn` (`frft` shorthand) + `core help frft` text.
6. **Orchestration**: `Tool(...)` row in `python/turbokain/registry.py`; add to `F32_DETECTORS` only after sky parity (drift/jerk cross-confirm on at least one injected + one sky slice).
7. **Ledgers**: `scripts/memlog.exe tool add "frft_hunt blueprint …" "docs/toolresearch/frft_hunt_guide.md"`; `catalog.tsv` row (`status=draft → builds → proven`, real prove receipt); `sky_catalog.tsv` battery extension on rows touched.
8. **Campaign**: MarkScript notebook `markscript/<date>_frft.md` with geometry table + RFI mask + inline verify fence; outputs always via `--out` into `reports/<run>/` (never bare in source dirs).
9. **v1.1 backlog**: resonate/patch trip + `FrftMirror` seal; AVX2 `cf32_chirp_mul` fast lane; cubic-phase extension (constant-jerk matched filter via FrFT peak-walk); IQ-native `slice --iq`; `waterfall` derotated-row overlay.

---

## 12. Worked sensitivity sketch (why coherent wins — honest version)

N = 2^20 @ fs ≈ 2.93 MHz → T ≈ 0.36 s. Chirp μ = 2000 Hz/s smears μT ≈ 716 Hz ≈ 2913 STFT bins at nfft=4096 (chan 715 Hz) — invisible incoherently below `z≈4`. FrFT at α* collects all N samples coherently: power-SNR gain ≈ N vs ≈N/2913 smeared → `z` gain ≈ √2913 ≈ 54× ideal, ≈ 5–15× after whitening losses (measured in P3, not theorized here). Sidereal μ = 0.1 Hz/s over the same T: smear 0.036 Hz ≪ bin — FrFT and FT tie (P4 asserts the tie goes to a=1 rather than minting a discovery).

Honest floor statement for v1.0: *"On 0.36 s L-band slices, FrFT recovers linear chirps ≥2× below the incoherent floor at matched false-alarm rate; at sidereal rates it ties the FT by construction."* Anything stronger needs chained stares (M3) and the P3 receipt.

---

## 13. References (build-order, not bibliography-spam)

- Ozaktas, Zalevsky & Kutay, *The Fractional Fourier Transform* (2001) — Ch. 6 discrete algorithms (the 3-stage decomposition).
- Pei & Ding, "Closed-form discrete fractional and affine Fourier transforms" (2000) — the sampling/normalization convention adopted here.
- Almeida, "The fractional Fourier transform and time-frequency representations" (1994) — chirp-detection identity §1.2.
- SetiYeti `python/scd_frf.py` (full SCD plane + dechirp bank) — the Python truth this lane must beat, then prove against.
- TurboKain `drift_hunt.kn` (incoherent baseline), `jerk_track.kn` (Viterbi + quad fit), `boxcar_bank.kn` (converge/whitener/prove mold), `lag_hunt.kn` (winsorize/local-unit/share lessons), `docs/kain/examples/sieve-pattern.kn` (the exe mold).

---

*End of `frft_hunt` guide · blueprint status · next action: scaffold `kain/core/frft_hunt.kn` §9.1–9.2, `kain check`, then fill `run_alpha_grid` behind the P1/P2 receipts.*
