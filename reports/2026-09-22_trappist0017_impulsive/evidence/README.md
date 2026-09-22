# Evidence — TRAPPIST-1 0017 impulsive structure

Everything cited in `../REPORT.md` is here, self-contained.

## Layout

```
evidence/
  measurements.tsv          one row per slice: n, distinct, sd, kurt, tail,
                            spike count/rate, burst count/rate, phase-mod-8 chi2,
                            burst-train top periods
  persistence_per_block.tsv per 128-block persistence: blocks with maxz>20,
                            min/median/max per-block maxz
  value_histograms.tsv      top-8 value frequencies per slice
  tables/                   the detector tables that triggered (from the sweep)
  slices/                   the .f32 voltage slices (256 MB each) + .slice.log
  scripts/analyze.py        regenerates the three .tsv files from slices/
```

## The comparison set (14 slices)

Channel 60 and 63 across the presence matrix:

| tag | file | freq |
|---|---|---|
| on0017_blc04_0000 | TRAPPIST1_0017.0000 (E:) | 1407.7 MHz |
| on0017_blc04_0001 | TRAPPIST1_0017.0001 (D:) | 1407.7 MHz |
| on0017_blc00 | TRAPPIST1_0017 (blc00) | 2157.7 MHz |
| on0017_blc01 | TRAPPIST1_0017 (blc01) | 1970.2 MHz |
| on0015_blc04 | TRAPPIST1_0015 (ON) | 1407.7 MHz |
| off0016_blc04 | TRAPPIST1_OFF_0016 | 1407.7 MHz |
| off0018_blc04 | TRAPPIST1_OFF_0018 | 1407.7 MHz |

## Regenerate

```bash
python3 scripts/analyze.py slices .
```

`.f32` slices are regenerable from the raw GUPPI files via `kain/core/slice.exe`
(commands in each `slices/*.slice.log`). Raw files are on `/d/data/raw/` and
`E:/SetiYeti/data/`.
