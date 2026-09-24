# `perm_entropy.kn` — Fast Permutation Entropy & LZW Algorithmic Complexity Screener

## Research, Mathematics, Architecture & Kain Implementation Guide

| field | value |
|---|---|
| tool | `perm_entropy` (Proposed TurboKain 23) |
| class | non-linear dynamics & information theory — model-free anomaly screener |
| status | blueprint & implementation |
| objective | Objective 1 §3.5 + §4 (non-Gaussian structure, spread spectrum, bystander traffic, unknown unknowns) |
| inputs | `.f32` real voltage / baseband slices; `--fs` mandatory (M7) |
| outputs | `perm.md` + `perm.csv` (`win_idx, t_ms_x100, h1_x1000, h2_x1000, cjs_x1000, klz_x1000, z_drop_x100, kind, verdict`) |
| siblings | `xeno_scan` (microscopic kurtosis/moments), `bitslice` (symbol extraction), `xvm_sandbox` (Turing execution), `lag_hunt` (autocorrelation) |

> **One-line pitch:** While standard FFTs search for *periodic tones* and `drift_hunt` searches for *drifting lines*, **`perm_entropy` operates without any spectral model whatsoever**: it tracks the collapse of ordinal permutation entropy $H_{\text{PE}}$, measures Jensen-Shannon statistical complexity $C_{\text{JS}}$, and quantifies algorithmic compressibility $K_{\text{LZ}}$ directly in streaming time series to flag low-SNR digital modulations, non-linear chaos, and exotic technosignatures that are completely invisible in power waterfalls.

---

## 0. Theoretical Foundation & Why This Tool Exists

1. **The Model-Free Advantage:**
   Traditional SETI and radio astronomy searches assume a specific spectral morphology: a continuous narrowband tone, a periodic pulse train, or a linear chirp. Advanced technological transmissions (such as direct-sequence spread spectrum (DSSS), frequency-hopping spread spectrum (FHSS), continuous phase modulation (CPM), and encrypted telemetry) are explicitly engineered to have flat, featureless power spectra that resemble Gaussian thermal noise. Standard FFT filterbanks cannot distinguish them from the receiver noise floor.
2. **Phase Space Ordinal Structure (Bandt & Pompe 2002):**
   Thermal noise exhibits maximum permutation disorder ($H_{\text{PE}} \approx 1.000$). Any deterministic signal, even embedded in heavy noise at low SNR, introduces persistent ordinal inequalities among neighboring voltage samples. Permutation entropy quantifies this structure in $O(N)$ streaming time without requiring Fourier transforms, phase unrolling, or power calibration.
3. **The Complexity-Entropy Causality Plane (Rosso et al. 2007 PRL):**
   Evaluating entropy alone creates ambiguities (e.g., both white noise and chaotic attractors have high entropy). By evaluating the **Jensen-Shannon Statistical Complexity** $C_{\text{JS}}$ alongside $H_{\text{PE}}$, the tool constructs a 2D diagnostic coordinate $(H, C_{\text{JS}})$:
   - **Thermal Gaussian Noise:** $(H \approx 1.0, C_{\text{JS}} \approx 0.0)$
   - **Periodic Tones / RFI:** $(H < 0.75, C_{\text{JS}} < 0.20)$
   - **Chaotic Attractors / Complex Modulations:** $(H \in [0.60, 0.95], C_{\text{JS}} \ge 0.150)$ — peak complexity!
4. **Algorithmic Information & LZW Complexity:**
   Thermal noise is algorithmically incompressible ($K_{\text{LZ}} \approx 1.0$). Structured transmissions and telemetry contain repeating sequences and state-machine transitions that collapse Lempel-Ziv complexity ($K_{\text{LZ}} \ll 1.0$), providing an independent witness to artificial structure.

---

## 1. Mathematics & Algorithmic Formulations

### 1.1 Ordinal Permutation Embedding & Lehmer Code Mapping ($d = 5$)

Given a real voltage series $\{x_t\}_{t=0}^{N-1}$ and delay parameter $\tau \ge 1$, we construct 5-dimensional delay vectors:
$$X_t = [x_t, x_{t+\tau}, x_{t+2\tau}, x_{t+3\tau}, x_{t+4\tau}]$$

There are $5! = 120$ possible permutations of 5 elements. To map any 5-tuple $(v_0, v_1, v_2, v_3, v_4)$ to a unique integer index $L \in [0, 119]$ in $O(1)$ time:
1. Compute the ordinal ranks $R_i \in \{0, 1, 2, 3, 4\}$ via 10 pairwise comparisons:
   $$R_i = \sum_{j=0}^4 \mathbb{I}(v_j < v_i \lor (v_j == v_i \land j < i))$$
2. Compute the factoradic / Lehmer code components $c_0, c_1, c_2, c_3$:
   $$c_i = \sum_{j=i+1}^4 \mathbb{I}(R_j < R_i)$$
