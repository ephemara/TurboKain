# JIT Brutal

> The JIT lane (`jit-run`: compile and execute via JIT, no VM) under the
> same load as the VM gauntlet. Same asserts, different engine — outputs
> must AGREE. Any divergence between `run` and `jit-run` is a bug with
> a receipt.

## fib_25

```markscript
let ja = 0
let jb = 1
let ji = 0
while ji < 25:
    let jt = ja + jb
    ja = jb
    jb = jt
    ji = ji + 1
```

> assert ja 75025
> assert jb 121393

## prime_sum_50

```markscript
let jc = 0
let js = 0
let jn = 2
while jn < 230:
    let jd = 2
    let jp = 1
    while jd * jd <= jn:
        if jn % jd == 0:
            jp = 0
        jd = jd + 1
    if jp == 1:
        jc = jc + 1
        js = js + jn
    jn = jn + 1
```

> assert jc 50
> assert js 5117

## collatz_27

```markscript
let jv = 27
let jl = 0
while jv != 1:
    if jv % 2 == 0:
        jv = jv / 2
    else:
        jv = jv * 3 + 1
    jl = jl + 1
```

> assert jl 111

## string_intent_mix

> upper "jit brutal"
> concat "jit" "brutal"
> sqrt 169
> min 9 4

> print "JIT BRUTAL DONE"
