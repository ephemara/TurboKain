# `subspace_null.kn` — Baseband Spatial Subspace Projection & Coherent RFI Nulling Engine

## Research, Mathematics, Architecture & Kain Implementation Guide

| field | value |
|---|---|
| tool | `subspace_null` (Proposed TurboKain 24 / RBSPE) |
| class | spatial signal processing & RFI mitigation — orthogonal subspace nulling |
| status | blueprint & implementation |
| objective | Objective 1 §3.5 + §4 (preserving celestial phase through intense directional RFI) |
| inputs | dual-polarization `.f32` voltages (`--in0 pol0.f32 --in1 pol1.f32`) or interleaved baseband |
| outputs | cleaned dual-pol `.f32` streams (`--out0 clean0.f32 --out1 clean1.f32`), `null.md`, `null.csv` |
| siblings | `sk_gate` (power blanking), `scint_pol` (polarization coherence), `slice` (dual-pol voltage extraction) |

> **One-line pitch:** While standard RFI blankers (`sk_gate`) aggressively discard corrupted science data blocks, **`subspace_null` computes the spatial covariance matrix $R_{xx}$ of dual-polarization baseband voltages, identifies the dominant interference eigenvector, and projects deep orthogonal nulls ($>30\text{ dB}$) toward the transmitter**—eradicating directional RFI while preserving the continuous phase and timing of the celestial target underneath.

---

## 0. Theoretical Foundation & Why This Tool Exists

1. **The Flaw of Power Blanking:**
   In modern radio astronomy, anthropogenic transmitters (satellites, cellular towers, aviation radar) exceed celestial signals by 40 to 80 dB. Standard mitigation tools (like Spectral Kurtosis `sk_gate`) operate by threshold blanking: when an RFI pulse is detected, the entire frequency channel or time block is zeroed out or masked. If an astronomical transient (such as an FRB or a technosignature) arrives during an RFI event, blanking permanently destroys the discovery.
2. **Spatial Degrees of Freedom in Dual-Polarization Feeds:**
   All modern radio telescopes (including the Green Bank Telescope and Parkes) employ dual-polarized receiver feeds ($X$ and $Y$ linear, or $L$ and $R$ circular). A single terrestrial transmitter impinges upon the feed along a specific spatial polarization manifold $\mathbf{v}_{\text{rfi}} = [v_0, v_1]^T$. 
3. **Orthogonal Subspace Projection ($P^\perp = I - \mathbf{u}\mathbf{u}^H$):**
   By decomposing the $2 \times 2$ spatial covariance matrix $R_{xx}$, the dominant eigenvalue $\lambda_1$ isolates the power of the directional RFI. Constructing the orthogonal projection operator $P^\perp$ maps the incoming voltage vectors onto the null space of the RFI manifold.
4. **Preserving Phase and Dynamic Calibration:**
   Unlike incoherent subtraction, linear spatial projection preserves the analytic phase topology, sub-nanosecond timing, and coherent dedispersion characteristics of any signal whose spatial manifold is not collinear with the RFI.

---

## 1. Mathematics & Closed-Form Analytical Eigensolver ($M = 2$)

Given dual-polarization baseband voltage samples $\mathbf{x}[n] = [x_0[n], x_1[n]]^T$ over an integration block of $N$ samples:

### 1.1 Spatial Covariance Estimation
$$R_{xx} = \frac{1}{N} \sum_{n=0}^{N-1} \mathbf{x}[n] \mathbf{x}^H[n] = \begin{bmatrix} r_{00} & r_{01} \\ r_{01}^* & r_{11} \end{bmatrix}$$
where $r_{00}, r_{11} \in \mathbb{R}$, and $r_{01} = r_{01,\text{re}} + j r_{01,\text{im}} \in \mathbb{C}$.

