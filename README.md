# TurboKain

### High-Throughput Coherent Radio Technosignature & Bystander Traffic Pipeline
*A native, formally verified signal processing engine for astronomical baseband recordings.*

---

## 1. Executive Summary & Observational Objective

Classical Search for Extraterrestrial Intelligence (SETI) historically presupposes intentional, high-power narrowband isotropic beacons directed at the Solar System. Modern communication theory and orbital link budgets dictate that advanced intelligences communicating across interstellar baselines will optimize strictly for channel capacity and energy efficiency ($\text{bits}/\text{joule}$). Such transmissions are:

1. **Point-to-Point and Off-Axis:** Directed between non-terrestrial nodes; observable from Earth only when our line of sight intercepts the transmission beam, its forward sidelobes, or interstellar scattering volume.
2. **Noise-Matched:** Modulated using high-order constellations, spread-spectrum coding, and forward error correction (FEC). Under power-detection methods, optimal transmissions are mathematically indistinguishable from Gaussian thermal noise.
3. **Continuous and Persistent:** Operating over decade- to millennial-scale baselines, exhibiting cyclic framing, telemetry synchronization, and packetized framing.

**TurboKain** is designed for the **Bystander Mission**: extracting structural signatures that thermal noise cannot produce from raw dual-polarization radio telescope baseband recordings.

The pipeline processes baseband voltage streams down to phase coherence, cyclostationary spectral correlation densities, dispersed pulse trains, chirped Doppler carriers, microsecond-scale autocorrelation lattices, and post-Shannon symbolic machine execution.

---

## 2. Architecture: Modular Source $\to$ Amalgamated Totality

TurboKain applies the **SQLite / BusyBox doctrine** to high-performance astrophysics pipelines: source code is maintained in strictly decoupled, domain-isolated modules during development, then fused into a single whole-program translation unit for native compilation.

```
kain/core/*.kn  ──►  kain amalgamate --raw kain/core -o kain/core.kn  ──►  kain build kain/core.kn  ──►  core.exe (~1.2 MB)
 (14 modules)                                                               (whole-program LLVM)          │
                                                                                                        ├── core <tool> [args...]
                                                                                                        ├── core help <tool>
                                                                                                        ├── core prove
                                                                                                        └── core sweep <f32>
```

### 2.1 Technical Advantages
- **Whole-Program Optimization (WPO):** Amalgamating into `core.kn` exposes the entire call graph to LLVM. The optimizer performs aggressive inter-procedural inlining, dead-code elimination, and loop vectorization across instrument boundaries.
- **Hermetic Portability:** Compiles into a single self-contained executable (`core.exe`, ~1.2 MB) linked directly against operating system system-call boundaries (`kernel32`). It requires zero runtime dependencies, interpreters, or shared libraries.
- **Direct Memory Handoffs:** Instruments share contiguous memory arenas (`Byte` and `Float` memory regions) without disk roundtrips.
- **Dual Invocation Model:** `dispatch.kn` captures invocation context via `GetCommandLineA()`. It operates as a subcommand suite (`core <tool> [args...]`) or as a multi-call binary (copying or linking `core.exe` to `<tool>.exe` executes that instrument directly).

---

## 3. Instrument Suite & Detection Lattice

The core engine comprises 14 specialized instruments spanning the complete RF analysis chain:

