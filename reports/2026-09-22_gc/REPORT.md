# GC REPORT — Sgr B2 + BLGCsurvey C07 (first Kain filterbank campaign)

Date: 2026-09-22. Tools: fil_reader (new, 4/4) + full battery.
Verdict: **honest negative with one instrumental square wave characterized six ways,
two tool bugs caught (one fixed live), one numerical false alarm quarantined.**
No candidate. No WATCH. Floor stated.

## 0. What the archive actually holds (preflight truth)

- **Zero raw voltages of the galactic center exist publicly.** GC survey
  (`BLGCSURVEY_CBAND_*`, 20 pointings) = filterbank-only, 200–680 GB/file.
  Sgr B2 (`DIAG_SGR_B2`, S-band) = HDF5-only, 6 files / 37 GB — all in
  `D:/data/gc/` (download completed, log `D:/data/tmp/sgrb2_dl.log`).
- Bootes void: nothing at any product level (BL points at stars; the void
  was never observed). No download possible. OFF pointings remain the
  empty-sky proxy.

## 1. Data in this report

| file | product | geometry | span |
|---|---|---|---|
| `gc_C07_sample.fil` | Sigproc .fil, C07 C-band | 1.7M chan × 279 spectra, tsamp 1.0737 s, fch1 8438.96 MHz | ~5 min |
| `...0013.gpuspec.0002.h5` | S-band Sgr B2 | 315392 chan × 55 spectra, tsamp 1.0737 s | 59 s |
| `...0013.gpuspec.8.0001.h5` | hi-time Sgr B2 | 2464 chan × 171008 spectra, tsamp 349.5 µs, fs 2861.02 Hz | 60 s |
| `...0014.gpuspec.0002.h5` | S-band Sgr B2 (+69 s) | 315392 chan × 558 spectra | ~10 min |
| `...0014.gpuspec.8.0001.h5` | hi-time Sgr B2 (+69 s) | 2464 chan × 1716224 spectra | ~10 min |
| `...0014.gpuspec.0000.h5` | ultra-fine Sgr B2 | 322M chan × 32 spectra, 2.79 Hz chans, 18.25 s | ~10 min |
| `...0013.gpuspec.0000.h5` | ultra-fine Sgr B2 | 322M chan × 3 spectra | ~1 min |

`.fil` → `.f32` via **fil_reader.kn (TurboKain 11, NEW)**:
prove 4/4 (f64 header decode, f32 roundtrip, u8/i16 encode, full
file roundtrip incl. header walk + chan extract exact).
C07 probe: `nchans=1703936 nspec=279 exact, fch1=8438.96, foff=-2861 Hz,
tsamp=1073741 us`, 0.049 s. Band-mean extract 1.9 GB in 11.6 s,
279/279 finite, mean 5.06e9 ±1% — header length confirmed by sanity
(no NaN/huge = no 4-byte offset error).
`.h5` → `.f32` via `_tmp/h5dump.py` (scratch bridge, gitignored, documented:
HDF5 container parsing is out of scope for a Kain lane; bitshuffle needs
`import hdf5plugin`; **gpuspec axis order is (time, feed, freq) despite
labels saying (freq, feed, time)** — verified against nchans).

## 2. FINDING: 25.00 Hz square wave, Sgr B2 scan 0013 (instrumental)

Six independent agreements on `sgrb2_0013b8_bandmean.f32` (171008 samples,
full-band mean over 2464 S-band channels):

| lane | result |
|---|---|
| python rfft (ground truth) | **25.00 Hz at 1.8M×median**, odd harmonics 75/125/175/225/275/325 (square signature) |
| fold_sum (fixed, --fs 2861) | DETECTED 25.00 Hz, σ 426025, subs f0/2../4 |
| frame_hunt dec=4 | DETECTED 25.00 Hz, σ 433958 |
| fam_god SEG=32768 | FAM-HIT, bins 286/573/859… = 24.97/50.03/75.0 Hz |
| xeno_scan | WATCH via LADDER 151 (comb) + SK-FLAG (4.7% deviant) |
| drift_hunt | 25 hits, ALL rate-0, freqs = f0+25k family (stationary) |
| bitslice→xvm (mag lane) | **XENO-CANDIDATE score 50** (CA/ACF/BM/raster/TAG all engage; sign/diff lanes correctly ENTROPY-BLOCK) |

Character: exact 25.00 Hz (df 0.0167), odd-harmonic square, FULL-BAND
(band-mean), stationary (zero drift). Attribution: **backend modulation —
chopper/cal-switching prime suspect** (square, exact-Hz, full-band,
square = switching). NOT sky. Grade I2 max, no WATCH, no candidate.
Coexisting exact tones: 19.53125 Hz family (x460), 50 Hz (x2088, even).

