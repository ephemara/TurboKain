# Metrics

MarkScript evaluation metrics - quantifying model performance through
classification, regression, and clustering metrics. Dispatches to
Python's `scikit-learn` metrics module.

---

## accuracy

Compute classification accuracy (fraction of correct predictions).

> run "python -c \"from sklearn.metrics import accuracy_score; y_true=[0,1,0,1,0,1]; y_pred=[0,1,0,0,0,1]; print(accuracy_score(y_true,y_pred))\""

```markscript
let y_true = [0 1 0 1 0 1]
let y_pred = [0 1 0 0 0 1]
# 5 correct out of 6
let accuracy = 0.833
```

---

## precision

Compute precision: TP / (TP + FP).

> run "python -c \"from sklearn.metrics import precision_score; y_true=[0,1,0,1,0,1]; y_pred=[0,1,0,0,1,1]; print(precision_score(y_true,y_pred))\""

```markscript
let y_true = [0 1 0 1 0 1]
let y_pred = [0 1 0 0 1 1]
# TP=2, FP=1 → 2/3
let precision = 0.667
```

---

## recall

Compute recall: TP / (TP + FN).

> run "python -c \"from sklearn.metrics import recall_score; y_true=[0,1,0,1,0,1]; y_pred=[0,1,0,0,1,1]; print(recall_score(y_true,y_pred))\""

```markscript
let y_true = [0 1 0 1 0 1]
let y_pred = [0 1 0 0 1 1]
# TP=2, FN=1 → 2/3
let recall = 0.667
```

---

## f1

Compute the F1 score (harmonic mean of precision and recall).

> run "python -c \"from sklearn.metrics import f1_score; y_true=[0,1,0,1,0,1]; y_pred=[0,1,0,0,1,1]; print(f1_score(y_true,y_pred))\""

```markscript
let y_true = [0 1 0 1 0 1]
let y_pred = [0 1 0 0 1 1]
# 2 * (prec * rec) / (prec + rec)
# 2 * (0.667 * 0.667) / (0.667 + 0.667)
let f1 = 0.667
```

---

## mae

Compute Mean Absolute Error for regression.

> run "python -c \"from sklearn.metrics import mean_absolute_error; y_true=[3,5,7,9]; y_pred=[2.8,5.2,7.1,8.7]; print(mean_absolute_error(y_true,y_pred))\""

```markscript
let y_true = [3 5 7 9]
let y_pred = [2.8 5.2 7.1 8.7]
# MAE = (|3-2.8| + |5-5.2| + |7-7.1| + |9-8.7|) / 4
# MAE = (0.2 + 0.2 + 0.1 + 0.3) / 4
let mae = 0.2
```

---

## mse

Compute Mean Squared Error for regression.

> run "python -c \"from sklearn.metrics import mean_squared_error; y_true=[3,5,7,9]; y_pred=[2.8,5.2,7.1,8.7]; print(mean_squared_error(y_true,y_pred))\""

```markscript
let y_true = [3 5 7 9]
let y_pred = [2.8 5.2 7.1 8.7]
# MSE = ((3-2.8)^2 + (5-5.2)^2 + (7-7.1)^2 + (9-8.7)^2) / 4
# MSE = (0.04 + 0.04 + 0.01 + 0.09) / 4
let mse = 0.045
```

---

## rmse

Compute Root Mean Squared Error for regression.

> run "python -c \"from sklearn.metrics import mean_squared_error; import numpy as np; y_true=[3,5,7,9]; y_pred=[2.8,5.2,7.1,8.7]; print(np.sqrt(mean_squared_error(y_true,y_pred)))\""

```markscript
let y_true = [3 5 7 9]
let y_pred = [2.8 5.2 7.1 8.7]
# RMSE = sqrt(MSE)
# RMSE = sqrt(0.045)
let rmse = 0.212
```

---

## r2

Compute the coefficient of determination (R²) for regression.

> run "python -c \"from sklearn.metrics import r2_score; y_true=[3,5,7,9]; y_pred=[3.1,5.0,6.9,9.2]; print(r2_score(y_true,y_pred))\""

```markscript
let y_true = [3 5 7 9]
let y_pred = [3.1 5.0 6.9 9.2]
# R² = 1 - SS_res / SS_tot
# close to 1 means excellent fit
let r2 = 0.985
```

---

## confusion_matrix

Compute the confusion matrix for classification evaluation.

> run "python -c \"from sklearn.metrics import confusion_matrix; y_true=[0,1,0,1,0,1,0,0,1,1]; y_pred=[0,1,0,0,0,1,1,0,1,1]; cm=confusion_matrix(y_true,y_pred); print(cm)\""

```markscript
let y_true = [0 1 0 1 0 1 0 0 1 1]
let y_pred = [0 1 0 0 0 1 1 0 1 1]
# [[4 1]   TN=4 FP=1
#  [2 3]]  FN=2 TP=3
```

---

## roc_auc

Compute the Area Under the ROC Curve (AUC-ROC).

> run "python -c \"from sklearn.metrics import roc_auc_score; y_true=[0,0,1,1]; y_score=[0.1,0.4,0.35,0.8]; print(roc_auc_score(y_true,y_score))\""

```markscript
let y_true = [0 0 1 1]
let y_scores = [0.1 0.4 0.35 0.8]
# AUC = 0.75
# measures ranking quality of probability scores
```

---

## log_loss

Compute log loss (cross-entropy loss) for probabilistic predictions.

> run "python -c \"from sklearn.metrics import log_loss; y_true=[0,1,0,1]; y_prob=[[0.9,0.1],[0.2,0.8],[0.8,0.2],[0.1,0.9]]; print(log_loss(y_true,y_prob))\""

```markscript
let y_true = [0 1 0 1]
# y_prob = [P(class0) P(class1)]
# [[0.9 0.1]  [0.2 0.8]  [0.8 0.2]  [0.1 0.9]]
let log_loss = 0.226
# lower is better (perfect = 0)
```

---

## silhouette_score

Compute the mean silhouette coefficient for cluster quality.

> run "python -c \"from sklearn.metrics import silhouette_score; from sklearn.datasets import make_blobs; X,y=make_blobs(n_samples=100,n_features=2,centers=3,random_state=0); print(silhouette_score(X,y))\""

```markscript
let n_clusters = 3
let n_samples = 100
# silhouette_score = 0.68
# range: -1 (bad) to 1 (excellent)
# >0.5 indicates reasonable cluster separation
```

---

## adjusted_rand

Compute the Adjusted Rand Index (ARI) for cluster agreement.

> run "python -c \"from sklearn.metrics import adjusted_rand_score; y_true=[0,0,1,1,2,2]; y_pred=[0,0,1,2,2,1]; print(adjusted_rand_score(y_true,y_pred))\""

```markscript
let y_true = [0 0 1 1 2 2]
let y_pred = [0 0 1 2 2 1]
# ARI = 0.556
# measures similarity between clusterings
# 1.0 = perfect match, 0.0 = random
```
