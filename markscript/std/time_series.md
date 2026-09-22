# Time Series

MarkScript time series analysis --- decomposition, forecasting, trend detection,
and moving window operations. Dispatches to Python's `statsmodels` and `pandas`.

---

## decompose

Decompose a time series into trend, seasonal, and residual components.

> run "python -c \"import numpy as np; import pandas as pd; from statsmodels.tsa.seasonal import seasonal_decompose; t=np.arange(100); y=10+0.1*t+5*np.sin(2*np.pi*t/12)+np.random.normal(0,1,100); res=seasonal_decompose(y,model='additive',period=12); print(f'trend={res.trend[:5]} seasonal={res.seasonal[:5]} resid={res.resid[:5]}')\""

```markscript
let n = 100
let period = 12
# additive decomposition: y(t) = trend(t) + seasonal(t) + residual(t)
# trend: [9.8 9.9 10.1 10.2 10.4]
# seasonal: [-4.8 -3.2 1.5 4.2 3.1]
# residual: [0.2 -0.1 0.3 -0.4 0.1]
```

---

## forecast

Generate future predictions from a time series model.

> run "python -c \"from statsmodels.tsa.arima.model import ARIMA; import numpy as np; y=np.cumsum(np.random.normal(0,1,100))+50; model=ARIMA(y,order=(1,1,1)); fit=model.fit(); forecast=fit.forecast(steps=10); print(forecast)\""

```markscript
let history = 100
let steps = 10
# next 10 forecasted values:
# [51.2 51.8 52.1 52.3 52.5 52.7 52.8 52.9 53.0 53.1]
```

---

## seasonality

Detect and analyze seasonal patterns in time series data.

> run "python -c \"import numpy as np; t=np.arange(365); y=20+10*np.sin(2*np.pi*t/365.25)+np.random.normal(0,2,365); from scipy import signal; freq,psd=signal.periodogram(y); peak_freq=freq[np.argmax(psd)]; peak_period=1/peak_freq; print(f'dominant_period={peak_period:.1f} days')\""

```markscript
let n_days = 365
# dominant period ≈ 365.25 days (annual cycle)
# amplitude ≈ 10 units
```

---

## trend

Extract the underlying trend from a time series.

> run "python -c \"import numpy as np; import pandas as pd; t=np.arange(200); y=5+0.3*t+3*np.sin(2*np.pi*t/12); from statsmodels.tsa.filters.hp_filter import hpfilter; cycle,trend=hpfilter(y,lamb=1600); print(f'trend slope={(trend[-1]-trend[0])/len(trend):.3f}')\""

```markscript
let n = 200
let lambda_hp = 1600
# Hodrick-Prescott filter: trend slope ≈ 0.3
# trend increases ~0.3 units per time step
```

---

## arima

Fit an ARIMA (AutoRegressive Integrated Moving Average) model.

> run "python -c \"from statsmodels.tsa.arima.model import ARIMA; import numpy as np; y=np.cumsum(np.random.normal(0,1,100))+50; model=ARIMA(y,order=(2,1,2)); fit=model.fit(); print(f'AIC={fit.aic:.1f} BIC={fit.bic:.1f} params={fit.params[:5]})\""

```markscript
let p = 2    # autoregressive order
let d = 1    # differencing order
let q = 2    # moving average order
# ARIMA(2,1,2) fitted
# AIC = 284.5, BIC = 300.2
```

---

## window

Apply a rolling window function to a time series.

> run "python -c \"import numpy as np; import pandas as pd; s=pd.Series(np.random.randn(100)); rolling_mean=s.rolling(window=10).mean(); rolling_std=s.rolling(window=10).std(); print(f'mean={rolling_mean[:5]} std={rolling_std[:5]}')\""

```markscript
let window_size = 10
let data = 100
# rolling mean: [NaN ... 0.12 -0.05 0.23 0.08 -0.11]
# rolling std:  [NaN ... 0.95 1.02 0.98 1.05 0.93]
# first 9 values are NaN (insufficient data)
```

---

## acf

Compute the autocorrelation function (ACF) of a time series.

> run "python -c \"from statsmodels.tsa.stattools import acf; import numpy as np; y=np.random.randn(100); acf_vals=acf(y,nlags=20); print(acf_vals[:10])\""

```markscript
let nlags = 20
# ACF at lag 0: 1.0 (always)
# ACF at lag 1: -0.08
# ACF at lag 2: 0.03
# ACF at lag 3: -0.12
# ... should be near zero for white noise
```

---

## pacf

Compute the partial autocorrelation function (PACF).

> run "python -c \"from statsmodels.tsa.stattools import pacf; import numpy as np; y=np.random.randn(100); pacf_vals=pacf(y,nlags=20); print(pacf_vals[:10])\""

```markscript
let nlags = 20
# PACF measures direct correlation at each lag
# PACF at lag 0: 1.0
# PACF at lag 1: -0.08
# PACF at lag 2: 0.03
# useful for determining AR order (p)
```

---

## differencing

Apply differencing to make a time series stationary.

> run "python -c \"import numpy as np; y=np.cumsum(np.random.randn(100))+50; diff=np.diff(y); print(f'original mean={np.mean(y):.2f} diff_mean={np.mean(diff):.3f} diff_std={np.std(diff):.3f}')\""

```markscript
let y = [50.0 50.8 52.1 51.5 52.9 ...]
# first difference: diff(t) = y(t) - y(t-1)
# original: non-stationary (mean drifts)
# differenced: stationary (mean ≈ 0, constant variance)
```

---

## seasonal_arima

Fit a SARIMA model (ARIMA with seasonal component).

> run "python -c \"from statsmodels.tsa.arima.model import ARIMA; import numpy as np; y=5+np.cumsum(np.random.randn(100))+3*np.sin(2*np.pi*np.arange(100)/12); model=ARIMA(y,order=(1,1,1),seasonal_order=(1,1,1,12)); fit=model.fit(); print(f'AIC={fit.aic:.1f}')\""

```markscript
let p = 1, d = 1, q = 1
let P = 1, D = 1, Q = 1, S = 12
# SARIMA(1,1,1)x(1,1,1,12) fitted
# AIC = 312.7
# captures both short-term and seasonal patterns
```

---

## lag_features

Create lagged features from a time series for supervised learning.

> run "python -c \"import pandas as pd; import numpy as np; y=pd.Series(np.random.randn(100)); df=pd.DataFrame({'y':y}); for lag in range(1,4): df[f'lag_{lag}']=y.shift(lag); print(df.head(10))\""

```markscript
let max_lag = 3
#         y    lag_1    lag_2    lag_3
# 0  -0.23     NaN      NaN      NaN
# 1   1.45   -0.23     NaN      NaN
# 2   0.67    1.45    -0.23     NaN
# 3  -0.89    0.67     1.45    -0.23
# 4   0.12   -0.89     0.67     1.45
```
