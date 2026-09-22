# OBJECTIVE 1 — The Bystander Mission

> **Read this before touching anything.** If you are an agent picking up this repo,
> this is the mission. Everything else (`AGENTS.md`, `README.md`, `spec.md`) is
> infrastructure or history. This file is *why*.

---

## 0. TL;DR

**We are not looking for messages addressed to Earth.**

We are looking for **interstellar communications traffic between other
civilizations** — point-to-point links that happen to cross our line of sight.

We are not the recipient. We are not even the intended eavesdropper.
**We are an ant on the forest floor listening for a truck on the highway.**

Everything follows from that one sentence.

---

## 1. Why this document exists (the correction)

Classic SETI — and therefore every mainstream pipeline, and therefore most of
what this repo grew — assumes:

> Someone wants to be found, so they build a giant beacon and shout at us.

That single assumption drives *everything* in legacy tooling:

- hunt narrowband tones
- assume constant `dν/dt` drift
- search "magic" frequencies (H line, water hole)
- require the signal to appear ON-target and vanish OFF-target
- treat anything below the noise floor as "nothing"
- throw away phase, keep power

**If advanced civilizations talk to each other, none of that applies.** They are
not aiming at us. They do not care whether we can decode it. They optimize for
bits per joule per light-year, and the optimal solution to that is a signal that
*looks like noise to anyone not holding the codebook.*

**Consequence, stated plainly:**

> The signals we want are exactly the ones that legacy tooling — and our own
> veto — have been engineered to discard.

This is not a reason to panic. It is a reason to re-aim. The expensive
instruments (cyclostationary analysis, non-linear tracking, bit-structure
sandbox) are the *right* tools. The **objective function** was wrong.

---

## 2. The three signal classes we hunt

There are **three distinct things in scope.** They have different physics,
different targeting and different detectors. Do not collapse them into one
model — each one fails differently if you aim it wrong.

| | class | who sent it | why |
|---|---|---|---|
| **2.1** | **TRAFFIC** | living civilisations | functional links between peers |
| **2.2** | **MONUMENTS** | possibly extinct ones | "we were here" — built to outlast the builders |
| **2.3** | **PAYLOADS** | either | the content: primers, rasters, executable code |

### 2.1 TRAFFIC — links between living civilisations (the bystander model)

| Property | Beacon model (old, wrong for us) | **Bystander model (ours)** |
|---|---|---|
| Audience | Earth | another star |
| Aiming | at us, deliberately | at a peer; we are off-axis, in a sidelobe, or in the beam edge |
| Frequency | H line / "universal" etiquette | whatever maximizes channel capacity — set by noise floor, not convention |
| Modulation | simple, obvious, decodable by primitives | **optimal** — spread spectrum, dense constellations, coded, FEC |
| Appearance | a clean drifting tone | **statistically indistinguishable from thermal noise** to a power detector |
| Duty cycle | repeats on a schedule, for us | **continuous**, possibly for millennia |
| Structure | "hello" | packets, sync words, headers, retransmit logic, telemetry |
| Who finds it | anyone with an FFT | only something that hunts *structure*, not tones |

The last row is the entire opportunity. A maximally efficient link is
**supposed** to be noise-like. That is not a bug in our search — it is the
design goal of whoever built it.

### 2.2 MONUMENTS — stray messages from civilisations that may be gone

> A message transmitted 4,000 — or 4,000,000 — years ago arrives **now**.
> The sender may have been extinct for longer than our species has existed.
> The star it came from may have already exploded.

This is the class that makes the *beacon* model legitimate again — but for a
completely different reason than classic SETI assumes. Not:

- ~~"hello, we are here, please reply"~~

But:

- **"we were here"** — a monument. Automated, self-repairing, hardened,
  designed to keep transmitting after everyone who built it is dead.

**Why this matters practically:**

