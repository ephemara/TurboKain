# Shell Pipeline

Cross-language orchestration simulation via markscript handler calls.
Demonstrates multi-step pipeline execution.

```markscript
print(concat("build", "_", "config"))
print(upper("config_validated"))
print(lower("EXECUTE_PHASE"))
print(concat("status", ":", " ", "ok"))
```

## verify

```markscript
print("shell_pipeline: cross-language pipeline complete")
```
