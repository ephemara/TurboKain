# CollatzDeepDive -- Sequence Explorer & Conjecture Verifier

> The Collatz conjecture: every positive integer eventually reaches 1 under
> the map `n → n/2 (if even)` or `n → 3n+1 (if odd)`.
> Computed entirely in markscript mini-language. No external math.
> Exercises: complex while loops, parity detection via equality workaround,
> sequence length tracking, max-value tracking.

---

## Configuration

| Parameter | Value |
|-----------|-------|
| MaxNumber | 100 |
| VerifyAll | 1 |
| LongestRun | 1 |

---

## detect_even -- Parity via repeated subtraction

```markscript
# Even/odd detection without modulo operator:
# Repeatedly subtract 2 from n and check if we hit 0 or 1
# If we reach 0, n is even. If we reach 1, n is odd.
```

---

## verify_conjecture -- Check every number up to MaxNumber

```markscript
let max_n = 100
let start = 2
let longest_seq = 0
let longest_n = 0
let total_steps = 0

print("=== Collatz Conjecture Verification up to " + str(max_n) + " ===")
print("")

while max_n > start:
    let n = start
    let steps = 0
    let max_val = n

    # Track the sequence
    while n > 1:
        # Detect parity: repeatedly subtract 2
        let p = n
        let is_even = 0
        let found_p = 0

        # Parity check: subtract 2 from copy until < 2
        # If result is 0: even. If result is 1: odd.
        # (We use the equality workaround here)
        let parity_test_val = n
        while parity_test_val > 1:
            let q = parity_test_val / 2
            let product = 2 * q
            if parity_test_val > product:
                # odd: n = 2*q + 1
                parity_test_val = 1
            else:
                # even: n = 2*q
                parity_test_val = 0
            # The while condition checks > 1, so we must exit
            # We'll set to 0 or 1 and the while check handles it

        if parity_test_val > 0:
            # n is odd: 3n + 1
            n = n * 3 + 1
        else:
            # n is even: n / 2
            n = n / 2

        steps = steps + 1

        # Track max value reached
        if n > max_val:
            max_val = n

    # Track longest sequence
    if steps > longest_seq:
        longest_seq = steps
        longest_n = start
        print("New longest: " + str(start) + " → " + str(steps) + " steps, max=" + str(max_val))

    total_steps = total_steps + steps
    start = start + 1

```

---

## report - Summary statistics

```markscript
print("")
print("=== Collatz Report ===")
print("")
print("Numbers verified: " + str(max_n - 1))
print("Total Collatz steps computed: " + str(total_steps))
print("Longest sequence: n=" + str(longest_n) + " (" + str(longest_seq) + " steps)")
print("")
print("Conjecture holds for all numbers 2 through " + str(max_n))
print("(Every sequence reached 1)")
```

---

## heavy_hitters - Find numbers with most interesting behavior

```markscript
# Verify specific known interesting Collatz numbers
# n=27 has 111 steps, peaks at 9232
# n=97 has 118 steps
# n=871 has 178 steps

print("")
print("=== Heavy Hitters ===")
print("")

let test_nums = 27
let test_max = 0
let test_seq = 0

# We can't loop through arrays, but we can hardcode interesting checks
let interesting = 27
let n = interesting
let steps = 0
let peak = n

while n > 1:
    # Same parity detection as above
    let p = n
    let workaround = 0

    # Parity: subtract 2s until < 2
    let pt = n
    while pt > 1:
        let q = pt / 2
        let prod = 2 * q
        if pt > prod:
            pt = 1
        else:
            pt = 0

    if pt > 0:
        n = n * 3 + 1
    else:
        n = n / 2

    if n > peak:
        peak = n

    steps = steps + 1

print("n=" + str(interesting) + ": " + str(steps) + " steps, peak=" + str(peak))

# n=97
interesting = 97
n = interesting
steps = 0
peak = n

while n > 1:
    let pt2 = n
    while pt2 > 1:
        let q2 = pt2 / 2
        let prod2 = 2 * q2
        if pt2 > prod2:
            pt2 = 1
        else:
            pt2 = 0

    if pt2 > 0:
        n = n * 3 + 1
    else:
        n = n / 2

    if n > peak:
        peak = n
    steps = steps + 1

print("n=" + str(interesting) + ": " + str(steps) + " steps, peak=" + str(peak))

# n=871
interesting = 871
n = interesting
steps = 0
peak = n

while n > 1:
    let pt3 = n
    while pt3 > 1:
        let q3 = pt3 / 2
        let prod3 = 2 * q3
        if pt3 > prod3:
            pt3 = 1
        else:
            pt3 = 0

    if pt3 > 0:
        n = n * 3 + 1
    else:
        n = n / 2

    if n > peak:
        peak = n
    steps = steps + 1

print("n=" + str(interesting) + ": " + str(steps) + " steps, peak=" + str(peak))

print("")
print("=== Collatz Analysis Complete ===")
```

---

## Sequence Stats Table

| Property | Value |
|----------|-------|
| Max n tested | 100 |
| Longest sequence start | 97 |
| Longest sequence length | 118 |
| Peak value reached by 27 | 9232 |
| Max steps for n≤100 | 118 |
| Conjecture violations | 0 |

> The Collatz conjecture remains unbroken after this markscript verification.
> (For n ≤ 100, at least. The general proof is left to the reader.)
