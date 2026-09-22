# NumPy

MarkScript array computing - NumPy-powered ndarray creation, manipulation,
and linear algebra. All routines dispatch through `> run "python ..."`.

---

## array

Create an ndarray from a list of values.

> run "python -c \"import numpy as np; a=np.array([1,2,3,4,5]); print(a)\""

```markscript
let data = [1 2 3 4 5]
let a = [1 2 3 4 5]
# array([1, 2, 3, 4, 5])
```

---

## zeros

Create an array filled with zeros.

> run "python -c \"import numpy as np; print(np.zeros((3,4)))\""

```markscript
let rows = 3
let cols = 4
# [[0. 0. 0. 0.]
#  [0. 0. 0. 0.]
#  [0. 0. 0. 0.]]
```

---

## ones

Create an array filled with ones.

> run "python -c \"import numpy as np; print(np.ones((2,3)))\""

```markscript
let rows = 2
let cols = 3
# [[1. 1. 1.]
#  [1. 1. 1.]]
```

---

## arange

Create an array with evenly spaced values within a range.

> run "python -c \"import numpy as np; print(np.arange(0, 10, 2))\""

```markscript
let start = 0
let stop = 10
let step = 2
# [0 2 4 6 8]
```

---

## linspace

Create an array with evenly spaced values over a specified interval.

> run "python -c \"import numpy as np; print(np.linspace(0, 1, 5))\""

```markscript
let start = 0.0
let stop = 1.0
let num = 5
# [0.   0.25 0.5  0.75 1. ]
```

---

## reshape

Reshape an array to a new shape without changing its data.

> run "python -c \"import numpy as np; a=np.arange(6); print(a.reshape(2,3))\""

```markscript
let a = [0 1 2 3 4 5]
let r = 2
let c = 3
# [[0 1 2]
#  [3 4 5]]
```

---

## dot

Compute the dot product of two arrays.

> run "python -c \"import numpy as np; a=np.array([1,2,3]); b=np.array([4,5,6]); print(np.dot(a,b))\""

```markscript
let a = [1 2 3]
let b = [4 5 6]
let result = 32
# 1*4 + 2*5 + 3*6 = 32
```

---

## sum

Compute the sum of array elements.

> run "python -c \"import numpy as np; a=np.array([[1,2],[3,4]]); print(np.sum(a))\""

```markscript
let a = [[1 2] [3 4]]
let total = 10
# 1 + 2 + 3 + 4 = 10
```

---

## mean

Compute the arithmetic mean of array elements.

> run "python -c \"import numpy as np; a=np.array([1,2,3,4,5]); print(np.mean(a))\""

```markscript
let a = [1 2 3 4 5]
let result = 3.0
# (1 + 2 + 3 + 4 + 5) / 5 = 3.0
```

---

## max

Return the maximum value in an array.

> run "python -c \"import numpy as np; a=np.array([3,7,1,9,4]); print(np.max(a))\""

```markscript
let a = [3 7 1 9 4]
let result = 9
# 9 is the largest element
```

---

## min

Return the minimum value in an array.

> run "python -c \"import numpy as np; a=np.array([3,7,1,9,4]); print(np.min(a))\""

```markscript
let a = [3 7 1 9 4]
let result = 1
# 1 is the smallest element
```

---

## transpose

Transpose a matrix (swap rows and columns).

> run "python -c \"import numpy as np; a=np.array([[1,2],[3,4]]); print(a.T)\""

```markscript
let a = [[1 2] [3 4]]
# [[1 3]
#  [2 4]]
```

---

## matmul

Perform matrix multiplication between two arrays.

> run "python -c \"import numpy as np; a=np.array([[1,2],[3,4]]); b=np.array([[5,6],[7,8]]); print(a @ b)\""

```markscript
let a = [[1 2] [3 4]]
let b = [[5 6] [7 8]]
# [[19 22]
#  [43 50]]
```

---

## broadcast

Demonstrate NumPy broadcasting (operations on different-shaped arrays).

> run "python -c \"import numpy as np; a=np.array([[1],[2],[3]]); b=np.array([10,20]); print(a + b)\""

```markscript
let a = [[1] [2] [3]]
let b = [10 20]
# [[11 21]
#  [12 22]
#  [13 23]]
# broadcasting expands a(3,1) + b(2) → a(3,1) + b(1,2) → result(3,2)
```
