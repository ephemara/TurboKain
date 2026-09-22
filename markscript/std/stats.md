# Stats

MarkScript statistical computations --- descriptive statistics, distributions,
and inference routines. Dispatches to Python's `scipy.stats` and `numpy`
through the IVT `run` handler.

---

## mean

Compute the arithmetic mean (average) of a numeric list.

> run "python -c \"import numpy as np; print(np.mean([1,2,3,4,5,6,7,8,9,10]))\""

```markscript
let data = [1 2 3 4 5 6 7 8 9 10]
let result = 5.5
# mean = sum(data) / len(data)
```

---

## median

Compute the middle value of a sorted numeric list.

> run "python -c \"import numpy as np; print(np.median([1,3,5,7,9,11]))\""

```markscript
let data = [1 3 5 7 9 11]
let n = 6
# n is even → median = (5 + 7) / 2 = 6
let result = 6.0
```

---

## mode

Find the most frequent value(s) in a dataset.

> run "python -c \"from scipy import stats; print(stats.mode([2,3,3,4,5,3,2,1]))\""

```markscript
let data = [2 3 3 4 5 3 2 1]
let result = 3
# 3 appears 3 times --- most frequent
```

---

## stddev

Compute the sample standard deviation.

> run "python -c \"import numpy as np; print(np.std([10,12,23,23,16,23,21,16], ddof=1))\""

```markscript
let data = [10 12 23 23 16 23 21 16]
let n = 8
# sqrt(sum((xi - mean)^2) / (n - 1))
let result = 5.237
```

---

## variance

Compute the sample variance.

> run "python -c \"import numpy as np; print(np.var([10,12,23,23,16,23,21,16], ddof=1))\""

```markscript
let data = [10 12 23 23 16 23 21 16]
let n = 8
# sum((xi - mean)^2) / (n - 1)
let result = 27.429
```

---

## percentile

Compute the k-th percentile of a dataset.

> run "python -c \"import numpy as np; print(np.percentile([1,2,3,4,5,6,7,8,9,10], 25))\""

```markscript
let data = [1 2 3 4 5 6 7 8 9 10]
let p = 25
# 25th percentile (Q1)
let result = 3.25
```

---

## correlation

Compute Pearson correlation coefficient between two datasets.

> run "python -c \"import numpy as np; a=[1,2,3,4,5]; b=[2,4,6,8,10]; print(np.corrcoef(a,b)[0,1])\""

```markscript
let x = [1 2 3 4 5]
let y = [2 4 6 8 10]
# perfect linear correlation
let r = 1.0
```

---

## regression

Fit a linear regression and return slope, intercept, r-value, and p-value.

> run "python -c \"from scipy import stats; x=[1,2,3,4,5]; y=[2,4,5,4,5]; res=stats.linregress(x,y); print(f'{res.slope},{res.intercept},{res.rvalue},{res.pvalue}')\""

```markscript
let x = [1 2 3 4 5]
let y = [2 4 5 4 5]
# slope = 0.6, intercept = 1.6, r = 0.7746, p = 0.1242
let slope = 0.6
let intercept = 1.6
```

---

## iqr

Compute the interquartile range (Q3 - Q1).

> run "python -c \"import numpy as np; d=[1,2,3,4,5,6,7,8]; q=np.percentile(d,[25,75]); print(q[1]-q[0])\""

```markscript
let data = [1 2 3 4 5 6 7 8]
let q1 = 2.5
let q3 = 6.5
let iqr = q3 - q1
# iqr = 4.0
```

---

## skewness

Compute the skewness of a dataset (measure of asymmetry).

> run "python -c \"from scipy import stats; print(stats.skew([1,2,2,3,3,3,4,5,10]))\""

```markscript
let data = [1 2 2 3 3 3 4 5 10]
# positive skew → right tail
let result = 1.566
```

---

## kurtosis

Compute the kurtosis of a dataset (measure of tailedness).

> run "python -c \"from scipy import stats; print(stats.kurtosis([1,2,3,4,5,6,7,8,9,10]))\""

```markscript
let data = [1 2 3 4 5 6 7 8 9 10]
# excess kurtosis (Fisher)
let result = -1.224
```

---

## describe

Generate a comprehensive statistical summary of a dataset.

> run "python -c \"import numpy as np; from scipy import stats; d=[1,2,3,4,5,6,7,8,9,10]; print(f'count={len(d)} mean={np.mean(d)} std={np.std(d,ddof=1)} min={min(d)} q25={np.percentile(d,25)} q50={np.median(d)} q75={np.percentile(d,75)} max={max(d)}')\""

```markscript
let data = [1 2 3 4 5 6 7 8 9 10]
# describe returns: count, mean, std, min, 25%, 50%, 75%, max
# count=10 mean=5.5 std=3.028 min=1 q25=3.25 q50=5.5 q75=7.75 max=10
```
