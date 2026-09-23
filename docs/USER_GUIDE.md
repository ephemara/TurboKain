# TurboKain User Guide

A practical, step-by-step manual for running radio technosignature and bystander signal analysis using **TurboKain**.

---

## Table of Contents

1. [Introduction & 30-Second Quickstart](#1-introduction--30-second-quickstart)
2. [Installation & Binary Setup](#2-installation--binary-setup)
3. [The Three Ways to Run TurboKain](#3-the-three-ways-to-run-turbokain)
4. [The 14 Instruments: A Plain-English Guide](#4-the-14-instruments-a-plain-english-guide)
5. [Configuration & Presets Deep Dive (`config` / `cfg`)](#5-configuration--presets-deep-dive-config--cfg)
6. [Automating with Python](#6-automating-with-python)
7. [The End-to-End Observational Pipeline (The "Ping-Pong" Protocol)](#7-the-end-to-end-observational-pipeline-the-ping-pong-protocol)
8. [Quick-Reference Cheat Sheet](#8-quick-reference-cheat-sheet)

---

## 1. Introduction & 30-Second Quickstart

### What TurboKain Does
When a radio telescope observes the sky, it captures continuous, high-bandwidth electromagnetic voltages. Most of this data is thermal noise from space, telescope electronics, or terrestrial Radio Frequency Interference (RFI) from satellites, cell towers, and radars.

TurboKain ingests these raw voltage recordings and searches for **structures that thermal noise cannot physically produce**:
* Dispersed pulses delayed by interstellar cold plasma ($\text{DM}$)
* Cyclostationary phase modulations produced by digital communication links (BPSK, QPSK, FSK)
* Linearly chirped carrier tones drifting due to orbital acceleration
* Microsecond-to-second periodic framing and direct autocorrelation echoes
* Non-random, post-Shannon algorithmic complexity in demodulated bitstreams

### Quickstart in 3 Commands

1. **Verify your installation:**
   ```bash
   tkc prove
   ```
   *Runs all 9 mathematical self-test batteries in-memory in under 3 seconds. You should see `receipt=PASS` for every instrument.*

2. **Explore available tools:**
   ```bash
   tkc help
   ```
   *Prints the complete directory of all 14 tools, categorized by mission phase.*

3. **Get deep help on any specific tool:**
   ```bash
   tkc help fam
   tkc help xvm
   tkc help slice
   ```

---

## 2. Installation & Binary Setup

### Option A: Download the Pre-Compiled Binary (Recommended)
Download the latest native binary release from GitHub:
👉 **[GitHub Releases: TurboKain v0.1.0-alpha](https://github.com/ephemara/TurboKain/releases/tag/v0.1.0-alpha)**

Extract the archive. You will have:
* `tkc.exe` (The primary ~1.2 MB native executable)
* `tkc.cmd` (Windows command-line shim)
* `turbokain_core.exe` (Formal release binary name; identical to `tkc.exe`)

Place `tkc.exe` and `tkc.cmd` into your system `PATH` (or run them directly from the repo root).

### Option B: Build from Source
If you are compiling from source using the Kain compiler:

```bash
# 1. Synthesize the amalgamated core translation unit:
kain amalgamate --raw kain/core -o kain/core.kn

# 2. Compile to native x86-64 binary via LLVM:
kain build kain/core.kn --target llvm -o tkc.exe

# 3. Create aliases:
cp tkc.exe turbokain_core.exe
cp tkc.exe core.exe
```

---

## 3. The Three Ways to Run TurboKain

TurboKain is built to accommodate interactive terminal analysis, automated multi-stage pipelines, and Python orchestration.

### 1. Interactive CLI (`tkc <tool> [args]`)
Every tool can be run as a subcommand with short aliases:
```bash
tkc slice D:/data/raw/scan.raw 44 ch44.f32 128 --pol 0
tkc fam --in ch44.f32 --segbank --out fam.md
tkc xvm --in bits.bin --out xvm.md
```

### 2. The Automated Sweep (`tkc sweep <file.f32>`)
Instead of invoking 7 separate commands, `tkc sweep` runs the entire detector battery across a voltage slice in a single pass:
```bash
tkc sweep ch44.f32 --out-dir reports/ch44_sweep/ --fs 2929687.5
```
This automatically runs:
1. `sk_gate` (RFI excision)
2. `xeno_scan` (6-marker statistical anomaly battery)
3. `boxcar_bank` (DM pulse matched filtering)
4. `drift_hunt` (Doppler carrier search)
5. `frame_hunt` (Harmonic comb periodogram)
6. `lag_hunt` (Direct autocorrelation lattice)
7. `fam_god` (Cyclic spectral correlation density)

### 3. Python Orchestration (`python/tk.py`)
TurboKain includes a lightweight, Python-standard-library-only orchestration driver under `python/`:
```bash
# List all tools and catalog status:
python python/tk.py list

# Run the complete test suite:
python python/tk.py prove

# Run a unified sweep over raw GUPPI or .f32 data:
python python/tk.py scan D:/data/raw/blc00.raw --chans 32,44,60 --blocks 128
```

---

## 4. The 14 Instruments: A Plain-English Guide

### Category 1: Ingest & Telemetry

#### 1. `slice` (GUPPI Baseband Ingest)
* **What it does:** Radio telescopes record dual-polarization complex baseband voltages in GUPPI format (17 GB files containing 128 data blocks). `slice` decodes raw 2-bit or 8-bit quantized integer samples directly into standard IEEE 32-bit floating-point voltage time series (`.f32`).
* **Shorthand:** `slice`
* **Syntax:**
  ```bash
  tkc slice <raw_file> <channel> <output.f32> [max_blocks] [--pol 0|1]
  # or with flags:
  tkc slice --in scan.raw --chan 44 --pol 0 --out ch44.f32 --blocks 128
  ```
* **Speed:** Processes a full 17 GB file (67 million samples) in **2.3 seconds**.

#### 2. `fil_reader` (Sigproc Filterbank Ingest)
* **What it does:** Many archival astronomical datasets (e.g. Galactic Center surveys) are stored as Sigproc `.fil` channelized power filterbanks rather than raw baseband voltages. `fil_reader` decodes 8-bit, 16-bit, and 32-bit filterbank files into calibrated `.f32` streams for downstream detectors.
* **Shorthand:** `fil`
* **Syntax:**
  ```bash
  tkc fil --in scan.fil --chan 32 --out ch32.f32
  tkc fil --in scan.fil --chan-lo 10 --chan-hi 50 --mean --out bandmean.f32
  ```

#### 3. `config` (Parameter & Geodesy Arbitration)
* **What it does:** Detectors need to know center frequencies, sample rates, bandwidths, and noise thresholds. `config` resolves these parameters using a strict three-tier hierarchy: **CLI flags override GUPPI headers, which override TOML preset files**.
* **Shorthand:** `cfg`
* **Syntax:**
  ```bash
  tkc cfg --show --preset presets/cband.toml --raw scan.raw
  tkc cfg --get fs --preset presets/cband.toml --raw scan.raw
  ```

---

### Category 2: RFI Excision & Anomaly Screening

#### 4. `sk_gate` (Spectral Kurtosis Gate)
* **What it does:** Evaluates whether each frequency bin follows Gaussian white-noise statistics. Terrestrial transmitters (radars, cell towers) heavily skew the power distribution. `sk_gate` calculates the Spectral Kurtosis ($SK$) over 4096/2048 STFT windows. If $|SK - 1| \ge 0.50$ in $>2\%$ of bins, the block is flagged as corrupted by RFI.
* **Shorthand:** `sk`
* **Syntax:**
  ```bash
  tkc sk --in ch44.f32 --out sk_report.md --csv sk_report.csv
  ```

#### 5. `xeno_scan` (6-Marker Microscopic Battery)
* **What it does:** Runs a battery of six independent physical and statistical anomaly tests on a voltage slice:
  1. **Spectral Kurtosis** (non-Gaussianity)
  2. **Zero-Crossing Interval Coherence** (clock-grade oscillator detection)
  3. **Cepstral Comb Ladder** (log-spectrum FFT quefrency peak detection)
  4. **DM Sign Order** (arrival-time frequency dispersion)
  5. **Impulsivity** ($>8\sigma$ transient bursts)
  6. **Excess Tail Kurtosis** ($4\sigma$ Gaussian tail departures)
* **Shorthand:** `xeno`
* **Syntax:**
  ```bash
  tkc xeno --in ch44.f32 --fs 2929687.5 --out xeno.md
  tkc xeno --selftest
  ```

---

### Category 3: Coherent & Periodic Detectors

#### 6. `boxcar_bank` (Dispersed Pulse Search)
* **What it does:** Interstellar electrons delay low radio frequencies relative to high frequencies. Fast Radio Bursts (FRBs) and pulsed signals arrive as curved parabolic sweeps across frequency. `boxcar_bank` searches across Dispersion Measure ($DM$) space and sweeps 8 boxcar matched filters ($1$ to $128$ samples wide) using an $O(N)$ prefix-sum algorithm.
* **Shorthand:** `boxcar`, `bb`
* **Syntax:**
  ```bash
  tkc boxcar --in ch44.f32 --dm-trials 32 --dm-max 1000.0 --thresh 14.0 --out pulse
  tkc boxcar --prove
  ```

#### 7. `fold_sum` (Harmonic Epoch Folder)
* **What it does:** Searches for weak periodic pulses (such as pulsars, beacons, or repeating transmitters) buried deep below the noise floor by folding the envelope into phase bins across trial periods. Uses 8-harmonic summation with a $16\sigma$ detection threshold.
* **Shorthand:** `fold`
* **Syntax:**
  ```bash
  tkc fold --in ch44.f32 --fs 2929687.5 --topk 8 --out fold.md
  ```

#### 8. `fam_god` (Cyclostationary Spectral Correlation Hunter)
* **What it does:** Digital communications (BPSK, QPSK, spread spectrum) have a hidden cyclostationary clock: the symbol baud rate $\alpha$. Even when a transmission is spread across a wide band and looks identical to Gaussian thermal noise on a standard power spectrum, its **Spectral Correlation Density (SCD)** exhibits sharp peaks at $(f, \alpha)$. `fam_god` runs a 3-decade baud bank ($8\text{ kHz}, 32\text{ kHz}, 131\text{ kHz}$) using the FFT Accumulation Method in seconds.
* **Shorthand:** `fam`
* **Syntax:**
  ```bash
  tkc fam --in ch44.f32 --fs 2929687.5 --segbank --out fam.md
  ```

#### 9. `frame_hunt` (Harmonic Comb & Periodicity Hunter)
* **What it does:** Searches for structured frame rates and synchronization pulses across $0.5\text{ ms}$ to $1000\text{ ms}$ intervals using envelope decimation, high-pass filtering, and subharmonic comb walks.
* **Shorthand:** `frame`
* **Syntax:**
  ```bash
  tkc frame --in ch44.f32 --fs 2929687.5 --thresh 40.0 --out frame.md
  tkc frame --prove
  ```

#### 10. `drift_hunt` (Dedoppler Carrier Search)
* **What it does:** A transmitter located on a rotating planet or orbiting spacecraft experiences Doppler shift, causing its carrier frequency to drift over time ($\dot{f}$). `drift_hunt` computes an STFT waterfall and applies Taylor tree shift-and-add integration across trial drift rates.
* **Shorthand:** `drift`
* **Syntax:**
  ```bash
  tkc drift --in ch44.f32 --drmax 2000.0 --step 100.0 --thresh 8.0 --out drift.md
  tkc drift --prove
  ```

#### 11. `lag_hunt` (Direct Autocorrelation Microscope)
* **What it does:** Instead of transforming into frequency space, `lag_hunt` calculates direct time-domain autocorrelation $R_{xx}(\tau)$ over microsecond-to-second baselines ($0.01\text{ ms} - 10\text{ s}$). It operates four distinct analytic lenses (Phase, Power, Cadence, Event) to detect self-similarity, repeating codes, and multi-path reflections.
* **Shorthand:** `lag`
* **Syntax:**
  ```bash
  tkc lag --in ch44.f32 --fs 2929687.5 --thresh 12.0 --out lag.md
  tkc lag --prove
  ```

---

### Category 4: Stream Slicing & Symbolic Execution

#### 12. `bitslice` (Voltage-to-Bitstream Converter)
* **What it does:** Once a carrier frequency or baud rate $\alpha$ has been identified (e.g. from `fam_god`), `bitslice` performs coherent integrate-and-dump decimation to convert floating-point voltages into packed binary bitstreams:
  * `.sign.bin`: Phase transitions (MSB-first bitstream)
  * `.diff.bin`: Inversion-robust differential transition encoding
  * `.mag.bin`: Energy modulation (1 if power exceeds local mean-square)
* **Shorthand:** `bits`
* **Syntax:**
  ```bash
  tkc bits --in ch44.f32 --alpha 11090.0 --out /data/bits/ch44_b11090
  tkc bits --prove
  ```

#### 13. `xvm_sandbox` (Post-Shannon Symbolic Execution Sandbox)
* **What it does:** If a signal is an engineered data transmission, what does its bitstream contain? `xvm_sandbox` treats the incoming bits as executable code and computational state:
  * **Subleq Machine:** Executes the bitstream in a One-Instruction Set Computer architecture to test for instruction loops.
  * **Rule 110 Cellular Automata:** Seeds bits into a 1D universal cellular automaton to evaluate self-propagating structures.
  * **Berlekamp-Massey Linear Complexity:** Determines if the bitstream was produced by a Linear Feedback Shift Register (LFSR).
  * **Raster Dimensions:** Tests for 2D visual raster dimensions (images or diagrams).
* **Shorthand:** `xvm`
* **Syntax:**
  ```bash
  tkc xvm --in ch44_b11090.head.sign.bin --out xvm.md
  tkc xvm --selftest
  ```

---

### Category 5: Spatial Verification

#### 14. `cadence_pair` (ON/OFF Spatial Corroboration Gate)
* **What it does:** The ultimate arbiter in radio astronomy. When an instrument detects a signal on a target star (ON-target observation), the telescope is nodded away to empty space (OFF-target observation).
  * **ON flagged + OFF clean $\to$ `WATCH`:** Genuine candidate originating from that patch of sky.
  * **ON flagged + OFF flagged $\to$ `COMMON`:** Local human terrestrial RFI picked up through sidelobes.
  * **ON clean + OFF clean $\to$ `CLEAN`:** Quiet thermal noise.
* **Shorthand:** `cad`
* **Syntax:**
  ```bash
  tkc cad --on on_target.md --off off_target.md --out cadence_verdict.md
  ```

---

## 5. Configuration & Presets Deep Dive (`config` / `cfg`)

TurboKain requires consistent observational metadata (sample rates, center frequencies, channel widths). The `config` instrument arbitrates these settings.

### Initializing a Preset Template
Generate a documented TOML configuration template with astronomical defaults:
```bash
tkc cfg --init presets/cband_gbt.toml
```

### The Three-Tier Arbitration Hierarchy
When running tools or resolving parameters:
1. **Command Line Flag (`--set key=value`):** Highest priority. Overrides everything.
2. **Raw Header (GUPPI / Sigproc header):** Medium priority. Actual physical telescope geometry extracted from the observation metadata.
3. **Preset File (`--preset file.toml`):** Default fallback for mission thresholds.

### Inspecting Settings
View the fully arbitrated configuration:
```bash
tkc cfg --show --preset presets/cband_gbt.toml --raw /data/raw/scan.raw
```
Extract a single parameter for shell scripting:
```bash
FS_HZ=$(tkc cfg --get fs --preset presets/cband.toml --raw scan.raw)
echo "Resolved sampling rate: $FS_HZ Hz"
```

---

## 6. Automating with Python

The `python/turbokain/` package provides a pure Python standard-library wrapper (no `pip install`, no dependencies required) for driving the native binaries, capturing receipts, and orchestrating campaigns.

### 1. Using the `tk` CLI Driver
```bash
# List all registered instruments and check binary presence:
python python/tk.py list

# Run the complete test suite across all 14 instruments:
python python/tk.py prove

# Run an automated multi-channel sweep:
python python/tk.py scan D:/data/raw/blc00.raw --chans 16,32,44,60 --blocks 128
```

### 2. Writing Custom Python Scripts
You can import `turbokain` directly in your own automation scripts:

```python
from pathlib import Path
from turbokain.registry import load_registry
from turbokain.runner import run_tool

root = Path("D:/TurboKain")
reg = load_registry(root)

# 1. Ingest a raw file:
slice_tool = reg.tools["slice"]
result = run_tool(slice_tool, [
    "D:/data/raw/scan.raw",
    "44",
    "D:/data/slices/ch44.f32",
    "128",
    "--pol", "0"
], root=root)

print(f"Slice finished in {result.seconds:.2f}s with exit code {result.returncode}")
print(f"Verdicts: {result.verdicts}")

# 2. Run cyclostationary baud rate estimation:
fam_tool = reg.tools["fam_god"]
fam_result = run_tool(fam_tool, [
    "--in", "D:/data/slices/ch44.f32",
    "--fs", "2929687.5",
    "--segbank",
    "--out", "reports/fam.md"
], root=root)

if fam_result.ok and fam_result.receipt:
    print("FAM God pass complete. Reviewing peak list...")
```

---

## 7. The End-to-End Observational Pipeline (The "Ping-Pong" Protocol)

Here is a complete, realistic workflow tracing a candidate from an initial telescope recording to spatial verification:

```text
[GUPPI Raw .raw]
       │
       ▼
 1. tkc slice          --> Extracts complex voltage (.f32)
       │
       ▼
 2. tkc sk             --> Excises RFI blocks (|SK-1| >= 0.50)
       │
       ▼
 3. tkc fam            --> Estimates cyclic baud rate (alpha = 11.09 kHz)
       │
       ▼
 4. tkc bits --alpha   --> Coherent integrate-and-dump (bits.bin)
       │
       ▼
 5. tkc xvm            --> Evaluates Turing complexity and Rule 110 halting
       │
       ▼
 6. tkc cad            --> Compares ON-target vs OFF-target observation
```

### Step 1: Slice the Target Channel
Extract 128 blocks (~67 million samples) of Channel 44, Polarization 0:
```bash
tkc slice D:/data/raw/on_target.raw 44 on_ch44.f32 128 --pol 0
tkc slice D:/data/raw/off_target.raw 44 off_ch44.f32 128 --pol 0
```

### Step 2: RFI Screening
Ensure the channel is not saturated by local ground transmitters:
```bash
tkc sk --in on_ch44.f32 --out reports/on_sk.md
```

### Step 3: Cyclostationary Baud Rate Hunting
Search for digital symbol modulation rates:
```bash
tkc fam --in on_ch44.f32 --segbank --out reports/on_fam.md
```
*Suppose `reports/on_fam.md` detects a persistent Y2 cyclostationary peak at $\alpha = 11,090\text{ Hz}$.*

### Step 4: Extract the Bitstream at the Detected Baud Rate
Demodulate the phase transitions into packed binary:
```bash
tkc bits --in on_ch44.f32 --alpha 11090.0 --out /data/bits/on_ch44_b11090
```

### Step 5: Symbolic Execution Sandbox
Evaluate the bitstream for universal computation:
```bash
tkc xvm --in /data/bits/on_ch44_b11090.head.sign.bin --out reports/on_xvm.md
```

### Step 6: Cadence Triage (ON vs. OFF)
Run the spatial gating law:
```bash
tkc cad --on reports/on_fam.md --off reports/off_fam.md --out reports/cadence.md
```
* If `reports/cadence.md` records **`WATCH`**, the transmission was present **only** while pointing at the target star.
* If it records **`COMMON`**, the transmission was equally present in the off-pointing and is flagged as terrestrial interference.

---

## 8. Quick-Reference Cheat Sheet

### Common Executable Names
* `tkc` (Primary fast name)
* `core` (Short name)
* `turbokain_core` (Formal release name)

### Common Tool Shorthands
| Instrument | Shorthands | Primary Role |
|---|---|---|
| `slice` | `slice` | Raw GUPPI voltage ingest |
| `fil_reader` | `fil` | Sigproc filterbank ingest |
| `config` | `cfg` | Metadata and telemetry arbitration |
| `sk_gate` | `sk` | Spectral Kurtosis RFI excision |
| `xeno_scan` | `xeno` | 6-marker microscopic anomaly battery |
| `boxcar_bank` | `boxcar`, `bb` | Dispersed single pulse search ($DM$) |
| `fold_sum` | `fold` | Multi-harmonic periodicity folding |
| `fam_god` | `fam` | Cyclostationary baud rate estimation |
| `frame_hunt` | `frame` | Envelope periodogram & harmonic combs |
| `drift_hunt` | `drift` | Taylor dedoppler chirped carrier search |
| `lag_hunt` | `lag` | Direct time-domain autocorrelation |
| `bitslice` | `bits` | Voltage-to-bitstream conversion |
| `xvm_sandbox` | `xvm` | Turing & cellular automata sandbox |
| `cadence_pair` | `cad` | Spatial ON/OFF pointing gate |

### Common Flags Across Tools
* `--in <path>`: Path to input data (`.f32`, `.raw`, `.fil`, `.bin`)
* `--out <path>`: Output Markdown table report
* `--csv <path>`: Output CSV table mirror
* `--fs <Hz>`: Explicit sample rate in Hertz (e.g. `2929687.5`)
* `--data-dir <dir>`: Root data directory (or set `$SETIYETI_DATA`)
* `--json`: Emit machine-readable JSON status to stdout
* `--prove` / `--selftest`: Run built-in analytical self-test
