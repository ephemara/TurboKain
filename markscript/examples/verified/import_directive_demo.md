# Import Directive Demo

Demonstrates @import resolution for multi-file composition.
Imports are resolved at compile time before bytecode emission.

---

## Local Import

@import "hello.md"

---

## Reuse Imported Content

The imported file's domains, routines, and tables are merged
into the calling namespace. Below we reference content that
should be available after import resolution.

> print "import demo: file composition via @import"

---

## Nested Import Proof

@import "math_ops.md"

---

## Verify

```markscript
print("import_directive_demo: @import resolution tested")
```
