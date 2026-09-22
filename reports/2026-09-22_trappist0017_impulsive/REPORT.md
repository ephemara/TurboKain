# TRAPPIST-1 0017 — Impulsive Structure: Full Report

**Date:** 2026-09-22 · **Instrument:** GBT / GUPPI · **Target:** TRAPPIST-1 (DIAG_TRAPPIST1)
**Pipeline:** TurboKain (pure Kain, no Python in the hot path)
**Status:** **INSTRUMENTAL ARTIFACT** (settled by diagnostic battery §6.6) ·
**Confidence in existence:** very high · **Confidence in attribution:** high (instrumental)

---

## 1. TL;DR

While running the first full-archive sweep, the `xeno_scan` corroboration lattice
fired **SK+IMP (XENO-STRONG)** on coarse channels 60 and 63 of TRAPPIST-1 scan
0017. The signal is a real, strong, **stationary impulsive process** — present in
every one of the 128 blocks of the observation, with a heavy-tailed amplitude
distribution ~10¹⁹× the Gaussian expectation. It is:

- **present** in scan 0017 at 1407.7 MHz (blc04, two files) **and** 2157.7 MHz (blc00),
- **absent** in scan 0015 (ON, 1407.7 MHz), scan 0016 (OFF), and 1970.2 MHz (blc01),
- **partially present** in scan 0018 (OFF, 1407.7 MHz, ch63 only).

It is **not periodic** (not a pulsar), **not phase-locked to the sample clock**
(not ADC interleaving), and **not block-boundary clustered** (not a simple
data-acquisition glitch).

**It has since been resolved as an instrumental artifact** (§6.6): a diagnostic
battery confirmed a **fs/2048 frame-clock comb** in the cyclic ladder, a
**cross-bank channel-index duplication**, a **PFB band-edge rolloff** profile, and
**common-mode structure across all four polarisation products**. No test produced
an astrophysical signature. See §6.5–6.6 for the astrophysical case and its
disproof, and §6.6.2 for the four new automated guards this earned.

---

## 2. How the pipeline caught it (the receipt chain)

Full-archive sweep (`reports/2026-09-22_fullsweep/`), one lane =
file × coarse-channel × pol0 × all 128 blocks × six detectors.

```
slice ch60 (full 128 blocks, 67,108,864 samples, 22.9 s)
  -> sk_gate           skflag=1  skfrac 25.69%  (>=2% gate; 12x over)
  -> xeno_scan         skflag=1, impuls=1  -> lattice SK+IMP -> XENO-STRONG
  -> fam_god           cyclic lines, Y2 ratio 316x @ 143.05 Hz
  -> fold_sum          detected (envelope periodicity in the 5-6 Hz family)
  -> boxcar_bank       (no dispersed single-pulse signature)
```

Trigger tables (`evidence/tables/`):
`ch60p0_s0017_xeno.md`, `ch63p0_s0017_xeno.md`, `ch60p0_s0017_fam.md`,
`ch63p0_s0017_fam.md`, `ch60p0_s0017_sk.md`.

The trigger line (xeno, self-documenting column headers):

```
| file | samples | skdev_x1000 | skfrac_x10000 | skflag | coh_x100 | cohflag | ladder_x100 | ladderq | dm_sign | dm_r2_x1000 | impuls | maxz_x10 | kurt_x100 | tailx_x100 | lattice | verdict |
| ...ch60... | 67108864 | 8152 | 2569 | 1 | 132 | 0 | 511 | 0 | +0 | 280 | 1 | 311 | 3574 | 442 | SK+IMP | XENO-STRONG |
```

`skdev=8152` (>8), `skfrac=25.69%` (12× the 2% gate), `impuls=1`, `maxz=31.1σ`,
`kurt=35.74`. Two independent markers corroborated; the lattice promoted it.

---

## 3. Measurements

All figures reproduced by `evidence/scripts/analyze.py` from the `.f32` slices in
`evidence/slices/`. Full tables: `evidence/measurements.tsv`,
`evidence/persistence_per_block.tsv`, `evidence/value_histograms.tsv`.

### 3.1 Primary presence matrix — channel 60, 1407.7 MHz (blc04)

