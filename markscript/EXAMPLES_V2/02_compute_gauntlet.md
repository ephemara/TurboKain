# Compute Gauntlet

> Raw mini-language execution: loops, recursion-by-iteration, integer edges,
> string building. Every block self-verifies with assert. If any assert
> fails, the VM's arithmetic is lying.

## fibonacci_iterative

```markscript
let fa = 0
let fb = 1
let fi = 0
while fi < 30:
    let ft = fa + fb
    fa = fb
    fb = ft
    fi = fi + 1
```

> assert fa 832040
> assert fb 1346269

## collatz_longest_under_1000

```markscript
let cn = 1
let cbest_n = 1
let cbest_len = 0
while cn < 1000:
    let cv = cn
    let clen = 0
    while cv != 1:
        if cv % 2 == 0:
            cv = cv / 2
        else:
            cv = cv * 3 + 1
        clen = clen + 1
    if clen > cbest_len:
        cbest_len = clen
        cbest_n = cn
    cn = cn + 1
```

> assert cbest_n 871
> assert cbest_len 178

## prime_sieve_first_100

```markscript
let pcount = 0
let psum = 0
let pn = 2
while pn < 542:
    let pd = 2
    let pis_prime = 1
    while pd * pd <= pn:
        if pn % pd == 0:
            pis_prime = 0
        pd = pd + 1
    if pis_prime == 1:
        pcount = pcount + 1
        psum = psum + pn
    pn = pn + 1
```

> assert pcount 100
> assert psum 24133

## integer_edges

```markscript
let big = 4611686018427387904
let big2 = big + big
print(big2)
let negmod = 0 - 17
let negmod_r = negmod % 5
let div_trunc = 7 / 2
let div_neg = 0 - 7
let div_neg_r = div_neg / 2
let zero_add = 0 + 0
let mul_zero = 123456789 * 0
```

> print "int edges done (big2 printed above: wrap vs bignum vs error)"
> assert div_trunc 3
> assert zero_add 0
> assert mul_zero 0
> print "int edges done"

## string_forge

```markscript
let sacc = ""
let si = 0
while si < 100:
    sacc = sacc + "x"
    si = si + 1
```

> print "string forge done"

## nested_loop_triangle

```markscript
let ttotal = 0
let ti = 1
while ti <= 50:
    let tj = 1
    while tj <= ti:
        ttotal = ttotal + tj
        tj = tj + 1
    ti = ti + 1
```

> assert ttotal 22100

## deep_while_100k

```markscript
let dw = 0
while dw < 100000:
    dw = dw + 1
```

> assert dw 100000
> print "COMPUTE GAUNTLET DONE"