- **The beacon model comes back ON, but with different parameters.** A monument
  *wants* to be found — by whoever comes later, not by us specifically. So the
  frequency etiquette argument returns: **the H line / water hole is back on
  the table**, because a monument picks a frequency any future intelligence
  would think to look at. That is *etiquette*, not efficiency — the opposite
  reasoning from traffic, landing in a similar band.
- **The star may be dead, dying, or irrelevant.** Do not restrict the search to
  stars that look hospitable. A monument could be orbiting a white dwarf, a
  supernova remnant, a failed star, or nothing at all — a relic in a stable
  orbit still running on starlight or on decay heat.
- **It repeats on a cycle.** Content must restart so a late listener can catch
  the beginning. That cycle could be seconds, minutes, hours, days, or years.
  **This is the single hardest thing to catch and the most valuable to find.**
- **It is continuous for millennia.** Any sufficiently long stare accumulates
  it — which means our dwell-time problem (3.2) softens over long baselines,
  but the *repeat period* may exceed any single observation. **Chained scans
  across nights are the only way to find a yearly cycle.**
- **An omnidirectional monument appears EVERYWHERE.** If it is broadcast
  broadly, it shows up in ON and OFF pointings alike — the same common-mode
  situation as traffic, for an entirely different reason. Yet another argument
  that common-mode must not be auto-vetoed.
- **A sweeping directional monument appears and disappears on a schedule.**
  Periodic reappearance in unrelated pointings is a signature.

**Detection hooks:** long-period repetition, stable carrier over days/years,
H-line or water-hole frequency, anomalous Doppler, presence in catalogue-native
"dead" directions.

### 2.3 PAYLOADS — the content itself (Arecibo-style, raster, or executable)

Payload hunting is *content* hunting, and it only begins **after** a detection
in 2.1 or 2.2. But the detectors should be built now, so that a candidate has
somewhere to go.

**The Arecibo model (1974):** 1679 bits, transmitted as a 23 x 73 raster.
**The factorisation is the message.** A prime-factor block structure is a
language-free way of saying *"this is a picture, fold me into 2D."* Nobody had
to agree on anything.

**A self-describing bootstrap** must go, in order:

```
primes -> arithmetic -> logic gates -> encoding -> framing -> universal machine -> program
```

Each layer is verifiable without shared language, because each layer is
*mathematically true* rather than culturally agreed. The only way to send a
program to an unknown architecture is to send a **universal abstract machine**:

- SUBLEQ / NOR one-instruction computer
- SKI combinator graph reduction
- a cellular automaton seed (Rule 110, Wireworld)
- a Markov / string-rewrite system

All four compute the same set of functions. All four are detectable *before*
you can read them.

**Error correction is mandatory** over interstellar distances, which is a gift
to us: engineered data is **coded**, and coding has fingerprints. Look for
Golay G24, Reed-Solomon, CRC-like syndrome behaviour — non-random structure in
demodulated bits.

**Detection hooks (build these before they are needed):**

| hook | what it proves | state |
|---|---|---|
| prime / semiprime block factorisation (`n = p * q`) | raster framing exists | NOT BUILT |
| 2D fold + spatial autocorrelation | the raster is a picture, not noise | NOT BUILT |
| Golay / CRC syndrome on bits | engineered, coded data | BUILT (vm_sandbox) |
| VM execution entropy collapse | the bits *compute* | BUILT (vm_sandbox) |
| LZ / compressibility profile over execution | code vs. noise phase transition | PARTIAL |

**Order of operations is strict:**

```
detect (2.1/2.2) -> characterise -> demodulate -> find frame -> run the VM
```

The VM sandbox is **the last step**, and it has been run repeatedly on thermal
noise today because nothing upstream produced a candidate. Building it was
correct. Never running it on a real candidate is the gap.

---

## 3. Hard consequences for this pipeline

### 3.1 The veto is currently blindfolding us — INVERT IT

Current logic (built for beacons):

```
signal in ON  and OFF   ->  human / local  ->  BLOCK
signal in ON only       ->  celestial      ->  interesting
```