| observation | scan | distinct | sd | kurtosis | spikes>10σ | rate | blocks hit |
|---|---|---|---|---|---|---|---|
| **ON 0017** | 0017 | 256 | 4.243 | **59.80** | **17,719** | 773/s | **128/128** |
| ON 0017 (.0001) | 0017 | 256 | 4.186 | **52.98** | 14,815 | 647/s | **128/128** |
| ON 0015 | 0015 | 46 | 3.875 | **0.00** | **0** | 0/s | 0/128 |
| OFF 0016 | 0016 | 43 | 3.745 | **−0.00** | **0** | 0/s | 0/128 |
| OFF 0018 | 0018 | 162 | 3.757 | **0.35** | 157 | 6.9/s | 14/128 |

### 3.2 Multi-band — channel 60 in other banks (same scan 0017)

| bank | freq (MHz) | distinct | sd | kurtosis | spikes | blocks hit |
|---|---|---|---|---|---|---|
| blc04 | 1407.7 | 256 | 4.243 | **59.80** | 17,719 | 128/128 |
| blc00 | 2157.7 | 256 | 1.700 | **1360.79** | 12,720 | 64/128 |
| blc01 | 1970.2 | 256 | 16.904 | 3.05 | **0** | 0/128 |

### 3.3 Channel 63, 1407.7 MHz (blc04)

| observation | distinct | sd | kurtosis | spikes | blocks hit |
|---|---|---|---|---|---|
| ON 0017 | 256 | 2.433 | **70.97** | 3,438 | 105/128 |
| ON 0017 (.0001) | 256 | 2.403 | **50.22** | 2,079 | 80/128 |
| ON 0015 | 30 | 2.314 | −0.00 | **0** | 0/128 |
| OFF 0016 | 97 | 2.243 | 2.08 | 71 | 7/128 |
| OFF 0018 | 239 | 2.263 | **27.68** | 924 | 66/128 |
| ON 0017 blc00 | 255 | 1.322 | 386.14 | 1,527 | 52/128 |
| ON 0017 blc01 | 256 | 17.710 | 2.51 | **0** | 0/128 |

### 3.4 Amplitude anatomy (blc04 ch60, 0017 ON)

- 67,108,864 samples; Gaussian-like core (top values 0, ±1, ±2 … at ~9-10% each)
- Fraction |z|>4: 0.039% (Gaussian 6.3e-5 → 620×)
- Fraction |z|>10: 2.64e-4 (Gaussian 1.5e-23 → **~10¹⁹×**)
- Bursts: 1,653 groups, ~10.7 spikes each (median 5, max 79), burst rate 72.2/s

---

## 4. Mechanism tests

| # | Test | Method | Result | Conclusion |
|---|---|---|---|---|
| 1 | **Periodic?** | FFT of burst-centre impulse train, 1–5000 Hz | flat; top peaks ≈ noise floor | **Not a pulsar.** No rotation/periodicity |
| 2 | **ADC interleaving?** | spike sample-index mod 8 distribution, χ² (7 dof) | χ²=1.43 (uniform) | **Not interleaving.** Spikes randomly phased |
| 3 | **Block-boundary glitch?** | spike position within 524,288-sample block, 10 deciles | ≤11.9% per decile; 4.8% within 2% of edge (uniform 4%) | **Not a boundary artifact.** Uniform within blocks |
| 4 | **Stationary?** | per-block max-z over 128 blocks | 128/128 blocks with max-z>20 (clamped ~30.1) | **Stationary, continuous** across 22.9 s |
| 5 | **ON/OFF?** | compare 0017 ON vs 0018 OFF, same chan | 773/s → 6.9/s (112×) | Present ON, near-absent OFF — but 0015 ON also quiet (see 7) |
| 6 | **Frequency-selective?** | compare banks | blc04+blc00 yes, blc01 no | Band-selective |
| 7 | **Recurrent?** | 0015 ON (earlier, same band) | kurt 0.00, 0 spikes | **Not recurrent** — 0017-only in ch60 |

---

## 5. Epoch signature (context)

The digitizer response differs sharply between epochs:

| epoch | scans | distinct values (ch60) |
|---|---|---|
| MJD 57807 early | 0015 ON, 0016 OFF | **43–46** (coarse) |
| MJD 57807 later | 0017 ON, 0018 OFF | **162–256** (fine) |

The impulsive structure appears only in the **later, finer-response** epoch, and
0017 is independently known-abnormal: SetiYeti's `runs/vm_hunt/REPORT.md` records
0017 as having *2× the dark lanes of 0015* and 31+ FAM-HITs vs 1–2 in 0015
("TRAPPIST 0017 is on fire"). Two independent pipelines agree the observation
is anomalous.

---

