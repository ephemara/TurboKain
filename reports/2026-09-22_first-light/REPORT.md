# First Light — 2026-09-22

First end-to-end TurboKain campaign: one ON/OFF pair through all four tools,
no Python in any hot path. TRAPPIST-1, blc04, L-band 1407.7 MHz, chan 44,
pol 0, blocks 0–6 (~1.2 s per leg).

## Inputs

| leg | file | size |
|---|---|---|
| ON 0015 | `blc04_guppi_57807_75725_DIAG_TRAPPIST1_0015.0000.PART1GB.raw` | 1 GiB, 7 blocks |
| OFF 0016 | `blc04_guppi_57807_75805_DIAG_TRAPPIST1_OFF_0016.0000.PART1GB.raw` | 1 GiB, 7 blocks |

Sliced with `slice 0.3.0` (chan 44, pol 0, 7 blocks): 3,670,016 samples/leg,
14.68 MB `.f32` each. Slice bytes are `cmp`-identical to `c/seti_slice`.

## Results

| tool | ON | OFF |
|---|---|---|
| `sk_gate` SK | skdev 0.792, frac 0.0004, **CLEAN** | skdev 1.073, frac 0.0004, **CLEAN** |
| `boxcar_bank` pulse | best 11.96σ (DM 419, w1), **CLEAN** | best 11.41σ (DM 484, w1), **CLEAN** |
| `fold_sum` period | 1564.98 Hz @6.65σ, undetected | 570.88 Hz @7.82σ, undetected |

Full tables: `sk_{on,off}.md`, `pulse_{on,off}.md` (256-row DM×width grids),
`fold_{on,off}.md` (top-8). CSV mirrors alongside every md.

## Cadence read

Nothing persists ON-only at I2: SK quiet both legs, pulse tops sub-threshold
both legs (14σ gate), fold tops differ per leg (1565 vs 571 Hz) and both sit
far below the 16σ gate. **No WATCH. No candidate.** This is an honest negative:
here is the floor (SK frac 4e-4, pulse 12σ max, fold 8σ max), here is the
coverage (1 chan × 1 pol × 7 blocks × 2 legs).

## Timings (dev lane, warm)

| step | ON | OFF |
|---|---|---|
| slice 7 blocks | 0.76 s | 0.32 s |
| sk_gate 512 segs | 0.16 s | 0.16 s |
| boxcar_bank | 0.5 s | 0.5 s |
| fold_sum | 2.4 s | 2.4 s |

Whole campaign: single-digit seconds per leg. Every tool exit 0 with
`receipt=PASS`.

## Tool versions

`slice 0.3.0` (kernel32 IO + unpack lane) · `sk_gate 0.1.0` · `boxcar_bank`
(user build, `--prove` 3/3) · `fold_sum 0.1.0` (share/fanout harmonic grid).

## Next

Wider chan sweep on this pair, `--start` depth on full 128-block files,
`cadence_pair` promotion to core, Wave-2 dispatch (`fam_scan`, `comb_scan`,
`vm_sandbox`).
