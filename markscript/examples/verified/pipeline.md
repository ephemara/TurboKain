# Pipeline

Sequential intent execution within a markscript block. Multiple handler
calls in sequence prove the dispatch loop works without stack corruption.

```markscript
print(concat("pipeline", " ", "step1"))
print(concat("pipeline", " ", "step2"))
print(concat("pipeline", " ", "step3"))
print(concat("pipeline", " ", "step4"))
print(concat("pipeline", " ", "step5"))
```

## verify

```markscript
print("pipeline: 5 sequential intents dispatched")
```
