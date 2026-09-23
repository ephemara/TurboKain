# scripts/make_waterfall_examples.py
import numpy as np
import subprocess
import os

os.makedirs("docs/waterfall_examples", exist_ok=True)
os.makedirs("_tmp/examples", exist_ok=True)

FS = 2929687.5  # 2.9297 MHz
N = 1048576 * 2 # ~2.1 million samples (~0.71 seconds at full rate, or simulated span)
t = np.arange(N) / FS

print(f"Synthesizing test scenarios (N={N} samples)...")

# -----------------------------------------------------------------------------
# Scenario 1: Proxima Centauri b (Narrowband Drifting Extraterrestrial Carrier)
# -----------------------------------------------------------------------------
print("[1/5] Synthesizing Proxima Centauri b (Drifting Narrowband Carrier)...")
# Noise baseline
noise1 = np.random.normal(0, 1.0, N).astype(np.float32)
# Drifting carrier: f0 = +250 kHz, drift = -50 kHz across scan
f_start = 250000.0
drift_rate = -50000.0 / (N / FS)
phase1 = 2 * np.pi * (f_start * t + 0.5 * drift_rate * t**2)
carrier = 1.5 * np.cos(phase1).astype(np.float32)
sig1 = noise1 + carrier
f32_path1 = "_tmp/examples/proxima_b.f32"
sig1.tofile(f32_path1)

png_path1 = "docs/waterfall_examples/01_proxima_b_drifting_carrier_turbo.png"
cmd1 = [
    "./tkc.exe", "waterfall",
    "--in", f32_path1,
    "--out", png_path1,
    "--target", "PROXIMA_CENTAURI_B",
    "--freq-mhz", "1420.4057",
    "--fs", str(FS),
    "--cmap", "turbo"
]
subprocess.run(cmd1, check=True)
print(f"  -> Generated {png_path1}")

# -----------------------------------------------------------------------------
# Scenario 2: Pulsar PSR B0329+54 (Periodic Pulse Train in Inferno)
# -----------------------------------------------------------------------------
print("[2/5] Synthesizing PSR B0329+54 (Periodic Pulsar Pulses)...")
noise2 = np.random.normal(0, 1.0, N).astype(np.float32)
# Pulse period P0 ~ 0.15s in this simulated window
pulse_period_samples = int(0.12 * FS)
pulse_width_samples = int(0.005 * FS)
pulses = np.zeros(N, dtype=np.float32)
for p_idx in range(0, N, pulse_period_samples):
    p_end = min(p_idx + pulse_width_samples, N)
    # broadband pulsed burst
    pulses[p_idx:p_end] += np.random.normal(0, 4.0, p_end - p_idx).astype(np.float32)

sig2 = noise2 + pulses
f32_path2 = "_tmp/examples/psr_b0329.f32"
sig2.tofile(f32_path2)

png_path2 = "docs/waterfall_examples/02_psr_b0329_periodic_pulses_inferno.png"
cmd2 = [
    "./tkc.exe", "waterfall",
    "--in", f32_path2,
    "--out", png_path2,
    "--target", "PSR_B0329+54",
    "--freq-mhz", "1400.0",
    "--fs", str(FS),
    "--cmap", "inferno"
]
subprocess.run(cmd2, check=True)
print(f"  -> Generated {png_path2}")

# -----------------------------------------------------------------------------
# Scenario 3: Terrestrial RFI Comb Interference (Non-Gaussian SK Bursts)
# -----------------------------------------------------------------------------
print("[3/5] Synthesizing Terrestrial RFI Comb (Clock lines & high SK)...")
noise3 = np.random.normal(0, 1.0, N).astype(np.float32)
# Stationary zero-drift carriers at -600 kHz, 0 Hz, +600 kHz
rfi_tones = (
    1.2 * np.cos(2 * np.pi * 600000.0 * t) +
    1.8 * np.cos(2 * np.pi * (-600000.0) * t) +
    2.5 * np.cos(2 * np.pi * 10000.0 * t)
).astype(np.float32)
# Intermittent duty cycle (causing high spectral kurtosis)
mask = (np.sin(2 * np.pi * 8.0 * t) > 0.3).astype(np.float32)
sig3 = noise3 + rfi_tones * mask
f32_path3 = "_tmp/examples/rfi_comb.f32"
sig3.tofile(f32_path3)

png_path3 = "docs/waterfall_examples/03_terrestrial_rfi_comb_turbo.png"
cmd3 = [
    "./tkc.exe", "waterfall",
    "--in", f32_path3,
    "--out", png_path3,
    "--target", "RFI_LOCAL_OSCILLATOR",
    "--freq-mhz", "1420.0",
    "--fs", str(FS),
    "--cmap", "turbo"
]
subprocess.run(cmd3, check=True)
print(f"  -> Generated {png_path3}")

# -----------------------------------------------------------------------------
# Scenario 4: Fast Radio Burst FRB 121102 (Dispersed Quadratic Chirp)
# -----------------------------------------------------------------------------
print("[4/5] Synthesizing FRB 121102 (Dispersed Frequency Sweep)...")
noise4 = np.random.normal(0, 1.0, N).astype(np.float32)
# Quadratic chirp sweeping from +800 kHz down to -800 kHz
f0_chirp = 800000.0
f1_chirp = -800000.0
T_span = N / FS
k_chirp = (f1_chirp - f0_chirp) / (T_span**2)
chirp_phase = 2 * np.pi * (f0_chirp * t + (k_chirp / 3.0) * t**3)
# Burst envelope localized in time
t_center = 0.5 * T_span
envelope = np.exp(-((t - t_center) / 0.15)**2).astype(np.float32)
chirp_sig = 2.8 * np.cos(chirp_phase).astype(np.float32) * envelope

sig4 = noise4 + chirp_sig
f32_path4 = "_tmp/examples/frb_121102.f32"
sig4.tofile(f32_path4)

png_path4 = "docs/waterfall_examples/04_frb_121102_dispersed_chirp_inferno.png"
cmd4 = [
    "./tkc.exe", "waterfall",
    "--in", f32_path4,
    "--out", png_path4,
    "--target", "FRB_121102_REPEATER",
    "--freq-mhz", "1420.0",
    "--fs", str(FS),
    "--cmap", "inferno"
]
subprocess.run(cmd4, check=True)
print(f"  -> Generated {png_path4}")

# -----------------------------------------------------------------------------
# Scenario 5: Real Sky Data (Galactic Center Sgr A* / Unified Demo Scan)
# -----------------------------------------------------------------------------
print("[5/5] Processing Real Sky Data from Archive (Sgr A* Galactic Center)...")
sky_f32 = "reports/2026-09-23_unified_demo_scan/ch32_p0.f32"
if os.path.exists(sky_f32):
    png_path5 = "docs/waterfall_examples/05_sgr_a_star_real_sky_inferno.png"
    cmd5 = [
        "./tkc.exe", "waterfall",
        "--in", sky_f32,
        "--dir", "reports/2026-09-23_unified_demo_scan",
        "--out", png_path5,
        "--target", "SGR_A_STAR_CORE",
        "--freq-mhz", "1420.0",
        "--fs", str(FS),
        "--cmap", "inferno"
    ]
    subprocess.run(cmd5, check=True)
    print(f"  -> Generated {png_path5}")

print("All 5 waterfall examples generated successfully in docs/waterfall_examples/!")
