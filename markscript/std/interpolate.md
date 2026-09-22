# Interpolate

MarkScript interpolation -- construct functions that fit known data points
for estimating intermediate values. Dispatches to Python's `scipy.interpolate`.

---

## linear

Perform linear interpolation between data points.

> run "python -c \"from scipy import interpolate; import numpy as np; x=[0,1,2,3,4]; y=[0,2,4,6,8]; f=interpolate.interp1d(x,y,kind='linear'); print(f(2.5))\""

```markscript
let x = [0 1 2 3 4]
let y = [0 2 4 6 8]
let query = 2.5
# linear interpolation → 5.0
# (2.5 is halfway between 2→4 and 3→6)
```

---

## cubic

Perform cubic spline interpolation between data points.

> run "python -c \"from scipy import interpolate; import numpy as np; x=[0,1,2,3,4,5]; y=[0,1,4,9,16,25]; f=interpolate.interp1d(x,y,kind='cubic'); print(f(2.5))\""

```markscript
let x = [0 1 2 3 4 5]
let y = [0 1 4 9 16 25]
let query = 2.5
# cubic interpolation → ~6.25
# smoother than linear, uses neighboring points
```

---

## nearest

Perform nearest-neighbor interpolation (step function).

> run "python -c \"from scipy import interpolate; import numpy as np; x=[0,1,2,3]; y=[10,20,30,40]; f=interpolate.interp1d(x,y,kind='nearest'); print(f(1.7))\""

```markscript
let x = [0 1 2 3]
let y = [10 20 30 40]
let query = 1.7
# nearest neighbor → 20 (closest to x=2? no, x=1.7 → nearest is x=2 → 30)
# nearest to 1.7 is x=2 → y=30... wait x=1 and x=2, distance 0.7 and 0.3
# so y=30
let result = 30
```

---

## extrapolate

Interpolate beyond the original data range (extrapolation).

> run "python -c \"from scipy import interpolate; import numpy as np; x=[0,1,2,3,4]; y=[0,2,4,6,8]; f=interpolate.interp1d(x,y,kind='linear',fill_value='extrapolate'); print(f(5))\""

```markscript
let x = [0 1 2 3 4]
let y = [0 2 4 6 8]
let query = 5.0
# extrapolate → 10.0
# linear extrapolation beyond x=4 continues the line
```

---

## spline

Fit a smoothing spline to noisy data.

> run "python -c \"from scipy import interpolate; import numpy as np; x=np.linspace(0,10,20); y=np.sin(x)+np.random.normal(0,0.1,20); spl=interpolate.UnivariateSpline(x,y,s=0.5); xs=np.linspace(0,10,100); ys=spl(xs); print(f'smooth_spline_fit shape={ys.shape}')\""

```markscript
let n_points = 20
let s = 0.5
# smoothing spline fitted to 20 noisy points
# s=0.5 controls smoothing factor
# evaluates to 100 points
```

---

## pchip

Perform monotonic cubic Hermite interpolation (preserves shape).

> run "python -c \"from scipy import interpolate; import numpy as np; x=[0,1,2,3,4,5]; y=[0,0,1,1,2,2]; f=interpolate.PchipInterpolator(x,y); print(f(2.5))\""

```markscript
let x = [0 1 2 3 4 5]
let y = [0 0 1 1 2 2]
let query = 2.5
# PCHIP preserves monotonicity → ~1.0
# no overshoot between flat and rising regions
```

---

## interp2d

Perform 2D interpolation on a grid.

> run "python -c \"from scipy import interpolate; import numpy as np; x=np.array([0,1,2]); y=np.array([0,1,2]); z=np.array([[0,1,2],[1,2,3],[2,3,4]]); f=interpolate.interp2d(x,y,z,kind='linear'); print(f(0.5,0.5))\""

```markscript
let x = [0 1 2]
let y = [0 1 2]
# z = f(x,y)
let z = [[0 1 2] [1 2 3] [2 3 4]]
let query_x = 0.5
let query_y = 0.5
# 2D linear interpolation → 1.0
```

---

## lagrange

Construct the Lagrange polynomial through data points.

> run "python -c \"from scipy import interpolate; import numpy as np; x=[0,1,2]; y=[1,3,2]; poly=interpolate.lagrange(x,y); print(poly(1.5))\""

```markscript
let x = [0 1 2]
let y = [1 3 2]
let query = 1.5
# Lagrange polynomial → 2.75
# polynomial passes exactly through all points
```

---

## barycentric

Perform barycentric interpolation (numerically stable polynomial interpolation).

> run "python -c \"from scipy import interpolate; import numpy as np; x=[0,1,2,3,4]; y=[0,1,4,9,16]; f=interpolate.BarycentricInterpolator(x,y); print(f(2.5))\""

```markscript
let x = [0 1 2 3 4]
let y = [0 1 4 9 16]
let query = 2.5
# barycentric → 6.25
# stable polynomial interpolation
```
