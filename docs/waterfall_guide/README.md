# Waterfall Field Manual — learning specimens (synthetic, pipeline-accurate)

Seven voltage-level synthetics rendered through the real `waterfall` engine
(fs = 2929687.5 Hz, N = 8388608 ≈ 2.86 s, fcenter 1500.0 MHz, turbo).
Pure Gaussian noise + injected features. Nothing here is sky — everything here
is exactly what the label says, which makes these the answer key for training
your eyes (and any LLM) before touching real data.

How to use: open a PNG, cover the right column + badges, write down every
feature you see with freq/drift/time/strength, then uncover and check.
The right column + peak badges are renderer-computed from the file, so they
are fair answer keys for *these* specimens. (On real sky, demand the OFF leg
before believing any badge — single-beam badges are screening, not verdicts.)

## The specimens

### g0_control — pure noise. THE most important image here.
Recipe: unit Gaussian, nothing injected.
See: flat spectrum (peak margin only +0.7 dB — noise breathes this hard),
featureless waterfall, ragged envelope ~22–24 dB, SK hugging 1.0.
Hit log reads NO DETECTIONS. Memorize this texture: every other image is
"this, plus something." Note the renderer still flags 56 bins (5.4%) on pure
noise — excision has a false-positive floor, and flagged ≠ RFI. Note the
faint dotted verticals: present with zero signals injected, so dotted lines
alone never constitute a detection.

### g1_stationary — loud carrier, zero drift. The RFI archetype.
Recipe: 3.0-amplitude tone at 600 kHz baseband, no drift.
See: razor line full height in panel 2, tall spike in panel 1, SK dip
exactly on the line, envelope flat (no time structure).
Watch out: the line appears TWICE (mirror image — real-valued input FFT
symmetry; every tone has a twin equidistant from band center). Not two
signals. Terrestrial carriers look exactly like this, which is why
"stationary line" alone is never interesting — persistence across ON/OFF is.

### g2_drifter — fast linear chirp. The classic candidate SHAPE.
Recipe: 3.0-amplitude tone, +6000 Hz/s over 2.86 s (~17 kHz walk).
See: peak badge +17 dB, hit log reports drift −6661.3 Hz/s. Two lessons:
(a) the slant is barely visible — 17 kHz across a 2.9 MHz span is ~7 px.
Eyeballs cannot do drift search; that is what `drift_hunt` (dedoppler
integration) is for. Real ET-like drifts (Hz/s, not kHz/s) are utterly
invisible here. (b) Injected +6000, reported −6661: sign flips and ~11%
magnitude error. The overview estimator is coarse and mirror-confused —
treat badge drift as "slanted, roughly this fast," never as measurement.

### g3_burst — brief wideband impulse. A time-domain creature.
Recipe: ×6 noise burst over 2% of samples (~60 ms).
See: horizontal orange band across ALL freqs in panel 2, square top-hat
step in the envelope (panel 3), flat spectrum (energy spread thin per bin),
SK mostly quiet (impulse is brief in time, not narrow in freq).
Watch out: the exact inverse of a tone. Cross-panel rule: band-wide +
envelope step = burst (radar, discharge, buffer glitch). Narrow + flat
envelope = carrier. Confusing them is the beginner error.

### g4_jerk — accelerating chirp (quadratic phase). The curve.
Recipe: 3.0 tone, drift rate itself ramping (jerk term bends it ~20 kHz).
See: badge fits a straight line (+6661.3 Hz/s) through a bent line — the
curve is nearly invisible at this scale, and the linear fit wins anyway.
Watch out: orbital/accelerating transmitters curve; linear dedoppler smears
them. That residual is `jerk_track` (Viterbi) territory. If a line looks
straight but drift search underperforms its SNR, suspect curvature.

### g5_forest — six carriers (RFI inferno, miniature).
Recipe: six 1.5-amplitude tones spread across baseband.
See: a picket fence (×2 with mirrors = twelve lines), SK dipping at every
line, flagged-bin count jumps. This is what L-band looks like near
civilization. Watch out: forests breed false harmonics — check integer
frequency ratios before counting "multiple signals." And the loudest line
is not the most interesting; the one surviving ON−OFF is.

### g6_faint — the threshold lesson. READ THIS ONE TWICE.
Recipe: tone at amplitude 0.25 — one quarter of the noise per sample.
See: badge +11.3 dB, clear line, SK dip. A signal 4× WEAKER than noise is
blindingly obvious after 2.86 s of integration. Faint at the antenna is
not faint after the STFT. True marginality lives far below what intuition
suggests — which is exactly why formal gates (8–10σ, trials-corrected) and
`stack` (√N gain across epochs) exist instead of eyeball thresholds.
Also note the file's own contradiction, kept honest: hit log rows say
CANDIDATE while disposition reads NOMINAL/CLEAN — badge logic and
instrument rows are being rewired to a single verdict path. Never cite a
badge without naming which row produced it.

## Universal watch-outs (tape to monitor)
1. Every tone has a mirror twin. Count signals accordingly.
2. Sub-bin drift reads as zero. "drift=0.0" means "unresolved," not "still."
3. Badge drift is ±10%-ish and sign-unreliable. Measurement lives in the
   detector tables, not the overlay.
4. Flagged bins and dotted lines appear on pure noise. They are hygiene,
   not evidence.
5. Envelope flat + line = carrier. Envelope step + band-wide stripe =
   burst. Never swap them.
6. +1 dB peaks are weather, not signals. The control proves it (+0.7 dB).
7. No OFF leg, no claim. All seven specimens are single-beam by
   construction — including the pretty ones.
