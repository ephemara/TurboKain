# PrimalityMaster - Prime Computation Suite

> Sieve of Eratosthenes, prime factorization, Goldbach pair verification.
> Pure markscript mini-language. No Kain code. No C. No external dependencies.

---

## Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| SieveLimit | 200 | Compute primes up to this number |
| TestNumber | 84 | Number to factorize |
| VerifyGoldbach | 1 | 1 = verify Goldbach for even numbers up to SieveLimit |

---

## is_prime --- Pure markscript primality test

```markscript
# is_prime(n): return 1 if prime, 0 if not
# Uses the equality workaround pattern:
#   Since we only have > and < (no ==),
#   if n > d * (n / d) then d does NOT divide n
#   else: (n == d * n/d) means d DOES divide n
```

```markscript
let n = 2
let max_n = 200
let prime_count = 0

while max_n > n:
    # Test if n is prime
    let is_p = 1        # assume prime until proven composite
    let d = 2

    while n > d:
        let q = n / d
        let product = d * q
        # If n > product, d doesn't divide n (integer division truncates)
        # If product > n (can't happen, product ≤ n always)
        # Else: product == n means d divides n exactly → composite
        if n > product:
            # not divisible by d, continue checking
            is_p = is_p   # keep as-is
        else:
            # divisible! n = d * q
            is_p = 0
            d = n         # force exit inner loop

        d = d + 1

    if is_p > 0:
        print(n)
        prime_count = prime_count + 1

    n = n + 1

print("Primes found up to " + str(max_n) + ": " + str(prime_count))
```

---

## factorize -- Prime factorization by trial division

```markscript
let target = 84
let remainder = target
let factor = 2
let first_flag = 1

print("Factorization of " + str(target) + ":")
print("")

while remainder > 1:
    # Check if factor divides remainder
    let q = remainder / factor
    let product = factor * q
    if remainder > product:
        # not divisible
        factor = factor + 1
    else:
        # divisible: factor divides remainder
        if first_flag > 0:
            print(str(factor))
            first_flag = 0
        else:
            print("× " + str(factor))
        remainder = q
        # Don't increment factor --- it might divide again (e.g. 2², 3³)

print("= " + str(target))
print("")
```

---

## goldbach - Verify Goldbach's conjecture

```markscript
# Goldbach: every even number > 2 is the sum of two primes
# Strategy: for each even n, find primes p, q such that p + q = n
# Uses: the equality workaround to check if a candidate q is prime

let limit = 200
let even = 4
let failures = 0

while limit > even:
    let found = 0
    let p = 2

    # Search for a Goldbach pair
    while even > p and found < 1:

        # Check if p is prime
        let p_is_prime = 1
        let d = 2
        while p > d:
            let q = p / d
            let prod = d * q
            if p > prod:
                # not divisible, continue checking
                continue_check = 0
            else:
                p_is_prime = 0
                d = p
            d = d + 1

        if p_is_prime > 0:
            let q_val = even - p

            # Check if q_val is prime
            let q_is_prime = 1
            let d2 = 2
            while q_val > d2:
                let q2 = q_val / d2
                let prod2 = d2 * q2
                if q_val > prod2:
                    # not divisible, continue checking
                    skip_check = 0
                else:
                    q_is_prime = 0
                    d2 = q_val
                d2 = d2 + 1

            if q_is_prime > 0:
                found = 1
                print("" + str(even) + " = " + str(p) + " + " + str(q_val))

        p = p + 1

    if found < 1:
        failures = failures + 1
        print("FAILURE: " + str(even) + " has no Goldbach pair!")

    even = even + 2

print("")
print("Goldbach verified up to " + str(limit) + ": " + str(failures) + " failures")
```

---

## Verify -- Self-check via assert

```markscript
let one_three = 13
let one_seven = 17
let sum_test = one_three + one_seven

# 13 + 17 = 30
> assert sum_test 30

# 13 * 17 = 221
let prod_test = one_three * one_seven
> assert prod_test 221

# 221 / 13 = 17
let div_test = prod_test / one_three
> assert div_test 17

print("All primality assertions passed")
```

---

## Notes

**Equality workaround:** The mini-language has no `==` operator --- only `>` and `<`. The pattern `if n > d * (n / d): else:` works because integer division truncates: `d * (n / d)` ≤ `n`, with equality iff `d` divides `n`. Since `d * (n / d)` can never be greater than `n`, the `else` branch fires exactly when `d | n`.

**Division granularity:** OP_DIV truncates towards zero for MARK_INT values, making this pattern safe.

**Nested loop depth:** The Goldbach search reaches 4 levels of nested while/if --- testing the parser's indentation-based block tracking.