## 6. Interpretation (confidence-graded)

| hypothesis | verdict | evidence for | evidence against |
|---|---|---|---|
| **Impulsive RFI during 0017** | **favoured** | present in 0017 only; multi-band; band-selective; no recurrence | would need a source at 1.4 AND 2.16 GHz but not 1.97 |
| Backend/digitizer transient in 0017 | plausible | epoch response change; 0017 known-abnormal; 0018 OFF shares ch63 | blc01 quiet at 1.97 GHz in same observation |
| Genuine astrophysical impulsive source | cannot exclude | stationary, strong, multi-band | no periodicity; absent in 0015 & 0018 (ch60) |
| ADC interleaving / boundary glitch | **excluded** | — | tests 2, 3 |
| Pulsar / rotating source | **excluded** | — | test 1 |

**Noise-matched context:** the 10σ tail excess is ~10¹⁹× Gaussian. This is not
noise, and it is not any mode in our catalogue. It is a real signal of
non-astrophysical or unexplained origin that requires the follow-up in §8.

---

## 6.5 Could this be a new astrophysical phenomenon?

This is the interesting question, and the answer is: **plausible, not excluded,
and worth the follow-up that would settle it.** Laid out honestly.

### 6.5.1 Why a stellar-physics origin is genuinely plausible

TRAPPIST-1 is an **M8 dwarf — a known, active flare star**, and it is a
well-established target for radio star–planet-interaction and flaring studies.
Active M dwarfs produce **coherent (electron-cyclotron-maser) and
gyrosynchrotron radio bursts** from magnetic reconnection in flares. Those
bursts are impulsive, stochastic (not periodic), and can last tens of seconds.
That is — at face value — what we measure.

Our signal's character actually *fits* that mechanism well:

| property measured | flare/ECMI expectation |
|---|---|
| impulsive, high kurtosis | yes — coherent emission is bursty |
| non-periodic | yes — flares are stochastic, not rotational |
| stationary over ~23 s | yes — a long-duration flare/activity episode |
| broadband across 1.4–2.16 GHz | possible for gyrosynchrotron |
| seen in one observation only | yes — activity is time-variable |
| ON-target, weaker/absent OFF | yes — should follow the source |

### 6.5.2 Why a local origin is still more likely

| property measured | local-artifact reading |
|---|---|
| **kurtosis rises toward the band edge** (ch57 0.3 → ch60 59.8 → ch63 71) | **band-edge / passband-rolloff / aliasing** — a classic instrumental pattern |
| appears only in scan 0017 | backend/digitizer state; 0017 is independently known-abnormal |
| 0018 OFF ch63 partially shares it (kurt 27.7) | argues against a purely target-locked source |
| no cross-polarisation or repeat test yet | the standard sky-vs-local discriminators are unrun |
| 1407.7 **and** 2157.7 MHz but not 1970.2 MHz | clumpy, not a smooth physical spectrum |

### 6.5.3 Honest plausibility (judgement, not measurement)

These are **not** computed probabilities — they are a reasoned weighting of the
evidence above, and should be read as such:

| origin | rough plausibility | decisive test that settles it |
|---|---|---|
| Local RFI / backend transient / band-edge | **~70%** | polarisation + ON-OFF-ON |
| Known astrophysical (M-dwarf flare / ECMI radio burst) | **~25%** | polarisation (ECMI is ~100% circular), cross-band coherence |
| **Genuinely novel astrophysical phenomenon** | **~5%** | exclusion of the above two, plus repeat detection |

The ~5% is real but small, and it is **not** a technosignature number — see §7.
Even the ~25% "astrophysical" case would be an interesting *stellar radio burst*
result (e.g. a bright coherent burst from TRAPPIST-1), not evidence of
technology.

### 6.5.4 The single most decisive test

**Polarisation.** Electron-cyclotron-maser emission is up to ~100% circularly
polarised with a fixed handedness; band-edge and interleave artifacts have a
signature tied to the digitiser, not to the sky. Running **pols 1–3 on ch60/63**
would separate these cleanly in one pass and is the highest-value follow-up.
Second: **ON-OFF-ON within a single epoch**, which removes the
scan-to-scan backend-state confound that currently prevents any sky claim.

### 6.5.5 The critical caveat

Even if every local explanation is excluded and this proves astrophysical, it
is **not** the thing the mission is hunting. Traffic is noise-like and
continuous; monuments repeat on a cycle; payloads are coded. An impulsive
stellar burst is **none of those** — it would be a bona-fide astrophysical
discovery, but not a technosignature. Both facts can be true at once, and we
should report it either way.