| Instrument | Module | Domain | Operational Contract | Sensitivity / Gate Floor |
|------------|--------|--------|----------------------|---------------------------|
| **`slice`** | `slice.kn` | Baseband Ingest | GUPPI `.raw` (2-bit / 8-bit) $\to$ `.f32` complex/power voltage | Layout-aware, 67M samples in 2.3 s |
| **`fil_reader`** | `fil_reader.kn` | Spectral Ingest | Sigproc `.fil` (8/16/32-bit) $\to$ calibrated `.f32` | Header validation, band-mean extraction |
| **`config`** | `config.kn` | Geodesy / Config | Resolves 40 telemetry, RF geometry, and search bounds | CLI $\gt$ Header $\gt$ Preset arbitration |
| **`sk_gate`** | `sk_gate.kn` | RFI Excision | Spectral Kurtosis ($SK$) estimator over 4096/2048 STFT | Excision threshold: $\vert SK - 1 \vert \ge 0.50$ |
| **`xeno_scan`** | `xeno_scan.kn` | Anomaly Screening | 6-marker battery: SK, coherence, comb, dispersion, tail | $\ge 20.0$ ladder ratio, $6.0\sigma$ zero-crossing |
| **`boxcar_bank`** | `boxcar_bank.kn` | Dispersed Pulses | $O(N)$ prefix-sum matched filtering over DM space | Threshold default: $14.0\sigma$ |
| **`fold_sum`** | `fold_sum.kn` | Epoch Folding | Hann-windowed STFT + sub-band 8-harmonic folder | Multi-harmonic threshold: $16.0\sigma$ |
| **`fam_god`** | `fam_god.kn` | Cyclostationary | 3-decade FFT Accumulation Method (SCD estimation) | Regularized Gamma $p$-value, FWE trials correction |
| **`frame_hunt`** | `frame_hunt.kn` | Periodic Modulation | Envelope periodogram + 6-subharmonic comb search | Harmonic family acceptance within 5% |
| **`drift_hunt`** | `drift_hunt.kn` | Chirped Carriers | Taylor dedoppler shift-and-add over $(\dot{f}, f)$ space | Sidereal and topocentric chirp acceleration |
| **`lag_hunt`** | `lag_hunt.kn` | Autocorrelation | Direct lag microscope ($0.01\text{ ms} - 10\text{ s}$) | 4-lens lattice (phase/power/cadence/event) |
| **`bitslice`** | `bitslice.kn` | Stream Conversion | Floating-point voltage $\to$ packed bitstreams (sign/diff/mag) | Coherent integrate-and-dump at baud rate $\alpha$ |
| **`xvm_sandbox`** | `xvm_sandbox.kn` | Symbolic Execution | Subleq, Rule 110 cellular automata, LZ/Berlekamp-Massey | Complexity threshold, TAG steps gate ($2200$) |
| **`cadence_pair`** | `cadence_pair.kn` | Spatial Filtering | Pointing corroboration gate (ON vs. OFF beam triage) | Formal `law` gates: `WATCH`, `COMMON`, `CLEAN` |

---

## 4. Mathematical & Algorithmic Formulations

### 4.1 Spectral Kurtosis (SK) RFI Excision
For $M$ spectral power estimates across channel bins, the estimator evaluates departures from Gaussianity:
$$V_k = \frac{\sum_{m=1}^M P_{m,k}^2}{\left( \sum_{m=1}^M P_{m,k} \right)^2}, \quad SK_k = \frac{M+1}{M-1} \left( M \cdot V_k - 1 \right)$$
For Gaussian white noise, $\mathbb{E}[SK_k] = 1$ with variance $\sigma_{SK}^2 \approx \frac{4}{M}$. RFI contamination is excised when $\vert SK_k - 1 \vert \ge 0.50$ across evaluated bins.

### 4.2 Cyclostationary Spectral Correlation (FAM Algorithm)
Phase-modulated digital communications (BPSK, QPSK, FSK) exhibit non-zero spectral correlation at cyclic frequency $\alpha$:
$$S_x^\alpha(f) = \lim_{T \to \infty} \frac{1}{T} \mathbb{E}\left[ X_T\left(f + \frac{\alpha}{2}\right) X_T^*\left(f - \frac{\alpha}{2}\right) \right]$$
The FFT Accumulation Method evaluates complex channelizer outputs over channel pairs $(f_k, f_l)$ where $f_k - f_l = \alpha$. Detection significances are evaluated via exact regularized lower incomplete Gamma integrals:
$$P(\chi^2 \ge 2 \cdot \text{SNR} \mid 2M) = 1 - \frac{\gamma(M, \text{SNR})}{\Gamma(M)}$$
corrected for Family-Wise Error (FWE) rate across the trial grid.

### 4.3 Dispersion-Compensated Dedoppler Search
Cold plasma dispersion delays lower frequencies according to the dispersion measure ($DM$):
$$\Delta t = k_{\text{DM}} \cdot DM \cdot \left( f_{\text{low}}^{-2} - f_{\text{high}}^{-2} \right), \quad k_{\text{DM}} \approx 4.148808 \times 10^3 \text{ MHz}^2 \text{ pc}^{-1} \text{ cm}^3 \text{ s}$$
For continuous carrier emissions, Doppler drift rates induced by orbital acceleration are parameterized via linear chirps:
$$f(t) = f_0 + \dot{f}_0 \cdot t$$
integrated via the Taylor tree algorithm across $(\dot{f}, f)$ resolution elements.

### 4.4 Post-Shannon Algorithmic Complexity
Demodulated bitstreams are evaluated for computational density and non-random state transitions:
1. **Linear Complexity:** Evaluated via the Berlekamp-Massey algorithm to determine the shortest linear feedback shift register (LFSR) capable of generating the sequence.
2. **Universal Computation:** Bit sequences are seeded as execution memory in single-instruction computing engines (One-Instruction Set Computer / Subleq) and 1D Rule 110 cellular automata to detect self-propagating structures and halting properties.

---

## 5. Build & Verification Protocol

### 5.1 Compilation
TurboKain compiles directly from source through the native Kain compiler:

```bash
# 1. Synthesize the amalgamated single-file core
kain amalgamate --raw kain/core -o kain/core.kn

# 2. Compile to native executable
kain build kain/core.kn --target llvm -o core.exe
```