Under the bystander model a third-party link **does not care which way we
point**. A beam between two distant stars will be present in the ON pointing
*and* the OFF pointing, because it is not coming from our target at all.

**Our veto would kill the jackpot and log it as `earth-likely`.**

Correct logic:

```
common-mode + UNSTRUCTURED   ->  local (hum, wander, drift)     -> BLOCK
common-mode + ENGINEERED     ->  THE INTERESTING ONE            -> ESCALATE
```

"Engineered" means measurable structure, not vibes:

- a baud comb in the cyclostationary plane
- a frame period in long-lag autocorrelation
- a coded block (Golay / CRC-like syndrome behaviour)
- a non-Gaussian tail inconsistent with thermal noise
- coherent amplitude/phase behaviour across channels or polarisations

**Do not delete the veto — re-score it.** Common-mode alone stops being
disqualifying; it becomes a *category*, and the question becomes "how
engineered is this?"

### 3.2 Dwell time IS sensitivity

A beacon is a gift: it comes back. Traffic is just *there*, always, and you
accumulate it.

```
bits = bandwidth x time
at 100 bps - 1 kbps:
  1.2 s  ->  15 B    - 150 B     (not a program; not even hello-world)
  60 s   ->  750 B   - 7.5 KB
  1 h    ->  45 KB   - 450 KB
  8 h    ->  360 KB  - 3.6 MB
```

The Arecibo message was 1679 bits. A self-describing bootstrap is kilobytes to
megabytes. **No detector can find a long program in a short window — the bits
physically are not present.**

Practical rule: **a 1 GiB file is a sip, not a dataset.** Chained blocks and
chained scans are the unit of work. 23 seconds is a starting point; multiple
scans stitched together is the goal.

Corollary: because traffic is continuous, **the mark of it is the absence of a
schedule**. We should expect it present in block 0, block 127, and every block
between — and the *only* reason we don't see it is integration, not timing.

### 3.3 Structure-first detection, not tone-first

Tone hunting is the wrong primer. Order of operations:

```
1. ingest raw voltage (phase preserved)
2. look for ANY non-thermal structure
   - cyclostationary baud lines        (S_x^alpha, f=0 slice exists; full plane needed)
   - long-lag autocorrelation / frame period   (NOT BUILT — top priority)
   - intermittency / non-Gaussian tail         (measured; not yet a detector)
   - polarisation coherence
3. only then ask about modulation, framing, and content
4. only then feed bits to the VM sandbox
```

The VM sandbox is **step 5 of 5**. It has been run repeatedly on thermal noise
today because steps 1-4 never produced a candidate. That is not a failure of
the sandbox — it is a failure to feed it.

### 3.4 Targeting geometry: look at ALIGNMENTS, not neighbours

For a beam running from star A to star B to pass near Earth, **A and B must
appear close together in our sky** (within roughly the beam width).

Therefore the correct targeting rule is not "nearby star" or "star with
planets". It is:

> **pairs of stars that appear nearly aligned from Earth** — their mutual
> interstellar link geometry is what crosses our path.

This is computable from a star catalogue and almost nobody aims at it.
(Related: the classic "eavesdropping on interstellar communication" idea.)

Secondary targeting notes:

- **Earth Transit Zone stars** — civilisations at these stars can see Earth
  transit the Sun and therefore already know we exist, for free. (Example in
  hand: TRAPPIST-1, ecliptic latitude +0.63 deg, observed at 1407.7 MHz.)
  Relevant because proximity-in-knowledge correlates with proximity-in-space,
  not because we expect a greeting.
- **Dense stellar regions** — shorter links are cheaper; links cluster where
  stars are close.
- **Quiet bands** — 1400-1427 MHz is excellent not because it is "the H line"
  but because terrestrial transmitters are *legally forbidden* there. Minimum
  noise = maximum achievable bit rate = where an efficient link would prefer to
  live.

