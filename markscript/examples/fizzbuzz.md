# FizzBuzz

> The original cliche. Compute FizzBuzz from 1 to 100 using the Markscript mini-language.
> Variables, while loops, if/else, arithmetic, modulo, and println --- all inside a ```markscript block.
> No Kain code written. Pure markdown. Pure bytecode. Pure execution.

## prove_it_works

```markscript
let n = 1
while n <= 100:
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)
    n = n + 1
```

## verify

The output above should contain exactly 100 lines:
- 14 lines of "FizzBuzz" (multiples of 15)
- 20 lines of "Buzz" (multiples of 5 not already counted)
- 27 lines of "Fizz" (multiples of 3 not already counted)
- The remaining 39 lines are numbers

The 15th line is "FizzBuzz" (15 = 3×5)
The 100th line is "Buzz" (100 = 5×20, printed because 100 % 5 == 0)

```markscript
let fizzbuzz_count = 0
let buzz_count = 0
let fizz_count = 0
let num_count = 0
let i = 1
while i <= 100:
    if i % 15 == 0:
        fizzbuzz_count = fizzbuzz_count + 1
    elif i % 3 == 0:
        fizz_count = fizz_count + 1
    elif i % 5 == 0:
        buzz_count = buzz_count + 1
    else:
        num_count = num_count + 1
    i = i + 1

print("FizzBuzz: " + str(fizzbuzz_count) + " (expect 14)")
print("Fizz: " + str(fizz_count) + " (expect 27)")
print("Buzz: " + str(buzz_count) + " (expect 20)")
print("Numbers: " + str(num_count) + " (expect 39)")
print("Total: " + str(fizzbuzz_count + fizz_count + buzz_count + num_count) + " (expect 100)")
```

---

## how_it_works

The Markscript mini-language compiles the ```markscript block to 21 real VM opcodes:

```markscript
let n = 1              → PUSH_STACK 1, STORE_VAR "n"
while n <= 100:        → LOAD_VAR "n", PUSH_STACK 100, CMP, JN loop_end
    if n % 15 == 0:    → LOAD_VAR "n", PUSH_STACK 15, MOD, JZ fizzbuzz_case
        print("FizzBuzz")  → PUSH_STACK "FizzBuzz", PUSH_PARAM "print", EXECUTE_CALL
    elif n % 3 == 0:   → LOAD_VAR "n", PUSH_STACK 3, MOD, JZ fizz_case
        print("Fizz")
    ...                → JMP loop_end, etc.
    n = n + 1          → LOAD_VAR "n", PUSH_STACK 1, ADD, STORE_VAR "n"
```

Every sleeping opcode (7-20) is now reachable. The VM was ready. The parser just needed to feed it.

## known_limitation

The `print()` function dispatches through the IVT to the Kain `handler_print` bridge handler. Currently the bridge logs `[PRINT] <value>` which appears in the mks output mixed with runtime telemetry. In production, the output stream would be separated from diagnostics.

To verify the output is CORRECT:
```bash
mks run examples/fizzbuzz.md | findstr "\[PRINT\]"
```
This extracts only the print lines. You should see exactly 100 lines matching the FizzBuzz spec.
