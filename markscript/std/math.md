# Math

Markscript arithmetic --- computation and numeric utilities.
Uses the markscript mini-language for direct bytecode operations (no IVT dispatch
needed for basic arithmetic -- it compiles to OP_ADD, OP_SUB, OP_MUL, OP_DIV).

---

## add

Add two numbers. Pure computation --- no IVT dispatch needed.

```markscript
let a = 5
let b = 3
let result = a + b
# result = 8
```

---

## subtract

Subtract b from a.

```markscript
let a = 10
let b = 4
let result = a - b
# result = 6
```

---

## multiply

Multiply two numbers.

```markscript
let a = 7
let b = 6
let result = a * b
# result = 42
```

---

## divide

Divide a by b. Traps if b is zero.

```markscript
let a = 100
let b = 5
let result = a / b
# result = 20
```

---

## chained_ops

Multiple operations in sequence.

```markscript
let x = 2
let y = 3
let z = 4
let result = (x + y) * z
# result = 20
```

---

## negate

Negate a value (multiply by -1 to flip sign).

```markscript
let x = 42
let neg = 0 - x
# neg = -42
```

---

## increment

Increment a counter.

```markscript
let count = 0
count = count + 1
count = count + 1
count = count + 1
# count = 3
```

---

## decrement

Decrement a counter.

```markscript
let count = 10
count = count - 1
count = count - 1
# count = 8
```

---

## linear

Compute a linear equation: y = mx + b.

```markscript
let m = 2
let x = 5
let b = 3
let y = m * x + b
# y = 13
```

---

## average

Average three numbers.

```markscript
let a = 10
let b = 20
let c = 30
let sum = a + b + c
let avg = sum / 3
# avg = 20
```
