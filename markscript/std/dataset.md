# Dataset

MarkScript dataset utilities --- loading, inspecting, splitting, and caching
datasets for machine learning. Dispatches to Python's `sklearn.datasets`
and `pandas`.

---

## load

Load a built-in dataset (e.g., iris, diabetes, digits).

> run "python -c \"from sklearn.datasets import load_iris; data=load_iris(); print(f'keys={data.keys()} features={data.data.shape} target={data.target.shape} classes={data.target_names}')\""

```markscript
let name = "iris"
# keys: ['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names']
# features: (150, 4), target: (150,)
# classes: ['setosa' 'versicolor' 'virginica']
```

---

## fetch

Fetch a dataset from an online repository.

> run "python -c \"from sklearn.datasets import fetch_california_housing; data=fetch_california_housing(); print(f'features={data.data.shape} target={data.target.shape} descr={data.DESCR[:100]}')\""

```markscript
let name = "california_housing"
# features: (20640, 8), target: (20640,)
# California housing prices with 8 features
```

---

## describe

Generate a detailed statistical description of a dataset.

> run "python -c \"import pandas as pd; from sklearn.datasets import load_diabetes; data=load_diabetes(); df=pd.DataFrame(data.data,columns=data.feature_names); df['target']=data.target; print(df.describe())\""

```markscript
let dataset = "diabetes"
# |       | age    | sex    | bmi    | bp     | target  |
# |-------|--------|--------|--------|--------|---------|
# | count | 442.0  | 442.0  | 442.0  | 442.0  | 442.0   |
# | mean  | -0.0   | -0.0   | -0.0   | -0.0   | 152.1   |
# | std   | 0.048  | 0.048  | 0.048  | 0.048  | 77.0    |
# | min   | -0.11  | -0.04  | -0.09  | -0.11  | 25.0    |
# | max   | 0.11   | 0.05   | 0.17   | 0.13   | 346.0   |
```

---

## sample

Draw random samples from a dataset.

> run "python -c \"import pandas as pd; from sklearn.datasets import load_wine; data=load_wine(); df=pd.DataFrame(data.data,columns=data.feature_names); df['target']=data.target; sample=df.sample(n=5,random_state=42); print(sample)\""

```markscript
let n = 5
let random_state = 42
# 5 random rows from the wine dataset
# preserves all columns including target
```

---

## split

Split a dataset into training, validation, and test sets.

> run "python -c \"from sklearn.datasets import load_iris; from sklearn.model_selection import train_test_split; X,y=load_iris(return_X_y=True); X_tr,X_te,y_tr,y_te=train_test_split(X,y,test_size=0.2,random_state=42); X_tr,X_val,y_tr,y_val=train_test_split(X_tr,y_tr,test_size=0.2,random_state=42); print(f'train={X_tr.shape} val={X_val.shape} test={X_te.shape}')\""

```markscript
let test_size = 0.2
let val_size = 0.16
# train: (96, 4), val: (24, 4), test: (30, 4)
# 64% train, 16% val, 20% test
```

---

## cache

Cache a dataset to disk for faster subsequent loads.

> run "python -c \"import pickle; from sklearn.datasets import load_diabetes; import os; cache_path='cache_diabetes.pkl'; if os.path.exists(cache_path): data=pickle.load(open(cache_path,'rb')); print('loaded from cache'); else: data=load_diabetes(); pickle.dump(data,open(cache_path,'wb')); print('cached to disk')\""

```markscript
let cache_path = "cache_diabetes.pkl"
# first call: downloads and caches
# subsequent calls: loads from cache
```

---

## list_datasets

List all available built-in datasets.

> run "python -c \"from sklearn.datasets import load_iris,load_diabetes,load_digits,load_wine,load_breast_cancer,load_linnerud; datasets=['iris','diabetes','digits','wine','breast_cancer','linnerud']; print(datasets)\""

```markscript
# Available datasets:
# iris         → 150 samples, 4 features, 3 classes (classification)
# diabetes     → 442 samples, 10 features (regression)
# digits       → 1797 samples, 64 features, 10 classes (classification)
# wine         → 178 samples, 13 features, 3 classes (classification)
# breast_cancer → 569 samples, 30 features, 2 classes (classification)
# california_housing → 20640 samples, 8 features (regression)
# linnerud     → 20 samples, 3 features (regression)
```

---

## make_classification

Generate a synthetic classification dataset.

> run "python -c \"from sklearn.datasets import make_classification; X,y=make_classification(n_samples=1000,n_features=10,n_classes=2,random_state=42); print(f'X={X.shape} y={y.shape} classes={set(y)}')\""

```markscript
let n_samples = 1000
let n_features = 10
let n_classes = 2
# X: (1000, 10), y: (1000,)
# 2-class classification dataset
# 10 features, some informative, some redundant
```

---

## make_regression

Generate a synthetic regression dataset.

> run "python -c \"from sklearn.datasets import make_regression; X,y=make_regression(n_samples=500,n_features=5,noise=0.1,random_state=42); print(f'X={X.shape} y={y.shape} y_range=[{y.min():.2f},{y.max():.2f}]')\""

```markscript
let n_samples = 500
let n_features = 5
let noise = 0.1
# X: (500, 5), y: (500,)
# linear regression ground truth with Gaussian noise
# y range: [-173.5, 167.8]
```
