# Error Recovery

Deliberately trigger unknown intents and verify the file still completes.
MKS error recovery ensures a bad intent does not poison the entire run.

## valid_section_before
> concat "valid" "before"

## triggering_unknown
> nonexistent_intent_phrase_xyzzy
> also_not_real_handler

## valid_section_after
> upper "recovered"

## verify

```markscript
print("error_recovery: file completed despite unknown intents")
```