## 3. Non-persistence: scan 0014 (+69 s) is DIFFERENT

- 25.00 Hz collapses 1.8M× → x293. The square did NOT persist.
- 0014 is dominated by a 19.53125 Hz family (x11423) + 50 Hz (x5637) +
  12.5 Hz + a DC ramp (frame's highpass saw past it; raw spectrum is
  ramp-swamped to 0.04 Hz).
- Verdict: backend STATE CHANGED between scans (60 s timescale). Both
  families are full-band exact-Hz modulations = backend, twice over.

## 4. Tool bugs caught (the campaign paid for itself)

1. **fold_sum hardcoded FS (FIXED LIVE).** No `--fs` flag; `FS_HZ` const
   burned in. On 349 µs power data it decimated by 488 and mislabeled every
   Hz (first run reported "1585.87 Hz" — pure artifact of wrong decimation).
   Fix: `--fs` (default 2929687.5, voltage runs unaffected), dec=1 below
   ~6 kHz. Check green, rebuild green, rerun reports true 25.00 Hz.
   Lesson: every detector takes geometry from argv/config (M7) — no exceptions.
2. **frame_hunt decimation ghosts (DOCUMENTED, needs guard).** Default
   dec=512 on 0013b8 reported 377.83 ms (2.1 bins — decimation/block
   artifact, gone at dec=4). On 0014b8, top ranks 157.62/78.81 Hz have
   x0.1/x1.6 spectral energy (GHOSTS, σ>1000) while the real strongest line
   (50 Hz x5637) missed top-8. Frame finds families but misranks; σ is not
   comparable across lanes. Needs a spectral-crosscheck guard.
3. **boxcar_bank quantized-MAD blowup (QUARANTINED, guard G5 proposed).**
   `sgrb2_0014b8_ch1363` reported SHOT 149σ w1→20σ w128 (all widths fire,
   decreasing with width). Raw data at t=39181: values 30–35, z≤2 — NOTHING
   THERE. Repro: 6-level quantized ramp fires 23.6σ; flat constant is CLEAN.
   Mechanism: periodic-quantized data nulls a sub-band → near-zero MAD →
   division blowup (same family as xeno's unfloored-ladder 1332, already
   guarded there). Voltage-regime results (FRB, proves) use continuous
   floats and are UNAFFECTED. Required: MAD floor before robust-z (G5).

## 5. Ultra-fine census (322M chans, 2.79 Hz — narrowband territory)

`sgrb2_0014big_census.csv`: 308× 1M-chan blocks, mean/max/std + top-3 peaks.
Bandpass falls 5.39e9 → 1.13e9 across 2720→1818 MHz; EVERY block holds
~5.7e13–1.1e14 spikes (S-band RFI forest toward the GC, or railed backend
values — flagged, not claimed). 32-sample bandmean smooth (±0.3%).
Narrowband tone search across 322M channels needs a spectral-census lane
(top-K per spectrum + persistence across the 32) — NOT YET BUILT, recorded
as the next detector after veto/frame follow-ups.

## 6. C07 floor (coarse stare, N=279)

frame_hunt dec=1: undetected, best 25.35σ vs 40σ gate (periods to ~150 s).
sk/fold/fam/drift/xeno/boxcar REQUIRE N≥4096 (boxcar: nt≥256; fold: band
nonempty; all refuse or degenerate below) — recorded NOT-RUN with reason,
not forced. bitslice→xvm on 279 smooth samples: correctly ENTROPY-BLOCK.
Coverage: one 5-min C-band pointing, full-band mean + 5 spot channels.

## 7. Regime floors earned tonight (for the next campaign)

- Detectors (except frame) need N≥4096 samples; fold needs fs≳2 Hz f0-band.
- fold_sum Hz labels are only valid with runtime --fs (fixed).
- frame_hunt default dec blinds fast rhythms AND hallucinates near 2-bin
  periods — always run dec ladder (e.g. 512 + 4) + spectral crosscheck.
- boxcar_bank on quantized integer power data can blow up via zero-MAD —
  require G5 MAD floor; voltage floats unaffected.
- gpuspec h5: import hdf5plugin (bitshuffle); axes (time, feed, freq).

## 8. Files (all in this dir)

bandmeans + spots (.f32), per-tool md/csv, `sgrb2_0014big_census.csv`,
metas. H5→f32 bridge: `_tmp/h5dump.py`, `_tmp/h5census.py` (scratch).
Fil lane: `kain/core/fil_reader.kn` (committed). Fold fix: `kain/core/fold_sum.kn`.
