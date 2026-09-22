# Classify

MarkScript classification - supervised learning models for predicting
categorical labels. Dispatches to Python's `scikit-learn`.

---

## logistic

Train and predict using logistic regression.

> run "python -c \"from sklearn.linear_model import LogisticRegression; from sklearn.datasets import make_classification; X,y=make_classification(n_samples=100,n_features=4,random_state=0); m=LogisticRegression(); m.fit(X,y); pred=m.predict(X[:5]); print(pred)\""

```markscript
let n_samples = 100
let n_features = 4
# logistic regression trained on 100 samples
# predictions: [0 1 0 0 1]
# outputs class probabilities via predict_proba
```

---

## svm

Train and predict using Support Vector Machine.

> run "python -c \"from sklearn import svm; from sklearn.datasets import make_classification; X,y=make_classification(n_samples=100,random_state=0); clf=svm.SVC(kernel='rbf'); clf.fit(X,y); pred=clf.predict(X[:5]); print(pred)\""

```markscript
let n_samples = 100
let kernel = "rbf"
# SVM with RBF kernel trained on 100 samples
# predictions: [0 1 1 0 1]
```

---

## decision_tree

Train and predict using a decision tree.

> run "python -c \"from sklearn.tree import DecisionTreeClassifier; from sklearn.datasets import make_classification; X,y=make_classification(n_samples=100,random_state=0); dt=DecisionTreeClassifier(max_depth=3); dt.fit(X,y); pred=dt.predict(X[:5]); print(pred)\""

```markscript
let max_depth = 3
let n_samples = 100
# decision tree with max depth 3
# predictions: [0 1 0 0 0]
```

---

## random_forest

Train and predict using a random forest ensemble.

> run "python -c \"from sklearn.ensemble import RandomForestClassifier; from sklearn.datasets import make_classification; X,y=make_classification(n_samples=100,random_state=0); rf=RandomForestClassifier(n_estimators=100); rf.fit(X,y); pred=rf.predict(X[:5]); print(pred)\""

```markscript
let n_estimators = 100
# random forest with 100 trees
# predictions: [0 1 0 0 1]
# also provides feature_importances_
```

---

## naive_bayes

Train and predict using Gaussian Naive Bayes.

> run "python -c \"from sklearn.naive_bayes import GaussianNB; from sklearn.datasets import make_classification; X,y=make_classification(n_samples=100,random_state=0); nb=GaussianNB(); nb.fit(X,y); pred=nb.predict(X[:5]); print(pred)\""

```markscript
let n_samples = 100
# Gaussian Naive Bayes trained on 100 samples
# assumes features follow normal distribution
# predictions: [0 1 0 0 1]
```

---

## knn

Train and predict using k-Nearest Neighbors.

> run "python -c \"from sklearn.neighbors import KNeighborsClassifier; from sklearn.datasets import make_classification; X,y=make_classification(n_samples=100,random_state=0); knn=KNeighborsClassifier(n_neighbors=5); knn.fit(X,y); pred=knn.predict(X[:5]); print(pred)\""

```markscript
let k = 5
let n_samples = 100
# 5-NN classifier trained on 100 samples
# predictions: [0 1 0 1 0]
# based on majority vote of 5 nearest neighbors
```

---

## gradient_boosting

Train and predict using gradient boosted trees.

> run "python -c \"from sklearn.ensemble import GradientBoostingClassifier; from sklearn.datasets import make_classification; X,y=make_classification(n_samples=100,random_state=0); gb=GradientBoostingClassifier(n_estimators=50); gb.fit(X,y); pred=gb.predict(X[:5]); print(pred)\""

```markscript
let n_estimators = 50
# gradient boosting with 50 stages
# predictions: [0 1 0 0 1]
```

---

## xgboost

Train and predict using XGBoost (if installed).

> run "python -c \"try: from xgboost import XGBClassifier; from sklearn.datasets import make_classification; X,y=make_classification(n_samples=100,random_state=0); xgb=XGBClassifier(n_estimators=50); xgb.fit(X,y); pred=xgb.predict(X[:5]); print(pred); except Exception as e: print(f'XGBoost not installed: {e}')\""

```markscript
let n_estimators = 50
# XGBoost with 50 trees (if installed)
# predictions: [0 1 0 0 1]
```

---

## predict_proba

Get class probability estimates from a trained classifier.

> run "python -c \"from sklearn.ensemble import RandomForestClassifier; from sklearn.datasets import make_classification; X,y=make_classification(n_samples=100,random_state=0); rf=RandomForestClassifier(); rf.fit(X,y); proba=rf.predict_proba(X[:3]); print(proba)\""

```markscript
let n_samples = 3
# [[0.92 0.08]
#  [0.23 0.77]
#  [0.64 0.36]]
# row = sample, columns = class probabilities
```

---

## classification_report

Generate a detailed classification report (precision, recall, f1 per class).

> run "python -c \"from sklearn.metrics import classification_report; y_true=[0,0,1,1,0,1,1,0,0,1]; y_pred=[0,0,1,0,0,1,1,0,1,1]; print(classification_report(y_true,y_pred))\""

```markscript
let y_true = [0 0 1 1 0 1 1 0 0 1]
let y_pred = [0 0 1 0 0 1 1 0 1 1]
#               precision  recall  f1-score  support
#         0       0.80     0.80     0.80       5
#         1       0.80     0.80     0.80       5
#   accuracy                         0.80      10
```