3. The unique permutation index $L$ is:
   $$L = c_0 \cdot 24 + c_1 \cdot 6 + c_2 \cdot 2 + c_3 \cdot 1$$

This provides a strict bijective mapping from $S_5 \to \{0, 1, \dots, 119\}$.

### 1.2 Normalized Permutation Entropy ($H_{\text{PE}}$)

For a window of length $W$ with $N_v = W - 4\tau$ vectors, we accumulate the histogram $C[0 \dots 119]$:
$$p_j = \frac{C[j]}{N_v}, \quad j = 0 \dots 119$$
The Shannon entropy is:
$$S[P] = - \sum_{j=0}^{119} p_j \log_2(p_j)$$
Normalized Permutation Entropy is bounded in $[0, 1]$:
$$H_{\text{PE}} = \frac{S[P]}{\log_2(120)} = \frac{S[P]}{6.9068906}$$

### 1.3 Jensen-Shannon Statistical Complexity ($C_{\text{JS}}$)

Let $P = (p_0, \dots, p_{119})$ be the empirical distribution, and $P_e = (1/120, \dots, 1/120)$ be the uniform distribution.
The mixture distribution is $M = \frac{1}{2}(P + P_e)$.
The Jensen-Shannon divergence is:
$$D_{\text{JS}}(P, P_e) = S[M] - \frac{1}{2} S[P] - \frac{1}{2} S[P_e]$$
The statistical complexity is defined as:
$$C_{\text{JS}} = Q_0 \cdot D_{\text{JS}}(P, P_e) \cdot H_{\text{PE}}$$
where the normalizer is $Q_0 = \frac{1}{D_{\text{max}}} \approx 1.0360707$.

### 1.4 Lempel-Ziv Algorithmic Complexity ($K_{\text{LZ}}$)

Using Kaspar & Schuster (1987) LZ76 formulation:
The voltage window is binarized around its median $b_t = \mathbb{I}(x_t \ge \text{median})$.
A parsing cursor partitions the binary stream into unique substring components $Q$ not present in prior prefix history.
The normalized complexity is:
$$K_{\text{LZ}} = \frac{c \cdot \log_2(W)}{W}$$
where $c$ is the total component count.
- Random noise: $K_{\text{LZ}} \approx 1.04$
- BPSK modulation: $K_{\text{LZ}} \approx 0.25 - 0.50$
- Periodic tone: $K_{\text{LZ}} \le 0.15$

---

## 2. Decision Ladder & Alien Construct Specifications

| Rung | Construct | Role in `perm_entropy.kn` |
|---|---|---|
| L3 | **`converge`** | `lehmer5(v0, v1, v2, v3, v4)` verified against spec permutation sorter with `verify random(8)` |
| L2 | **`law`** | `law pe_bounds` ($0 \le H \le 1000$), `law complexity_bounds` ($0 \le C \le 1000$), `law lz_bounds` ($0 \le K \le 1500$) |
| L1 | **`world` + `entangle`** | `EntropyAuthority` ↔ `EntropyMirror` tracking window totals, anomaly counts, minimum entropy, and lead anomaly timestamps |
| L2 | **`patch`** | `commit_entropy_window` journals each processed window into the audit ledger |
| L7 | **`collapse`/`decay`** | Single `decay` per arena with strict $+32$ byte SIMD safety padding |
| L0 | **`fn/struct`** | Fast kernel32 file streaming, quickselect median, formatting helpers |

---

## 3. Formal 5-Check Prove Battery (`--prove`)

1. **P1 (Permutation Bijective Mapping):** Evaluates all 120 unique permutations of $[0.0, 1.0, 2.0, 3.0, 4.0]$. Asserts min index = 0, max index = 119, unique count = 120 (0 collisions).
2. **P2 (Gaussian Thermal Noise Control):** $N=2048$ samples of Gaussian noise. Asserts $H_{\text{PE}}(\tau=1) \ge 0.985$, $C_{\text{JS}} \le 0.030$, $K_{\text{LZ}} \ge 0.950$, and verdict `CLEAN`.
3. **P3 (Continuous Wave Tone Injection):** Injected sinusoidal carrier. Asserts $H_{\text{PE}} \le 0.800$, $K_{\text{LZ}} \le 0.200$, and verdict `ANOMALY-PERIODIC`.
4. **P4 (Digital BPSK Modulation Injection):** Injected pseudo-random phase transitions. Asserts $K_{\text{LZ}} \le 0.500$, $H_{\text{PE}} \le 0.950$, and verdict `ANOMALY-MODULATION`.
5. **P5 (Non-Linear Chaos Attractor / Logistic Map):** Chaotic orbit $x_{n+1} = 4x_n(1 - x_n)$. Asserts peak statistical complexity $C_{\text{JS}} \ge 0.150$, $H_{\text{PE}} \in [0.60, 0.95]$, and verdict `ANOMALY-CHAOS`.

---
*End of Guide*
