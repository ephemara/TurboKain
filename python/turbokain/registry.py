"""Tool registry — the one place that knows where the Kain exes live and how
they expect to be called.

Detectors keep their own byte-identical CLI contracts (see AGENTS.md). This
registry is a *description* of those contracts, not a reimplementation:

  * ``input_kind`` tells the scan driver what the tool consumes
    (raw GUPPI, ``.f32`` time series, ``.fil``, ``.bin`` bitstream, tables).
  * ``selftest`` is the argv that triggers the tool's built-in prove harness,
    or ``None`` when the tool has no self-test flag (slice / sk_gate /
    fold_sum / fam_god are prove-by-run-with-known-data).
  * ``in_flag`` / ``out_flag`` are how the scan driver feeds one stage into
    the next. Positional-only tools set ``in_flag=None``.

Nothing here hardcodes a drive letter: everything is repo-relative, resolved
at load time.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Tool:
    """A single native Kain executable and its CLI contract."""

    name: str
    exe: str  # repo-relative path to the .exe
    kind: str  # ingest | detector | gate | bridge | driver | sandbox | config | template
    input_kind: str  # raw | f32 | fil | bits | table | none
    selftest: tuple[str, ...] | None = None
    in_flag: str | None = "--in"  # None => positional input
    out_flag: str | None = "--out"
    csv_flag: str | None = None
    appends_ext: bool = False  # True => tool appends .md/.csv to a bare --out stem itself
    fs_flag: str | None = "--fs"
    note: str = ""

    def resolve(self, root: Path) -> Path:
        return (root / self.exe).resolve()

    @property
    def stem(self) -> str:
        return Path(self.exe).stem


# ---------------------------------------------------------------------------
# Registry. One row per exe we intend to wrap. Update when a tool is added.
# ---------------------------------------------------------------------------
_TOOLS: list[Tool] = [
    # -- ingest -------------------------------------------------------------
    Tool(
        "slice",
        "kain/core/slice.exe",
        "ingest",
        "raw",
        selftest=None,
        in_flag="--in",
        out_flag="--out",
        fs_flag=None,
        note="GUPPI raw -> per-chan/pol .f32. Probe-only when no --out.",
    ),
    Tool(
        "fil_reader",
        "kain/core/fil_reader.exe",
        "ingest",
        "fil",
        selftest=("--prove",),
        out_flag="--out",
        fs_flag=None,
        note="Sigproc .fil -> .f32 (nbits 32/8/16, nifs=1).",
    ),
    Tool(
        "h5_reader",
        "kain/core/h5_reader.exe",
        "ingest",
        "h5",
        selftest=("--prove",),
        out_flag="--out",
        fs_flag=None,
        note="BL HDF5 filterbank -> .f32 (bitshuffle/gzip, nbits 32/8/16).",
    ),
    # -- detectors over .f32 ------------------------------------------------
    Tool(
        "sk_gate",
        "kain/core/sk_gate.exe",
        "detector",
        "f32",
        selftest=None,
        out_flag="--out",
        csv_flag="--csv",
        fs_flag=None,
        note="Spectral-kurtosis anomaly gate.",
    ),
    Tool(
        "boxcar_bank",
        "kain/core/boxcar_bank.exe",
        "detector",
        "f32",
        selftest=("--prove",),
        out_flag="--out",
        appends_ext=True,  # --out <stem> -> <stem>.md + <stem>.csv by itself
        note="DM sweep + boxcar pulse search.",
    ),
    Tool(
        "fold_sum",
        "kain/core/fold_sum.exe",
        "detector",
        "f32",
        selftest=None,
        out_flag="--out",
        csv_flag="--csv",
        note="Periodicity fold + 8-harmonic sum.",
    ),
    Tool(
        "fam_god",
        "kain/core/fam_god.exe",
        "detector",
        "f32",
        selftest=None,
        out_flag="--out",
        csv_flag="--csv",
        note="Cyclostationary fingerprint + recurring-target journal.",
    ),
    Tool(
        "frft_hunt",
        "kain/core/frft_hunt.exe",
        "detector",
        "f32",
        selftest=("--prove",),
        out_flag="--out",
        csv_flag="--csv",
        note="Coherent fast Fractional Fourier Transform chirp matched filter (O(N log N)).",
    ),
    Tool(
        "perm_entropy",
        "kain/core/perm_entropy.exe",
        "detector",
        "f32",
        selftest=("--prove",),
        out_flag="--out",
        csv_flag="--csv",
        note="Model-free Permutation Entropy & LZW Complexity screener (O(N)).",
    ),
    Tool(
        "subspace_null",
        "kain/core/subspace_null.exe",
        "detector",
        "f32",
        selftest=("--prove",),
        in_flag=None,
        out_flag="--out",
        csv_flag="--csv",
        note="Baseband spatial subspace RFI nulling & phase preservation (M=2, RBSPE).",
    ),
    Tool(
        "drift_hunt",
        "kain/core/drift_hunt.exe",
        "detector",
        "f32",
        selftest=("--prove",),
        out_flag="--out",
        csv_flag="--csv",
        note="De-Doppler tone search (STFT + shift-add).",
    ),
    Tool(
        "frame_hunt",
        "kain/core/frame_hunt.exe",
        "detector",
        "f32",
        selftest=("--prove",),
        out_flag="--out",
        csv_flag="--csv",
        note="M2 frame hunter (envelope + harmonic family).",
    ),
    Tool(
        "xeno_scan",
        "kain/core/xeno_scan.exe",
        "detector",
        "f32",
        selftest=("--selftest",),
        out_flag="--out",
        csv_flag="--csv",
        note="Microscopic battery (SK + coherence + cepstral + DM-order).",
    ),
    Tool(
        "lag_hunt",
        "kain/core/lag_hunt.exe",
        "detector",
        "f32",
        selftest=("--prove",),
        out_flag="--out",
        csv_flag="--csv",
        note="M2 long-lag direct autocorrelation (PHASE/POWER/CADENCE/EVENT lenses).",
    ),
    Tool(
        "jerk_track",
        "kain/core/jerk_track.exe",
        "detector",
        "f32",
        selftest=("--prove",),
        out_flag="--out",
        csv_flag=None,
        appends_ext=True,
        note="Viterbi dynamic programming trellis for non-linear Doppler & orbital acceleration.",
    ),
    Tool(
        "scint_pol",
        "kain/core/scint_pol.exe",
        "detector",
        "f32",
        selftest=("--prove",),
        out_flag="--out",
        csv_flag=None,
        appends_ext=True,
        note="Interstellar diffractive scintillation decorrelation & polarization coherence.",
    ),
    Tool(
        "stack",
        "kain/core/stack.exe",
        "detector",
        "f32",
        selftest=("--prove",),
        out_flag="--out",
        csv_flag="--csv",
        note="Incoherent multi-epoch ON/OFF power stacker (sqrt-N gain).",
    ),
    # -- bridges ------------------------------------------------------------
    Tool(
        "bitslice",
        "kain/core/bitslice.exe",
        "bridge",
        "f32",
        selftest=("--prove",),
        out_flag="--out",
        fs_flag="--fs",
        note=".f32 -> xvm bitstreams (sign/diff/mag).",
    ),
    Tool(
        "raster_hunt",
        "kain/core/raster_hunt.exe",
        "payload",
        "bits",
        selftest=("--prove",),
        out_flag="--out",
        csv_flag="--csv",
        note="2D payload framing & pictogram spatial autocorrelation (M8).",
    ),
    Tool(
        "xvm_sandbox",
        "kain/core/xvm_sandbox.exe",
        "sandbox",
        "bits",
        selftest=("--selftest",),
        in_flag="--in",
        out_flag=None,
        fs_flag=None,
        note="TAG/converge sandbox over a bit payload.",
    ),
    # -- gates --------------------------------------------------------------
    Tool(
        "cadence_pair",
        "kain/core/cadence_pair.exe",
        "gate",
        "table",
        selftest=None,
        in_flag=None,
        out_flag=None,
        fs_flag=None,
        note="ON/OFF cadence gate over two lane tables (--on / --off).",
    ),
    # -- config -------------------------------------------------------------
    Tool(
        "config",
        "kain/core/config.exe",
        "config",
        "none",
        selftest=("--prove",),
        in_flag=None,
        out_flag=None,
        fs_flag=None,
        note="Preset/header/CLI resolver (40 keys).",
    ),
    # -- report -------------------------------------------------------------
    Tool(
        "unify",
        "kain/core/unify.exe",
        "report",
        "dir",
        selftest=("--prove",),
        in_flag="--dir",
        out_flag="--out",
        csv_flag="--csv",
        fs_flag=None,
        note="Campaign report unifier: tables -> REPORT.md + evidence.csv + verdicts.json.",
    ),
    # -- visualization ------------------------------------------------------
    Tool(
        "waterfall",
        "kain/core/waterfall.exe",
        "detector",
        "f32",
        selftest=("--prove",),
        in_flag="--in",
        out_flag="--out",
        fs_flag="--fs",
        note="Multi-panel 1920x1080 scientific diagnostic waterfall PNG generator.",
    ),
    # -- suite / portable core ----------------------------------------------
    Tool(
        "core",
        "core.exe",
        "suite",
        "none",
        selftest=None,
        in_flag=None,
        out_flag=None,
        fs_flag=None,
        note="Portable core executable containing all 14 tools amalgamated.",
    ),
    # -- examples (kept wrapped so the prove battery is uniform) -----------
    Tool(
        "lane_sieve",
        "kain/_examples/lane_sieve.exe",
        "template",
        "none",
        selftest=(),  # runs its self-check with no argv
        in_flag=None,
        out_flag=None,
        fs_flag=None,
        note="Example 01: converge spec vs AVX2 lane mold.",
    ),
]


@dataclass
class Registry:
    root: Path
    tools: dict[str, Tool] = field(default_factory=dict)
    missing: list[str] = field(default_factory=list)
    unregistered: list[Path] = field(default_factory=list)

    def get(self, name: str) -> Tool:
        key = name.lower()
        if key in self.tools:
            return self.tools[key]
        # allow `boxcar_bank.exe` / path stems
        stem = Path(name).stem.lower()
        for tool in self.tools.values():
            if tool.stem.lower() == stem:
                return tool
        raise KeyError(f"unknown tool: {name!r} (try `tk list`)")

    def names(self) -> list[str]:
        return sorted(self.tools)

    def by_kind(self, kind: str) -> list[Tool]:
        return [t for t in self.tools.values() if t.kind == kind]

    def discover(self, extra_globs: Iterable[str] = ("kain/**/*.exe",)) -> None:
        """Flag exes on disk that are not in the registry (drift detector)."""
        seen = {Path(t.exe).name for t in self.tools.values()}
        found: set[Path] = set()
        for pat in extra_globs:
            found |= {p.resolve() for p in self.root.glob(pat)}
        self.unregistered = sorted(
            p for p in found if p.name not in seen and ".kain" not in p.parts
        )


CORE_TOOLS: set[str] = {
    "bitslice",
    "boxcar_bank",
    "cadence_pair",
    "config",
    "drift_hunt",
    "fam_god",
    "fil_reader",
    "fold_sum",
    "frame_hunt",
    "frft_hunt",
    "lag_hunt",
    "perm_entropy",
    "sk_gate",
    "slice",
    "subspace_null",
    "unify",
    "waterfall",
    "xeno_scan",
    "xvm_sandbox",
}


def load_registry(root: Path) -> Registry:
    reg = Registry(root=root)
    core_exe = None
    for cand in [
        root / "turbokain_core.exe",
        root / "turbokain.exe",
        root / "core.exe",
        root / "kain" / "turbokain_core.exe",
        root / "kain" / "core.exe",
        root / "kain" / "core" / "core.exe",
    ]:
        if cand.exists():
            core_exe = cand
            break

    for tool in _TOOLS:
        if tool.resolve(root).exists() or (core_exe is not None and tool.name in CORE_TOOLS):
            reg.tools[tool.name] = tool
        else:
            reg.missing.append(tool.name)
    # aliases so old names still resolve (`fam` -> `fam_god`)
    alias = {"fam": "fam_god", "boxcar": "boxcar_bank"}
    for a, target in alias.items():
        if target in reg.tools:
            reg.tools.setdefault(a, reg.tools[target])
    reg.discover()
    return reg