### 3.5 Doppler tells us the transmitter is not on Earth

A beacon drifts with Earth's rotation: a fixed, known, sidereal rate.
A third-party link drifts with **both endpoints' orbital and galactic motion**
— different rate, possibly different sign, possibly curved.

Anomalous Doppler is one of the few *unfakeable* hints that a transmitter is
not local. Our Viterbi jerk tracker is genuinely built for this; it is
under-used.

---

## 4. Detector classes we are hunting

Ranked by value to *this* objective:

1. **Cyclostationary baud lines** — any digital modulation leaves them. Works
   with no knowledge of the codebook. Half-built (f=0 slice works and is
   proven at -12 dB DSSS; full (f, alpha) plane exists; needs to run wide).
2. **Long-baseline repetition / frame period** — the signature of packetised
   traffic. **NOT BUILT. Highest-priority new build.**
3. **Non-Gaussian / intermittency statistics** — traffic is coded, so it is not
   perfectly Gaussian. Cheap to measure, never yet used as a *detector*.
4. **Coded-block structure** — Golay / CRC-like syndrome behaviour on
   demodulated bits. Built, waiting for a candidate.
5. **Anomalous Doppler** — non-terrestrial drift. Built (Viterbi + quad fit),
   under-used.
6. **Common-mode + engineered** — the veto inversion (Section 3.1).
7. **Long-period repetition (monuments)** — the same signal reappearing on a
   cycle across hours, days, or separate observations. Needs chained scans and
   a cross-observation matcher.
8. **Prime / semiprime block structure** — raster framing marker (2.3).
9. **2D fold + spatial autocorrelation** — is the raster a picture?
10. **Dead / anomalous directions** — pointings toward supernova remnants,
    white dwarfs, failed stars, or empty sky with no obvious host.

---

## 5. Mission tasks (priority order)

| # | Task | Why | State |
|---|---|---|---|
| M1 | **Veto inversion** — score common-mode by engineeredness instead of auto-blocking | currently discards the target class | NOT STARTED |
| M2 | **Long-baseline repetition / frame hunter** — autocorrelation at lags 10 us - 10 s across whole files, all channels | only detector matched to "packetised traffic" | NOT STARTED |
| M3 | **Long dwell acquisition** — full 128-block files, chained scans, all 4 polarisations | dwell = sensitivity; we have been at ~2% | PARTIAL |
| M4 | **Alignment targeting** — star-pair line-of-sight computation from a catalogue | correct targeting for third-party beams | NOT STARTED |
| M5 | **Doppler anomaly test** — flag signals whose drift is not consistent with Earth rotation | unfakeable locality test | BUILT, UNUSED |
| M6 | **Non-Gaussianity detector** — kurtosis / tail-excess / intermittency as a first-class sieve | cheap, orthogonal, never used as a detector | NOT STARTED |
| M7 | **Config-driven CLI** — header-driven `FS`/geometry, presets, rearrangable detectors | stop editing constants per file | NOT STARTED |
| M8 | **Raster / semiprime block detector** — test bitstreams for prime-factor block structure, fold to 2D, score spatial autocorrelation | payload framing (2.3) | NOT STARTED |
| M9 | **Cross-observation matcher** — find the *same* signature recurring across nights (monument repeat cycle) | only way to catch long-cycle monuments (2.2) | NOT STARTED |
| M10 | **Dead-direction targeting** — supernova remnants, white dwarfs, empty sky, relic-orbital geometry | do not assume the sender is alive (2.2) | NOT STARTED |

**M1 and M2 are the objective-critical path.** M8-M10 are the monument/payload
extension and should not be skipped — they are the difference between hunting
living neighbours and hunting the actual record.

---

## 6. What "found something" looks like — under THIS model

Not one detector firing. The bystander jackpot is a *combination*:

1. **Structure where there should be none** — baud comb or frame period in a
   slice whose spectrum is flat.