### 1.2 Closed-Form Hermitian Eigen-Decomposition
$$\text{Trace} = r_{00} + r_{11}, \quad \Delta = \sqrt{(r_{00} - r_{11})^2 + 4 |r_{01}|^2}$$
The dominant (RFI) and minor (SOI + noise) eigenvalues are:
$$\lambda_1 = \frac{\text{Trace} + \Delta}{2}, \quad \lambda_2 = \frac{\text{Trace} - \Delta}{2}$$
The condition ratio $\gamma = \frac{\lambda_1}{\lambda_2}$ serves as a formal, unitless RFI indicator:
- **Thermal Gaussian Noise:** $\lambda_1 \approx \lambda_2 \implies \gamma \in [1.0, 2.5]$
- **Directional Polarized RFI:** $\lambda_1 \gg \lambda_2 \implies \gamma \ge 5.0$ (up to $1000+$)

### 1.3 Dominant Eigenvector & Orthogonal Projector
The normalized interference steering vector $\mathbf{u}_{\text{rfi}} = [u_0, u_1]^T$ satisfies $(R_{xx} - \lambda_1 I)\mathbf{u} = 0$:
$$u_0 = \frac{r_{01}}{\sqrt{|r_{01}|^2 + (\lambda_1 - r_{00})^2}}, \quad u_1 = \frac{\lambda_1 - r_{00}}{\sqrt{|r_{01}|^2 + (\lambda_1 - r_{00})^2}}$$
The orthogonal projection operator $P^\perp = I_2 - \mathbf{u}\mathbf{u}^H$ is:
$$P^\perp = \begin{bmatrix} 1 - |u_0|^2 & -u_0 u_1^* \\ -u_1 u_0^* & 1 - |u_1|^2 \end{bmatrix}$$
Notice that $P^\perp$ is Hermitian ($(P^\perp)^H = P^\perp$) and idempotent ($(P^\perp)^2 = P^\perp$).

### 1.4 Streaming Sample Projection
For each sample vector $\mathbf{x}[n]$, the cleaned voltage vector is:
$$\mathbf{x}_{\text{clean}}[n] = P^\perp \mathbf{x}[n]$$
When no RFI is detected ($\gamma < \gamma_{\text{gate}}$), $P^\perp$ defaults to the identity matrix $I_2$, passing thermal noise through untouched.

---

## 2. Decision Ladder & Alien Construct Specifications

| Rung | Construct | Role in `subspace_null.kn` |
|---|---|---|
| L3 | **`converge`** | `cov2x2_eigen` verified against reference solver via `verify random(8)` |
| L2 | **`law`** | `law covariance_psd` ($\lambda_1 \ge \lambda_2 \ge 0$), `law projection_idempotent` ($P^2 = P$), `law rfi_condition_ratio` |
| L1 | **`world` + `entangle`** | `SubspaceAuthority` ↔ `SubspaceMirror` tracking blocks processed, RFI blocks nulled, and peak suppression dB |
| L2 | **`patch`** | `commit_subspace_block` journals block diagnostics into the run ledger |
| L7 | **`collapse`/`decay`** | Fast dual-channel memory buffers with $+32$ byte SIMD safety padding |
| L0 | **`fn/struct`** | Fast kernel32 dual-handle file streaming and scaled integer telemetry |

---

## 3. Formal 5-Check Prove Battery (`--prove`)

1. **P1 (Projector Idempotence & Hermiticity):** Asserts $(P^\perp)^2 = P^\perp$ and $(P^\perp)^H = P^\perp$ to machine precision ($< 10^{-6}$).
2. **P2 (Thermal Noise Passthrough Control):** $N=4096$ dual-pol Gaussian noise. Condition ratio $\lambda_1/\lambda_2 < 3.0$ keeps projector at identity ($0\text{ dB}$ attenuation, `CLEAN-PASSTHROUGH`).
3. **P3 (Directional RFI Eigen-Alignment & Nulling):** $+30\text{ dB}$ RFI at polarization angle $\theta = 35^\circ$. Asserts measured eigenvector error $< 0.01$ and RFI power suppression $\ge 25.0\text{ dB}$.
4. **P4 (SOI Waveform & Phase Preservation):** Injected faint celestial tone overlapping in time with intense RFI. Asserts true signal correlation $> 0.85$ after nulling.
5. **P5 (Transient Radar/Satellite Burst Nulling):** Intermittent RFI burst. Quiet blocks stay untouched; flared blocks trigger active nulling.

---
*End of Guide*
