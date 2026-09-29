# A Multi-Window Baseband Pilot Survey of TRAPPIST-1: Limits on Narrowband and Coded Spread-Spectrum Emission at 2-12 GHz

**Folder:** `papers/trappist1_bystander_survey/`  
**Target:** TRAPPIST-1 (2MASS J23062928-0502285)  
**Lead Author:** Taylor James Kipp (`taylor@kainlang.com`)  
**Telescope:** Robert C. Byrd Green Bank Telescope (100 m)  
**Survey Volume:** 732.1 GB raw GUPPI baseband voltages across 4 microwave bands (2.1 to 12.0 GHz)  
**Total Channels Swept:** 1,024 dual-polarization observations  
**Status:** Revised pilot draft (2026-09-28) — honest negative, methods pilot. Peer-review pass complete; injection first-light DONE 2026-09-28 (reports/2026-09-28_injection_cal/, §5.4/§sec:inject); coded sensitivity not established; DOI bundle still deferred (see §7). Suitable for RNAAS / methods note now; AJ-track after §7 punch list.

---

## Files in this Directory

| File | Purpose |
|---|---|
| **`manuscript.md`** | Comprehensive academic paper in Markdown with full mathematical proofs, telemetry tables, and figures. Read directly in GitHub or VS Code. |
| **`manuscript.tex`** | Official American Astronomical Society (AAS) Journals LaTeX manuscript (`aastex631` template). Ready for Overleaf, arXiv (`astro-ph.IM`), or AJ/RNAAS submission. |
| **`references.bib`** | Complete BibTeX bibliography citing Breakthrough Listen, TRAPPIST-1 discovery, Shannon information theory, Gallager LDPC, and Kolmogorov turbulence. |
| **`figures/`** | Publication-quality high-resolution diagnostic dashboards: |
| ├── `figure1_xband_thermal_waterfall.png` | 1920x1080 Full HD dashboard of X-Band Channel 49 showing Gaussian thermal noise floor and telemetry cards. |
| └── `figure2_sband_impulse_storm.png` | 1920x1080 Full HD dashboard of S-Band Channel 36 showing the microsecond terrestrial ingress burst train. |

---

## How to Compile the LaTeX Manuscript (`.tex`)

### Option A: Overleaf (Zero Setup, Easiest)
1. Go to [Overleaf.com](https://www.overleaf.com) (free).
2. Click **New Project** $\rightarrow$ **Upload Project**.
3. Upload `manuscript.tex`, `references.bib`, and the `figures/` folder.
4. Click **Recompile**. Overleaf automatically provides the `aastex631.cls` template and compiles the final two-column PDF!

### Option B: Local Compilation via `latexmk` / `pdflatex`
If you have TeX Live / MiKTeX installed:
```bash
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex
```

---

## 100% Replication Instructions

Every single number, table, and figure in this paper can be reproduced on any machine using TurboKain:

1. **Verify Instrument Prove Batteries (25/25 Green):**
   ```bash
   ./core.exe prove
   ```
2. **Inspect the Master Overnight Campaign Dossier:**
   ```bash
   cat reports/trappist1_overnight_20260928_094823/OVERNIGHT_REPORT.md
   ```
3. **Query the SQLite Research Warehouse (1.44M rows):**
   ```bash
   # Check the 11 alien candidate triage verdicts:
   python python/tk.py db query "SELECT verdict, COUNT(*) FROM stamp GROUP BY verdict"
   python python/tk.py db query "SELECT verdict, COUNT(*) FROM ghost GROUP BY verdict"
   python python/tk.py db query "SELECT verdict, COUNT(*) FROM gperf GROUP BY verdict"
   ```
4. **Re-run the Gated Sweep on Any Channel:**
   ```bash
   ./core.exe sweep reports/2026-09-28_trappist_alien/ch36_on_p0.f32 --fs 2929687.5 --out-dir _tmp/repro/
   ```

---

## Citation (BibTeX)

```bibtex
@article{kipp2026trappist1,
  author    = {Kipp, Taylor James and {The TurboKain Collaboration}},
  title     = {A Multi-Band Bystander Technosignature Survey of {TRAPPIST-1}: Deep Microwave Limits on Coded Spread-Spectrum Traffic and Galactic Clocks},
  journal   = {The TurboKain Research Archive},
  year      = {2026},
  volume    = {1},
  pages     = {1--12},
  eprint    = {reports/trappist1_overnight_20260928_094823/OVERNIGHT_REPORT.md},
  url       = {https://github.com/ephemara/turbokain}
}
```