2. **Common-mode BUT engineered** — present in ON and OFF, yet carrying
   measurable modulation structure. *(This currently gets vetoed. That is the
   bug.)*
3. **Persistent across time** — present in block 0 and block 127 and everything
   between, because a link is continuous. A real link does not flicker once.
4. **Anomalous Doppler** — drift inconsistent with Earth rotation and with any
   known satellite.
5. **Coded-block behaviour** — demodulated bits show non-random syndrome /
   frame structure.
6. **Emergent geometry** — the same signature appears in *multiple unrelated
   pointings*, consistent with a beam sweeping past rather than a source in the
   target.

**Monument signature (2.2)** — add to the above:

7. **Long-period recurrence** — the same signature reappears on a *cycle*
   across hours, days, or separate observations. Content must restart so a late
   listener catches the beginning; the period may be far longer than any single
   stare.
8. **Host-independent** — present in a pointing with no plausible living host:
   a supernova remnant, a white dwarf, a failed star, or apparently empty sky
   with a transmitter that outlived its makers.
9. **Delay-tolerant** — the signal is still there, unchanged, when you come back
   a week or a year later. A monument does not stop.

**Payload signature (2.3)** — only reachable after a detection:

10. **Framing structure** — demodulated bits factor into a semiprime block
    (`n = p * q`), or contain a repeating sync word. This is the Arecibo trick:
    the factorisation *is* the announcement that a picture exists.
11. **2D structure on fold** — fold the bits into `p x q`, and spatial
    autocorrelation rises well above shuffled and 1D controls. That is a
    picture or a rasterised page, not noise.
12. **Execution** — the sandbox runs more than a handful of instructions,
    sustains an attractor instead of stalling, and memory-access locality
    clusters like stack/heap rather than spraying uniformly. Command is: *it
    computes*.

Which cluster matters depends on which class you are chasing:

```
traffic  ->  1-6      (structure, common-mode, persistence, Doppler, geometry)
monument ->  3 + 7-9  (persistence, recurrence, host-independence, delay-tolerance)
payload  ->  10-12    (framing, raster structure, execution)
```

Any one is a curiosity. Several together, with receipts, is the signal.

---

## 7. Anti-goals and guardrails

**Do not:**

- assume the sender is alive. A monument's civilisation may have been extinct
  for a million years and its star may have already exploded. **Targeting must
  not depend on the host still being there.**
- collapse the three classes. Traffic is optimised to be invisible; a monument
  is optimised to be found. Same sky, opposite design goals — the detectors are
  not the same.
- hunt beacons aimed at us. No "hello, we see you" framing, no assuming anyone
  knows or cares that we exist.
- assume a signal must appear ON-target. Third-party traffic appears wherever
  the beam happens to be.
- auto-veto common-mode. That is the blindfold. Score it, do not delete it.
- run the VM sandbox on noise and call it a test. It is step 5; feed it nothing
  and it correctly reports nothing.
- over-claim. Every negative needs a noise-matched receipt (`AGENTS.md` rule 1).
- waste dwell. 1 GiB is a sip. Chained blocks and chained scans are the unit.
- mistake "quiet" for "empty". Most of the file is *supposed* to be thermal
  noise — that is what a receiver sounds like. The search is for the tail, not
  the body.

**Do:**

- keep it data-driven and configurable — variations per file, on the fly, not
  constant-editing.
- preserve phase. Never square voltages before the detectors see them.
- provenance everything. `hits.csv`, `evidence.csv`, `rfi_catalog.json` are the
  scientific record.
- keep it fun. This is a side quest that is supposed to fuel the person doing
  it, not grind them down. Rigid and stiff kills the project faster than a null
  result ever will.

---

## 8. Assets in hand (as of this objective being written)

**Data**

- TRAPPIST-1 (DIAG_TRAPPIST1), MJD 57807, 2017-02-23, GBT, `Rcvr1_2` L-band
  - blc04, 1407.7 MHz, 8-bit, 64 chan x 4 pol, 128 blocks (~23 s), **cadence
    pair**: scan 0015 ON / scan 0016 OFF (OFF pointing ~1 deg away)
  - 1 GiB partial of each downloaded (7 blocks each)
