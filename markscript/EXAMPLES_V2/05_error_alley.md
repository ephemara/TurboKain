# Error Alley

> The spec's boldest claim: markdown has NO syntax errors — the only errors
> are runtime errors (name not found, arity mismatch, bounds violation,
> import failure). This file proves each class: every section must COMPILE
> clean and fail ONLY at exec, gracefully (no crash, proper error text).

## arity_mismatch

```markscript
let am = 10
```

> min 5
> print "arity row done"

## unknown_name

> frobnicate wildly
> print "unknown row done"

## div_by_zero

```markscript
let dz = 1
let dzr = dz / 0
print(dzr)
```

> print "divzero row done"

## assert_failure

```markscript
let af = 1 + 1
```

> assert af 3
> print "assert row done"

## import_failure

> import /definitely/not/a/real/module.kn

> print "ERROR ALLEY DONE"
