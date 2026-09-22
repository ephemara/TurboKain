# pipeline — TurboKain single entry point

One Kain binary that wraps the stage chain and applies the **artifact guards in
one place** (not hard-coded into every detector). Built with Kain's `use`-module
system (`module_roots`, one file per concern).

## Layout (all in one crate, one exe)

```
kain/pipeline/
  KAIN.toml
  src/
    main.kn      entry + `file` (run stages) + `analyze` (guard staged tables)
    guards.kn    G1 fs/2048 comb · G3 band-edge rolloff · G4 pol triage
    tables.kn    markdown-table reader (shared)
    exec.kn      spawn a tool, verify by artifact (not exit code)
```

## Usage

```bash
# stage + guard a whole sub-band (slice -> xeno -> fam, then guards)
pipeline file <raw> --chan-lo 57 --chan-hi 63 --pols 0 [--work DIR] [--target NAME]

# guard an existing directory of lane tables (no re-scan)
pipeline analyze <workdir> [--target NAME]
```

## Guards (earned by the TRAPPIST-1 0017 investigation)

| guard | detects | evidence |
|---|---|---|
| **G1** frame-clock comb | cyclic peaks on the fs/2^k grid (spacing = seg/2048 bins = fs/2048 Hz) | 0017 ch60: ranks 0-10 exactly 4-bin spaced @SEG=8192 |
| **G3** band-edge rolloff | kurtosis rising toward the sub-band edge (PFB rolloff) | 0017: ch57 0.3 → ch60 59.8 → ch63 71 |
| **G4** pol front-end triage | all pols impulsive → common-mode ingress (1); one rail → hardware failure (2) | 0017 ch60: all four products kurt 18-60 |

## Verdict vocabulary

`CLEAN` · `ARTIFACT-COMB` · `ARTIFACT-EDGE` · `ARTIFACT-COMMON` · `ARTIFACT-RAIL`
· `INTERESTING` (detector fired and no guard explains it).

## Proven

`file`/`analyze` on TRAPPIST-1 0017: detector STRONG on ch60/63 → guards downgrade
to `ARTIFACT-COMMON` (pol) and `ARTIFACT-EDGE`/`ARTIFACT-COMB` (channel). Guard
unit proof: 6/6 (3 positive + 3 negative controls).

## Design rule

Detectors stay standalone exes with byte-identical CLI/CSV contracts. The
pipeline **wraps** them; it does not absorb them. Shared concerns (IO, guards,
table parsing) live in this crate once. When in-process fusion arrives, the
stage calls move from `exec::run_tool` to direct `use`-imports — the module
boundaries are already in place.