- W75N, MJD 57388, X-band 8118 MHz - **DEAD** (receiver delivered no signal;
  1.05 bits/byte, 8 distinct byte values across all 16 GB)
- M31, MJD 57396, X-band 9281 MHz, 2-bit - scanned early, before several fixes
- HIP113357 blc4/blc6, MJD 57388 - blc4 healthy, blc6 dark digitizer

**Data source** (no AWS account needed)

```
portal : http://seti.berkeley.edu/opendata
API    : http://seti.berkeley.edu/opendata/api/query-files?target=<NAME>
         http://seti.berkeley.edu/opendata/api/list-targets?simbad
files  : http://blpd0.ssl.berkeley.edu/<dir>/<file>.raw   (HTTP, Accept-Ranges: bytes)
speed  : ~3.6 MB/s per connection (server-side limit, not the VPS)
```

Range GETs make preflight cheap: pull 64 KB, check `PROJID`, `NBITS`, byte
entropy, payload liveness — before paying for 17 GB.

**Tools that work (proven)**

- `c/seti_slice` — GUPPI unpacker. Header padding is now **detected, not
  assumed** (2016 files use 2880-byte FITS padding, 2016+ use 256-byte
  alignment — this was silently truncating every multi-block scan to block 0).
- `c/fam_scan` — Y2/Y4 cyclostationary (f=0 SCD slice)
- `c/vm_sandbox` — SUBLEQ locality + Golay G24 + entropy gate
- `python/scd_frf.py` — full (alpha, f) SCD plane + dechirp bank
- `python/jerk_scan.py` — Viterbi track-before-detect + quadratic fit
- `python/latent_pca.py` — corpus-level anomaly triage
- `python/rfi_veto.py` — disposition engine (needs M1)

**Known defects / gaps**

- veto: common-mode auto-blocks (M1)
- veto: `FLO` / band allocation table hardcoded to X-band
- `FS = 2929687.5` hardcoded in 8 python files instead of header-derived
- no frame/repetition hunter (M2)
- only coarse polarisation coverage (M3)
- catalog explodes on common-mode artifacts (dedupe needed)

---

## 9. Standing orders for any agent on this repo

1. **Read this file first.** If a task does not serve Objective 1, say so.
2. **Prove before detect.** Any new detector ships with a synthetic injection
   prove that shows it fires on the target class and stays quiet on matched
   noise. Report the floor.
3. **Receipts for every negative.** Thresholds come from noise-matched
   realisations, not theory and not one noise draw.
4. **Never hide a flag.** Re-score it, quarantine it, name it — but do not
   silently drop it.
5. **Stay configurable.** Header-driven geometry, presets, detectors that can be
   rearranged per run. No new hardcoded constants. If you must freeze a value,
   put it in a config file with a comment explaining why.
6. **Report honestly.** "No candidates, here is the floor, here is the
   coverage" is a successful shift. Inflated enthusiasm is not.
7. **Keep it fun.** Rigid + stiff = project death. Variation and curiosity are
   features.

---

## 10. One-line summary

> Hunt for **other people's phone calls, and for the monuments they left
> behind** — in the quietest band, with the longest stare, scoring structure
> rather than tones, never assuming the sender is still alive, and never
> discarding a signal just because it was present when we looked away.

Three things are in scope:

1. **Traffic** — links between living civilisations, noise-like by design
2. **Monuments** — repeating "we were here" messages from civilisations that
   may already be extinct, possibly orbiting stars that are already dead
3. **Payloads** — Arecibo-style rasters and self-executing universal machines,
   the content of either of the above

The detectors for all three are the same family: **find structure that thermal
noise cannot produce.** Everything else is targeting, and targeting is
cheap to change. Structure detection is the machine.
