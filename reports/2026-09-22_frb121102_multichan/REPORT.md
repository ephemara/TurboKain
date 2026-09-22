# 11.09 kHz Line Follow-up — 2026-09-22

Question: `fam_god` flagged a weak persistent Y2 line (bin 31 @11086.46 Hz,
p≈6e-4) in FRB121102 ch44 pol0. Instrument or sky? Protocol: multi-channel
coincidence + cross-polarisation agreement. A sky line repeats across chans
and pols; receiver-chain wander diverges in both (HIP-113357 lesson).

## Step 1a — adjacent coarse channels, same file, same α grid (8k SEG)

| chan/pol | top Y2 line | 11.09 kHz present? | verdict |
|---|---|---|---|
| ch30 p0 | bin 537 @192.0 kHz | no | CLEAN |
| ch43 p0 | bin 73 @26.1 kHz, p≈1e-4 | no | FAM-HIT (own family) |
| ch44 p0 | **bin 31 @11.09 kHz, p≈6e-4** | **yes (target)** | FAM-HIT |
| ch45 p0 | bin 39 @13.9 kHz | no | FAM-HIT (own family) |

The 11.09 kHz line appears NOWHERE else. Every channel carries its own
family of weak low-α lines at different frequencies — the intermod-thicket
signature (mixing products folding per-channel), C-band edition.

## Step 1b — cross-polarisation (same chan, other feed)

| chan/pol | 11.09 kHz present? | verdict |
|---|---|---|
| ch44 p1 | no (nearest bin 56 @20.0 kHz, p≈0.8 = noise) | CLEAN |

Polarisation-divergent: the textbook receiver-chain fingerprint. A sky signal
arrives in every feed at the same frequency; this arrives in one.

## Disposition

**RULED OUT as receiver-chain/intermod artifact**, with receipts:
1. not cross-channel (Step 1a),
2. not cross-polarisation (Step 1b).

No ON–OFF cadence needed for this line (dead on two filters already). Note:
no OFF leg exists on disk for scan 0011 — a future OFF would be a third nail
only if a line ever survives 1a+1b.

Tables: `god_ch{30,43,45,44p1}.md/csv`. Slices: `frb_ch{43,45}.f32` (full 128
blocks, ~2 s each). Parent data: `../2026-09-22_frb121102_full/`.
