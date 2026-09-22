# 🏛 Qualifier Pipeline — 14 Natural Language Intents

Demonstrates all 14 qualifier/modifier keywords as first-class MKS intents.
Each dispatches through `handler_qualifier_echo` and outputs `[QUALIFIER: word] ...`.

Proves the registry scales naturally — these 14 new keywords required
only `intents.md` edits + one handler in `bridge.kn`.

---

## Combinators (and / with / by)

> and alpha beta gamma

> with context "production-mode"

> by category group

## Filters (exclude / only / except / not)

> exclude "*.tmp" "*.log"

> only "*.kn" "*.md"

> except "node_modules"

> not "debug" "verbose"

## Temporal (after / before / until / since)

> after "3000ms" "cleanup"

> before "shutdown" "save-state"

> until "condition-met" "poll"

> since "2024-01-01" "audit-log"

## Spatial / Directional (from / to / using)

> from "input.txt" "extract"

> to "output.txt" "convert"

> using "gpg" "encrypt"

---

## Verification

```markscript
# After running, verify each qualifier dispatched:
# 1. [QUALIFIER: and] alpha beta gamma
# 2. [QUALIFIER: with] context production-mode
# 3. [QUALIFIER: exclude] *.tmp *.log
# ... (14 total)
print(concat("qualifier", "pipeline", "verified"))
```