### 5.2 Formal Prove Battery
Every instrument contains mathematical self-tests verifying analytical bounds against synthetic Gaussian noise and injected reference signals. Run the full battery natively:

```bash
core prove
```

Verification output demonstrates zero-divergence against analytical ground truths:
```
================================================================================
 TurboKain Core Suite — Unified Native Prove Battery (9 instruments)
================================================================================
[1/9] bitslice --prove      -> receipt=PASS prove=4/4
[2/9] boxcar_bank --prove   -> receipt=PASS prove=4/4
[3/9] config --prove        -> receipt=PASS prove=6/6
[4/9] drift_hunt --prove    -> receipt=PASS prove=4/4
[5/9] fil_reader --prove    -> receipt=PASS prove=4/4
[6/9] frame_hunt --prove    -> receipt=PASS prove=9/9
[7/9] lag_hunt --prove      -> receipt=PASS prove=9/9
[8/9] xeno_scan --selftest  -> [selftest] ALL PASS
[9/9] xvm_sandbox --selftest-> receipt=PASS selftest=24/24
================================================================================
 Core Battery Receipt: ALL 9 PROVE BATTERIES PASSED (receipt=PASS)
================================================================================
```

---

## 6. Execution Modes

### 6.1 Interactive Command-Line Help
```bash
# Master directory of all 14 tools and data flows
core help

# Detailed mathematical parameters, flags, and contracts for an instrument
core help slice
core help fam_god
core help boxcar_bank
core help xvm_sandbox
```

### 6.2 Automated Pipeline Sweep (`core sweep`)
Execute the complete 7-stage screening and detection battery on a voltage slice in a single pass:
```bash
core sweep <path_to_voltage.f32> --out-dir reports/target_sweep/ --fs 2929687.5
```
This executes in sequence:
1. `sk_gate` (Spectral kurtosis RFI screening)
2. `xeno_scan` (Statistical anomaly lattice)
3. `boxcar_bank` (Transient dispersed pulse detection)
4. `drift_hunt` (Chirped carrier dedoppler extraction)
5. `frame_hunt` (Harmonic comb and periodicity identification)
6. `lag_hunt` (Direct time-domain autocorrelation lattice)
7. `fam_god` (Cyclostationary spectral correlation density mapping)

### 6.3 Direct Tool Invocation
Individual instruments execute directly with explicit argument contracts:
```bash
# Ingest 128 blocks of channel 44 from a raw GUPPI baseband file
core slice /data/raw/blc00_guppi.raw 44 /data/slices/ch44.f32 128 --pol 0

# Run multi-decade cyclostationary baud rate estimation
core fam_god --in /data/slices/ch44.f32 --fs 2929687.5 --segbank --out reports/fam.md

# Decimate and slice bits at detected baud rate
core bitslice --in /data/slices/ch44.f32 --alpha 11090.0 --out /data/bits/ch44_b11090

# Evaluate computational complexity in the symbolic execution sandbox
core xvm_sandbox --in /data/bits/ch44_b11090.head.sign.bin --out reports/xvm.md

# Gate spatial persistence against an off-target reference observation
core cadence_pair --on reports/on_target.md --off reports/off_target.md --out reports/cadence.md
```

---

## 7. Operational Standards & Research Rigor

1. **Noise-Matched Auditability:** A non-detection is scientifically valid only when accompanied by explicit noise floor sensitivity measurements. Unsubstantiated negative results are prohibited.
2. **Immutable Ledgers:** Every modification, build artifact, and observational verdict is logged sequentially in `memory.tsv` (change log) and `catalog.tsv` (instrument ledger).
3. **Thresholds as Telemetry:** Algorithmic thresholds must not be hardcoded in pipeline logic. All operating bounds, filter dimensions, and significance levels must derive from command-line arguments or formal configuration records (`config.kn`).
4. **Independent Veto Invariants:** Candidate dispositions (`CLEAN`, `WATCH`, `COMMON`, `CANDIDATE`) are governed by formal logical invariants (`law` blocks in Kain). Automated tools generate candidate metrics and evidence receipts; promotion to interstellar candidate status requires multi-epoch verification and human analyst adjudication.

---

## 8. Data Ingest & Ground-Truth Verification

TurboKain ingests raw baseband recordings from major radio observatories:
- **Green Bank Telescope (GBT):** GUPPI baseband format (2-bit and 8-bit complex voltage streams).
- **Parkes Observatory (Murriyang):** Multibeam baseband and filterbank archives.
- **MeerKAT:** High-density array voltage records.

All signal processing algorithms are validated against Python and C oracle benchmarks ([SetiYeti](https://github.com/ephemara/SetiYeti)) and verified across sky observations including FRB 121102, TRAPPIST-1, Sagittarius B2, and interstellar interloper 1I/'Oumuamua.
