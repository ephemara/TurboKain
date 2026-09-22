# Preprocess

MarkScript data preprocessing -- transforming raw data into ML-ready features.
Dispatches to Python's `scikit-learn` preprocessing and `pandas`.

---

## normalize

Scale individual samples to have unit norm.

> run "python -c \"from sklearn.preprocessing import normalize; import numpy as np; X=np.array([[1,2,3],[4,5,6],[7,8,9]]); Xn=normalize(X,norm='l2'); print(Xn)\""

```markscript
let X = [[1 2 3] [4 5 6] [7 8 9]]
let norm = "l2"
# [[0.267 0.535 0.802]
#  [0.456 0.570 0.684]
#  [0.502 0.574 0.646]]
```

---

## standardize

Standardize features by removing mean and scaling to unit variance.

> run "python -c \"from sklearn.preprocessing import StandardScaler; import numpy as np; X=np.array([[1,2],[2,3],[3,4],[4,5]]); scaler=StandardScaler(); Xs=scaler.fit_transform(X); print(f'mean={scaler.mean_} std={np.sqrt(scaler.var_)}')\""

```markscript
let X = [[1 2] [2 3] [3 4] [4 5]]
# scaled X has mean=0, std=1 for each feature
# mean = [2.5 3.5], std = [1.118 1.118]
```

---

## minmax_scale

Scale features to a given range (default 0 to 1).

> run "python -c \"from sklearn.preprocessing import MinMaxScaler; import numpy as np; X=np.array([[1,100],[2,200],[3,300],[4,400]]); scaler=MinMaxScaler(); Xs=scaler.fit_transform(X); print(Xs)\""

```markscript
let X = [[1 100] [2 200] [3 300] [4 400]]
# [[0.    0.   ]
#  [0.333 0.333]
#  [0.667 0.667]
#  [1.    1.   ]]
```

---

## encode_categorical

Convert categorical variables to one-hot encoded vectors.

> run "python -c \"from sklearn.preprocessing import OneHotEncoder; import numpy as np; X=np.array([['red'],['green'],['blue'],['red']]); enc=OneHotEncoder(sparse_output=False); Xe=enc.fit_transform(X); print(f'categories={enc.categories_}'); print(Xe)\""

```markscript
let data = ["red" "green" "blue" "red"]
# categories = [['blue' 'green' 'red']]
# [[0 0 1]   # red
#  [0 1 0]   # green
#  [1 0 0]   # blue
#  [0 0 1]]  # red
```

---

## label_encode

Convert categorical labels to integer indices.

> run "python -c \"from sklearn.preprocessing import LabelEncoder; labels=['cat','dog','bird','dog','cat']; le=LabelEncoder(); encoded=le.fit_transform(labels); print(f'classes={le.classes_} encoded={encoded}')\""

```markscript
let labels = ["cat" "dog" "bird" "dog" "cat"]
# classes = ['bird' 'cat' 'dog']
# encoded = [1 2 0 2 1]
```

---

## impute

Fill missing values in a dataset.

> run "python -c \"from sklearn.impute import SimpleImputer; import numpy as np; X=np.array([[1,2],[np.nan,3],[4,np.nan],[5,6]]); imp=SimpleImputer(strategy='mean'); Xi=imp.fit_transform(X); print(f'statistics={imp.statistics_}'); print(Xi)\""

```markscript
let X = [[1 2] [None 3] [4 None] [5 6]]
let strategy = "mean"
# statistics = [3.333 3.667]
# [[1.    2.   ]
#  [3.333 3.   ]
#  [4.    3.667]
#  [5.    6.   ]]
```

---

## scale

Standardize data using a specific scaler (robust or quantile).

> run "python -c \"from sklearn.preprocessing import RobustScaler; import numpy as np; X=np.array([[1,100],[2,200],[3,300],[1000,400]]); scaler=RobustScaler(); Xr=scaler.fit_transform(X); print(Xr)\""

```markscript
let X = [[1 100] [2 200] [3 300] [1000 400]]
# RobustScaler uses median & IQR (robust to outliers)
# [[ 0.    -1.   ]
#  [ 0.     0.   ]
#  [ 0.     1.   ]
#  [ 99.75  1.5  ]]
```

---

## split

Split data into training, validation, and test sets.

> run "python -c \"from sklearn.model_selection import train_test_split; import numpy as np; X=np.random.rand(100,4); y=np.random.randint(0,2,100); X_tr,X_te,y_tr,y_te=train_test_split(X,y,test_size=0.2,random_state=42); X_tr,X_val,y_tr,y_val=train_test_split(X_tr,y_tr,test_size=0.2,random_state=42); print(f'train={len(X_tr)} val={len(X_val)} test={len(X_te)}')\""

```markscript
let total = 100
let test_size = 0.2
let val_size = 0.16
# train=64, val=16, test=20
# 80-20 train-test, then 80-20 train-val of training
```

---

## binarize

Convert numerical features to binary values based on a threshold.

> run "python -c \"from sklearn.preprocessing import Binarizer; import numpy as np; X=np.array([[0.1],[0.8],[0.3],[0.6]]); b=Binarizer(threshold=0.5); Xb=b.fit_transform(X); print(Xb)\""

```markscript
let X = [0.1 0.8 0.3 0.6]
let threshold = 0.5
# [[0]
#  [1]
#  [0]
#  [1]]
```

---

## polynomial_features

Generate polynomial and interaction features.

> run "python -c \"from sklearn.preprocessing import PolynomialFeatures; import numpy as np; X=np.array([[1,2],[3,4]]); poly=PolynomialFeatures(degree=2); Xp=poly.fit_transform(X); print(f'feature_names={poly.get_feature_names_out()}'); print(Xp)\""

```markscript
let X = [[1 2] [3 4]]
let degree = 2
# features: [1, x0, x1, x0^2, x0*x1, x1^2]
# [[ 1.  1.  2.  1.  2.  4.]
#  [ 1.  3.  4.  9. 12. 16.]]
```
