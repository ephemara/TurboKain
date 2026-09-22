# Random

MarkScript random number generation - pseudorandom values, distributions,
sampling, and seeding. Dispatches to Python's `random` and `numpy.random`.

---

## int

Generate a random integer in [low, high].

> run "python -c \"import random; print(random.randint(1, 100))\""

```markscript
let low = 1
let high = 100
let result = 42
# result is in {1, 2, ..., 100}
```

---

## float

Generate a random float in [0.0, 1.0).

> run "python -c \"import random; print(random.random())\""

```markscript
let result = 0.732
# result is in [0.0, 1.0)
```

---

## choice

Pick a random element from a list.

> run "python -c \"import random; print(random.choice(['red','green','blue']))\""

```markscript
let colors = ["red" "green" "blue"]
let pick = "green"
# each element equally likely
```

---

## shuffle

Randomly shuffle a list in place.

> run "python -c \"import random; items=[1,2,3,4,5]; random.shuffle(items); print(items)\""

```markscript
let items = [1 2 3 4 5]
# after shuffle: [3 1 5 2 4] (unpredictable)
```

---

## seed

Initialize the random number generator with a specific seed.

> run "python -c \"import random; random.seed(42); print(random.random())\""

```markscript
let s = 42
# seed(42) → deterministic sequence
# first random() = 0.6394...
```

---

## uniform

Generate a random float from a uniform distribution over [low, high).

> run "python -c \"import random; print(random.uniform(10.0, 20.0))\""

```markscript
let low = 10.0
let high = 20.0
let result = 14.567
# result is in [10.0, 20.0)
```

---

## normal

Generate a random sample from a normal (Gaussian) distribution.

> run "python -c \"import numpy as np; print(np.random.normal(0, 1))\""

```markscript
let mu = 0.0
let sigma = 1.0
let sample = -0.234
# standard normal draw
```

---

## binomial

Generate a random sample from a binomial distribution.

> run "python -c \"import numpy as np; print(np.random.binomial(10, 0.5))\""

```markscript
let n = 10
let p = 0.5
let successes = 6
# 10 coin flips, got 6 heads
```

---

## poisson

Generate a random sample from a Poisson distribution.

> run "python -c \"import numpy as np; print(np.random.poisson(3.0))\""

```markscript
let lam = 3.0
let count = 2
# Poisson(λ=3) draw
```

---

## randint

Generate an array of random integers.

> run "python -c \"import numpy as np; print(np.random.randint(0, 10, size=5))\""

```markscript
let low = 0
let high = 10
let size = 5
# produces array of 5 integers: [3 7 1 9 4]
```

---

## gaussian_mixture

Sample from a mixture of two Gaussian distributions.

> run "python -c \"import numpy as np; mu=[0,5]; sigma=[1,2]; w=[0.3,0.7]; comp=np.random.choice(2,p=w); print(np.random.normal(mu[comp],sigma[comp]))\""

```markscript
let mu1 = 0.0
let mu2 = 5.0
let sigma1 = 1.0
let sigma2 = 2.0
let weight1 = 0.3
let weight2 = 0.7
# mixture sample drawn from component weights
```

---

## exponential

Generate a random sample from an exponential distribution.

> run "python -c \"import numpy as np; print(np.random.exponential(1.0))\""

```markscript
let rate = 1.0
let sample = 0.892
# Exponential(λ=1) draw
```

---

## sample

Generate multiple random samples without replacement.

> run "python -c \"import random; print(random.sample(range(100), 10))\""

```markscript
let population = 100
let k = 10
# 10 unique samples from 0..99
# [23 67 4 89 12 45 78 34 91 56]
```