---

## 6.6 DIAGNOSTIC BATTERY — three instrumental contradictions, settled

Three independent instrumental signatures were predicted, tested, and **all
three confirmed**. The astrophysical case (§6.5) does not survive.

### C1 — fs/2048 frame-clock comb — **CONFIRMED**

The cyclic peaks in `ch60p0_s0017_fam.md` at SEG=8192 sit on an exact
grid: **the 11 strongest peaks (ranks 0–10) fall at bins 3, 7, 11, 15, 19,
23, 27, 31, 35, 39, 43** — ten consecutive diffs of **4 bins**. Bin width at
SEG=8192 is fs/8192 = 357.628 Hz, so the spacing is 4 × 357.628 =
**1430.51 Hz = fs/2048 exactly** (2,929,687.5 / 2048 = 1430.5115).
This is the channelizer frame clock (2048 samples), not sky. **The `fam_god`
"cyclic detection" is a clock comb.** (A few NMS-tail rows sit off-grid — the
guard uses the *modal* diff, not every diff.)

### C2 — cross-bank channel-index duplication — **CONFIRMED**

The impulsive structure concentrates on the *same channel indices* (60, 62, 63)
in blc04 (1407.7 MHz) and blc00 (2157.7 MHz) — two independent GUPPI compute
nodes 750 MHz apart — while blc01 (1970.2 MHz) is flat. A natural emitter does
not track channel index across independent backends; a per-node filterbank
defect does.

### C3 — filterbank rolloff profile — **CONFIRMED**

Kurtosis rises monotonically toward the sub-band edge:

| chan | 57 | 58 | 59 | 60 | 61* | 62 | 63 |
|---|---|---|---|---|---|---|---|
| kurtosis | 0.26 | 1.02 | 4.36 | 59.80 | 0.20 | 36.55 | 70.97 |

(*ch61 is a degraded lane, distinct=141 — structure masked.) This is the
passband-rolloff / aliasing signature of the polyphase filterbank at the band
edge, NOT a physical spectrum. See `evidence/channel_map_0017.tsv`.

### Step 1 — Polarimetric Stokes extraction (the decisive test) — **RUN**

| product | distinct | sd | kurtosis | spikes>10σ |
|---|---|---|---|---|
| pol0 | 256 | 4.243 | **59.80** | 17719 |
| pol1 | 256 | 4.240 | **58.91** | 17609 |
| pol2 | 256 | 5.785 | **18.81** | 14871 |
| pol3 | 256 | 5.787 | **18.79** | 14969 |

All four recorded streams are impulsive; pol0≈pol1 and pol2≈pol3. Stokes
products (I=XX+YY, Q=XX−YY, U=2·Re, V=2·Im): |mean|/sd is ~0.17 for I and
~0.09 for U and V — **no large circular polarisation**.

**Verdict (decision matrix row 2): common-mode across polarisations, Stokes V≈0
→ terrestrial/interference ingress or backend, NOT a hardware single-rail
failure (pol1 is not quiet) and NOT coherent circular ECME (no |V/I|>0.8).**

### Step 2 — band-center PFB control (ch32) — **RUN**

| chan | kurtosis | spikes>10σ |
|---|---|---|
| ch32 (band centre) | **0.02** | **0** |
| ch60 (edge) | 59.80 | 17719 |

**Verdict: PFB rolloff artifact.** Band centre is perfectly quiet; only the edge
channels are impulsive. This is edge-channel leakage/aliasing, not a source.

### Step 3 — GUPPI packet continuity — **RUN**

`PKTIDX` increments **sequentially** by 16384 across headers (0, 16384, 32768,
49152 …). `DROPBLK = 0` and `DROPTOT = 0` for every block after block 0 (which
logged a negligible DROPTOT = 0.451 of one packet). **`DROPMARK`: 0 matches.**

**Verdict: no socket underrun.** The Dirac-edge-step hypothesis is excluded.

---

### 6.6.1 FINAL DISPOSITION

**INSTRUMENTAL ARTIFACT — PFB band-edge rolloff modulated by the fs/2048 frame
clock, common-mode across all four polarisation products, present in the
abnormal 0017 backend state.**

All three of the predicted contradictions were confirmed, all four battery
steps behaved as the instrumental hypothesis requires, and **no test produced
the astrophysical signature**. The §6.5 plausibility weights are superseded by
direct measurement: local/instrumental ~1.0, astrophysical ~0.

