# FirstLight — TurboKain 8-tool campaign

All eight tools, one file, one run log. Probe target (fast): blc00 274 MB.
Slice chan 44 pol 0 blocks 0-1, every detector on the slice, xvm selftest,
cadence on the first-light ON/OFF pair. Markdown IS the run log.

## Slice

> slice the probe file chan 44

> run "D:/TurboKain/kain/core/slice.exe E:/SetiYeti/data/blc00_probe.raw 44 D:/TurboKain/_tmp/camp.f32 2 --pol 0"

| leg | file | chan | pol | blocks |
|---|---|---|---|---|
| probe | blc00_probe.raw | 44 | 0 | 2 |

## Gates

> run every detector on the slice

> run "D:/TurboKain/kain/core/sk_gate.exe --in D:/TurboKain/_tmp/camp.f32 --out D:/TurboKain/_tmp/camp_sk.md"
> run "D:/TurboKain/kain/core/boxcar_bank.exe --in D:/TurboKain/_tmp/camp.f32 --out D:/TurboKain/_tmp/camp_pulse"
> run "D:/TurboKain/kain/core/fold_sum.exe --in D:/TurboKain/_tmp/camp.f32 --out D:/TurboKain/_tmp/camp_fold.md"
> run "D:/TurboKain/kain/core/fam_god.exe --in D:/TurboKain/_tmp/camp.f32 --out D:/TurboKain/_tmp/camp_fam.md"

## Micro

> run the microscopic battery on the slice

> run "D:/TurboKain/kain/core/xeno_scan.exe --in D:/TurboKain/_tmp/camp.f32 --out D:/TurboKain/_tmp/camp_xeno.md"

## Sandbox

> prove the alien-code battery (no bits tool yet — selftest exercises all machines)

> run "D:/TurboKain/kain/core/xvm_sandbox.exe --selftest"

## Cadence

> gate the first-light ON/OFF struct pair (needs a pair — single probe file cannot promote)

> run "D:/TurboKain/kain/core/cadence_pair.exe --on D:/TurboKain/reports/2026-09-22_first-light/sk_on.md --off D:/TurboKain/reports/2026-09-22_first-light/sk_off.md --out D:/TurboKain/_tmp/camp_cad.md"

## Verify

> confirm every artifact landed

> file exists "D:/TurboKain/_tmp/camp.f32"
> file exists "D:/TurboKain/_tmp/camp_sk.md"
> file exists "D:/TurboKain/_tmp/camp_fold.md"
> file exists "D:/TurboKain/_tmp/camp_fam.md"
> file exists "D:/TurboKain/_tmp/camp_xeno.md"
> file exists "D:/TurboKain/_tmp/camp_cad.md"
> print "FirstLight complete: 8 tools, one log"
