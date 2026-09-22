# Optimize

MarkScript optimization -- finding minima and maxima of functions, gradient-based
methods, and constrained optimization. Dispatches to Python's `scipy.optimize`.

---

## minimize

Find the minimum of a scalar function.

> run "python -c \"from scipy import optimize; import numpy as np; f=lambda x: x**2 + 2*x + 1; res=optimize.minimize(f,0); print(f'x={res.x[0]:.6f} f={res.fun:.6f}')\""

```markscript
let f = "x^2 + 2x + 1"
let initial = 0.0
# minimum at x = -1.0, f(x) = 0.0
let x_min = -1.0
let f_min = 0.0
```

---

## maximize

Find the maximum of a scalar function (minimize the negative).

> run "python -c \"from scipy import optimize; import numpy as np; f=lambda x: -(x-3)**2 + 5; res=optimize.minimize(lambda x: -f(x),0); print(f'x={res.x[0]:.6f} f={f(res.x[0]):.6f}')\""

```markscript
let f = "-(x-3)^2 + 5"
let initial = 0.0
# maximum at x = 3.0, f(x) = 5.0
let x_max = 3.0
let f_max = 5.0
```

---

## gradient_descent

Perform gradient descent optimization on a function.

> run "python -c \"import numpy as np; f=lambda x: x**2+2*x+1; df=lambda x: 2*x+2; x=5.0; lr=0.1; for i in range(50): x=x-lr*df(x); print(f'x={x:.6f} f={f(x):.6f}')\""

```markscript
let f = "x^2 + 2x + 1"
let grad = "2x + 2"
let x = 5.0
let lr = 0.1
let steps = 50
# after 50 steps: x ≈ -1.0, f(x) ≈ 0.0
# converges to the global minimum
```

---

## newton

Use Newton's method for root finding.

> run "python -c \"from scipy import optimize; f=lambda x: x**2 - 4; df=lambda x: 2*x; root=optimize.newton(f,1,fprime=df); print(f'root={root:.6f}')\""

```markscript
let f = "x^2 - 4"
let initial = 1.0
# finds root at x = 2.0 (since 2^2 - 4 = 0)
let root = 2.0
```

---

## constraints

Minimize a function subject to equality and inequality constraints.

> run "python -c \"from scipy import optimize; f=lambda x: x[0]**2+x[1]**2; cons=({'type':'eq','fun':lambda x:x[0]+x[1]-1},); res=optimize.minimize(f,[0,0],constraints=cons); print(f'x={res.x} f={res.fun:.6f}')\""

```markscript
let f = "x^2 + y^2"
let constraint = "x + y = 1"
# minimum at x=0.5, y=0.5, f=0.5
# satisfies x + y = 1
```

---

## basin_hopping

Global optimization using basin-hopping algorithm.

> run "python -c \"from scipy import optimize; import numpy as np; f=lambda x: x**2 + 10*np.sin(x); res=optimize.basinhopping(f,0); print(f'x={res.x[0]:.6f} f={res.fun:.6f}')\""

```markscript
let f = "x^2 + 10*sin(x)"
let initial = 0.0
# global minimum found (not just local)
# x ≈ -1.306, f ≈ -7.946
```

---

## curve_fit

Fit a curve (non-linear least squares) to data.

> run "python -c \"from scipy import optimize; import numpy as np; f=lambda x,a,b: a*np.exp(-b*x); x=np.array([0,1,2,3]); y=f(x,2.5,1.3)+np.random.normal(0,0.05,4); popt,pcov=optimize.curve_fit(f,x,y); print(f'a={popt[0]:.3f} b={popt[1]:.3f}')\""

```markscript
let model = "a * exp(-b*x)"
let x = [0 1 2 3]
let y = [2.5 0.65 0.17 0.045]
# fitted: a ≈ 2.5, b ≈ 1.3
# y = 2.5 * exp(-1.3 * x)
```

---

## least_squares

Solve a non-linear least-squares problem.

> run "python -c \"from scipy import optimize; import numpy as np; f=lambda x: [x[0]+0.5*x[1]-1, x[0]-x[1]-2]; res=optimize.least_squares(f,[0,0]); print(f'x={res.x}')"

```markscript
let eq1 = "x + 0.5y = 1"
let eq2 = "x - y = 2"
# solution: x = 1.333, y = -0.667
```

---

## linear_programming

Solve a linear programming problem.

> run "python -c \"from scipy import optimize; c=[-3,-2]; A=[[2,1],[1,2]]; b=[20,20]; bounds=[(0,None),(0,None)]; res=optimize.linprog(c,A_ub=A,b_ub=b,bounds=bounds); print(f'x={res.x} f={-res.fun:.3f}')\""

```markscript
let c = [-3 -2]    # maximize 3x + 2y
let A = [[2 1] [1 2]]
let b = [20 20]     # 2x+y ≤ 20, x+2y ≤ 20
let bounds = [0 None 0 None]
# optimal: x=6.667, y=6.667, f=40.0
```

---

## differential_evolution

Global optimization using differential evolution.

> run "python -c \"from scipy import optimize; f=lambda x: x[0]**2+x[1]**2+10*np.sin(x[0])+10*np.sin(x[1]); bounds=[(-5,5),(-5,5)]; res=optimize.differential_evolution(f,bounds); print(f'x={res.x} f={res.fun:.6f}')\""

```markscript
let f = "x^2 + y^2 + 10*sin(x) + 10*sin(y)"
let bounds = [[-5 5] [-5 5]]
# global minimum found without gradient
# x ≈ -1.306, y ≈ -1.306, f ≈ -15.892
```