**This is not a new astrophysical phenomenon, and it is not a technosignature.**
All slices, tables and the battery output are retained in `evidence/` so the
kill is reproducible and auditable.

### 6.6.2 What this earns us (the real result)

A **new named artifact mode + four automated guards**, all with receipts:

1. **fs/2048 comb detector** — any fam_god alpha ladder whose peaks sit on a
   fs/2^k grid is a frame-clock comb → auto-discount.
2. **Band-edge guard** — flag kurtosis that rises monotonically toward the
   sub-band edge (PFB rolloff).
3. **Cross-bank index guard** — the same channel index spiking in independent
   banks is a per-node defect, not a source.
4. **Polarisation-front-end triage** — all-pols-spiky + V≈0 → common-mode
   ingress; single-pol-spiky → hardware rail failure.

These are the concrete calibration deliverables; the sweep, the report, and this
battery all reduce to "three guards we did not have yesterday, each with a
receipt."

**Implemented.** The three guards now live in one place, `kain/pipeline/`
(`guards.kn`), wrapped by a single entry point (`main.kn`, Kain use-modules):

```
pipeline file <raw> --chan-lo 57 --chan-hi 63 --pols 0 --work DIR
pipeline analyze <workdir>
```

Re-running the 0017 case through it downgrades the detector's XENO-STRONG to
ARTIFACT-COMMON (G4 pol triage), ARTIFACT-EDGE (G3 rolloff) and ARTIFACT-COMB
(G1 frame clock) automatically -- the kill is now mechanical, not manual. Guard
unit proof: 6/6 (3 positive + 3 negative controls).

---

## 7. Why this is not a candidate (yet)

Per `INTERSTELLAR_HIT_CRITERIA.md`, a candidate needs **persistence +
sky markers + independence**. This event fails:

- **No persistence across epochs** (0015 ON, same band, is perfectly quiet),
- **No ON-OFF-ON** in a single epoch (0017 ON vs 0018 OFF are different scans),
- **No periodicity, no dispersion, no coded structure**,
- **Polarisation untested** (pol0 only), **other channels only partly mapped**.

It is filed as a **new named mode** (`impulsive-0017`) to guarantee it is
re-scored rather than auto-vetoed in future sweeps.

---

## 8. Follow-ups (priority)

1. **ON-OFF-ON in a single epoch** — the only test that separates scan-state from sky.
2. **Polarisation** — run pols 1–3 on ch60/ch63; a sky/RFI source vs a backend
   artifact separate cleanly in cross-pol.
3. **Full channel map of 0017** — where exactly in frequency does it sit? (ch59
   quiet, ch60/62/63 spiky, ch61 quiet — is there a comb?)
4. **Recurrence query** — every 0017 bank + every other TRAPPIST epoch for the
   same impulsive signature (the journals already carry the peaks).
5. **Inject a matched decaying impulse train** through `xeno_scan` to confirm the
   SK+IMP lattice fires as a matter of sensitivity, not accident.

---

## 9. Reproduce

```bash
# 1. extract slices (slice.exe, kernel32 arena IO)
cd kain/core
slice.exe "E:/SetiYeti/data/blc04_guppi_57807_75885_DIAG_TRAPPIST1_0017.0000.raw" 60 <out>/on0017_blc04_0000_ch60.f32 128 --pol 0
# ... (all slice commands are recorded in evidence/slices/*.slice.log)

# 2. measurements + tables
python3 evidence/scripts/analyze.py evidence/slices evidence
```

## 10. Provenance

| artifact | path |
|---|---|
| trigger tables | `evidence/tables/` |
| measurements | `evidence/measurements.tsv` |
| per-block persistence | `evidence/persistence_per_block.tsv` |
| value histograms | `evidence/value_histograms.tsv` |
| `.f32` slices (256 MB each) | `evidence/slices/` |
| slice logs | `evidence/slices/*.slice.log` |
| analysis script | `evidence/scripts/analyze.py` |
| parent sweep | `../2026-09-22_fullsweep/` |
| independent confirmation | `E:/SetiYeti/runs/vm_hunt/REPORT.md` (§3.1) |

**Tools:** slice 0.3.0 · sk_gate 0.1.0 · xeno_scan 0.1.0 · fam_god 0.5.0 · boxcar_bank 0.1.1 · fold_sum 0.1.0 · cadence_pair 0.2.0
