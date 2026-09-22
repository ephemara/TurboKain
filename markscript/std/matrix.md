# Matrix

MarkScript linear algebra --- matrix operations, decompositions, and solvers.
Dispatches to Python's `numpy.linalg` for computation.

---

## multiply

Multiply two matrices (dot product).

> run "python -c \"import numpy as np; a=np.array([[1,2],[3,4]]); b=np.array([[5,6],[7,8]]); print(a @ b)\""

```markscript
let a = [[1 2] [3 4]]
let b = [[5 6] [7 8]]
# [[19 22]
#  [43 50]]
```

---

## transpose

Transpose a matrix (swap rows and columns).

> run "python -c \"import numpy as np; a=np.array([[1,2,3],[4,5,6]]); print(a.T)\""

```markscript
let a = [[1 2 3] [4 5 6]]
# [[1 4]
#  [2 5]
#  [3 6]]
```

---

## inverse

Compute the multiplicative inverse of a square matrix.

> run "python -c \"import numpy as np; a=np.array([[1,2],[3,4]]); print(np.linalg.inv(a))\""

```markscript
let a = [[1 2] [3 4]]
# [[-2.   1. ]
#  [ 1.5 -0.5]]
# A * A^{-1} = I
```

---

## determinant

Compute the determinant of a square matrix.

> run "python -c \"import numpy as np; a=np.array([[1,2],[3,4]]); print(np.linalg.det(a))\""

```markscript
let a = [[1 2] [3 4]]
let det = -2.0
# (1*4) - (2*3) = 4 - 6 = -2
```

---

## eigenvalues

Compute eigenvalues and eigenvectors of a square matrix.

> run "python -c \"import numpy as np; a=np.array([[1,2],[2,1]]); eig=np.linalg.eig(a); print(f'eigenvalues={eig[0]} eigenvectors={eig[1]}')\""

```markscript
let a = [[1 2] [2 1]]
# eigenvalues = [ 3. -1.]
# eigenvectors = [[ 0.707 -0.707]
#                 [ 0.707  0.707]]
```

---

## solve

Solve a linear system Ax = b.

> run "python -c \"import numpy as np; a=np.array([[3,1],[1,2]]); b=np.array([9,8]); x=np.linalg.solve(a,b); print(x)\""

```markscript
let a = [[3 1] [1 2]]
let b = [9 8]
# x = [2. 3.]
# 3*2 + 1*3 = 9 ✓
# 1*2 + 2*3 = 8 ✓
```

---

## svd

Compute the singular value decomposition (SVD) of a matrix.

> run "python -c \"import numpy as np; a=np.array([[1,2],[3,4],[5,6]]); u,s,vt=np.linalg.svd(a); print(f'U={u} s={s} Vt={vt}')\""

```markscript
let a = [[1 2] [3 4] [5 6]]
# U = 3x3, S = [9.525 0.514], Vt = 2x2
# A = U * diag(S) * Vt
```

---

## norm

Compute the matrix or vector norm.

> run "python -c \"import numpy as np; a=np.array([3,4]); print(np.linalg.norm(a))\""

```markscript
let a = [3 4]
let norm = 5.0
# sqrt(3^2 + 4^2) = 5.0 (L2 norm)
```

---

## cholesky

Compute the Cholesky decomposition of a positive-definite matrix.

> run "python -c \"import numpy as np; a=np.array([[4,2],[2,3]]); L=np.linalg.cholesky(a); print(L)\""

```markscript
let a = [[4 2] [2 3]]
# L = [[2.  0. ]
#      [1.  1.414]]
# A = L * L^T
```

---

## qr

Compute the QR decomposition of a matrix.

> run "python -c \"import numpy as np; a=np.array([[1,2],[3,4],[5,6]]); q,r=np.linalg.qr(a); print(f'Q={q} R={r}')\""

```markscript
let a = [[1 2] [3 4] [5 6]]
# Q = 3x3 orthogonal, R = 3x2 upper triangular
# A = Q * R
```

---

## rank

Compute the matrix rank.

> run "python -c \"import numpy as np; a=np.array([[1,2,3],[2,4,6],[3,6,9]]); print(np.linalg.matrix_rank(a))\""

```markscript
let a = [[1 2 3] [2 4 6] [3 6 9]]
let rank = 1
# rows 2 and 3 are multiples of row 1 → rank 1
```

---

## trace

Compute the trace of a square matrix (sum of diagonal elements).

> run "python -c \"import numpy as np; a=np.array([[1,2,3],[4,5,6],[7,8,9]]); print(np.trace(a))\""

```markscript
let a = [[1 2 3] [4 5 6] [7 8 9]]
let trace = 15
# 1 + 5 + 9 = 15
```
