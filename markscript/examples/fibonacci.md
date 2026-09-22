# Fibonacci

> Compute the Fibonacci sequence using the Markscript mini-language.
> Variables, while loops, arithmetic, and string formatting --- all inside a ```markscript block.

## compute_fib

```markscript
let n = 20
let a = 0
let b = 1
let i = 0
while i < n:
    let temp = a + b
    a = b
    b = temp
    i = i + 1
print("Fibonacci(" + str(n) + ") = " + str(a))
```

## verify_sequence

The first 20 Fibonacci numbers are:
0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181

Fibonacci(0) = 0, Fibonacci(1) = 1, ..., Fibonacci(20) = 6765

```markscript
let fib_n = 20
let fib_a = 0
let fib_b = 1
let fib_i = 1
while fib_i <= fib_n:
    let fib_next = fib_a + fib_b
    fib_a = fib_b
    fib_b = fib_next
    fib_i = fib_i + 1

if fib_a == 6765:
    print("VERIFIED: Fibonacci(20) = " + str(fib_a) + " ✓")
else:
    print("FAILED: Fibonacci(20) = " + str(fib_a) + " (expected 6765)")
```

## bigger_numbers

```markscript
let nth = 30
let fa = 0
let fb = 1
let fi = 1
while fi <= nth:
    let fc = fa + fb
    fa = fb
    fb = fc
    fi = fi + 1
print("Fibonacci(" + str(nth) + ") = " + str(fa))
```

Fibonacci(30) = 832040. Run the compute above and verify the output.

---

## the_cliche

Every language tutorial needs a Fibonacci demo. Markscript's is inside a fenced code block
inside a markdown file that compiles to bytecode that runs on a stack VM written in Kain
compiled through LLVM to native machine code.

**Your documentation is your program.** This file proves it.
