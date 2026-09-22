# Operator Proof

> Branching + comparison + modulo operators. Verified by PRINT output
> (asserts can't self-verify until F2 lands, so READ the output).
> Expected output is recorded below — any deviation is a regression.

## elif_chain

```markscript
let e = 2
if e == 1:
    print("one")
elif e == 2:
    print("two")
else:
    print("other")
```

## expected: exactly one line: two

## comparison_matrix

```markscript
if 1 == 1:
    print("eq-true")
else:
    print("eq-FAIL")
if 1 == 2:
    print("ne-FAIL")
else:
    print("ne-true")
if 1 != 2:
    print("neq-true")
else:
    print("neq-FAIL")
if 2 != 2:
    print("neq2-FAIL")
else:
    print("neq2-true")
if 1 < 2:
    print("lt-true")
else:
    print("lt-FAIL")
if 1 <= 1:
    print("lte-true")
else:
    print("lte-FAIL")
if 2 > 1:
    print("gt-true")
else:
    print("gt-FAIL")
if 2 >= 2:
    print("gte-true")
else:
    print("gte-FAIL")
```

## expected: eq-true ne-true neq-true neq2-true lt-true lte-true gt-true gte-true

## modulo_row

```markscript
print(15 % 15)
print(30 % 15)
print(7 % 15)
print(100 % 15)
print(7 % 3)
print(10 % 5)
```

## expected: 0 0 7 10 1 0

## while_lte_row

```markscript
let c = 0
let n = 1
while n <= 5:
    c = c + 1
    n = n + 1
print(c)
print(n)
```

## expected: 5 6
