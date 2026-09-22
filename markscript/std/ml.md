# ML

MarkScript machine learning - training, prediction, evaluation, and model
selection. Dispatches to Python's `scikit-learn` through the IVT `run` handler.

---

## train

Train a machine learning model on features and labels.

> run "python -c \"from sklearn.ensemble import RandomForestClassifier; from sklearn.datasets import make_classification; X,y=make_classification(n_samples=100,n_features=4,random_state=0); m=RandomForestClassifier(); m.fit(X,y); print('trained')\""

```markscript
let n_samples = 100
let n_features = 4
let model_type = "RandomForestClassifier"
# model trained on 100 samples with 4 features
```

---

## predict

Generate predictions from a trained model.

> run "python -c \"import numpy as np; from sklearn.ensemble import RandomForestClassifier; from sklearn.datasets import make_classification; X,y=make_classification(n_samples=100,random_state=0); m=RandomForestClassifier(); m.fit(X,y); preds=m.predict(X[:5]); print(preds)\""

```markscript
let model = "trained_model"
let samples = 5
# predictions = [0 1 1 0 1]
# 5 predictions from the trained model
```

---

## evaluate

Evaluate a model on test data and return performance metrics.

> run "python -c \"from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score; y_true=[0,1,1,0,1]; y_pred=[0,1,0,0,1]; print(f'acc={accuracy_score(y_true,y_pred)} prec={precision_score(y_true,y_pred)} rec={recall_score(y_true,y_pred)} f1={f1_score(y_true,y_pred)}')\""

```markscript
let y_true = [0 1 1 0 1]
let y_pred = [0 1 0 0 1]
let accuracy = 0.8
let precision = 1.0
let recall = 0.667
let f1 = 0.8
```

---

## split_data

Split data into training and testing sets.

> run "python -c \"from sklearn.model_selection import train_test_split; import numpy as np; X=np.random.rand(100,4); y=np.random.randint(0,2,100); X_tr,X_te,y_tr,y_te=train_test_split(X,y,test_size=0.2,random_state=42); print(f'train={len(X_tr)} test={len(X_te)}')\""

```markscript
let total = 100
let test_size = 0.2
let train = 80
let test = 20
# 80 training, 20 testing samples
```

---

## cross_validate

Perform k-fold cross-validation and return scores.

> run "python -c \"from sklearn.model_selection import cross_val_score; from sklearn.ensemble import RandomForestClassifier; from sklearn.datasets import make_classification; X,y=make_classification(n_samples=100,random_state=0); m=RandomForestClassifier(); scores=cross_val_score(m,X,y,cv=5); print(f'scores={scores} mean={scores.mean():.3f} std={scores.std():.3f}')\""

```markscript
let k = 5
let scores = [0.92 0.88 0.95 0.91 0.89]
let mean = 0.91
let std = 0.025
```

---

## feature_importance

Extract feature importance scores from a trained model.

> run "python -c \"import numpy as np; from sklearn.ensemble import RandomForestClassifier; from sklearn.datasets import make_classification; X,y=make_classification(n_samples=100,n_features=5,random_state=0); m=RandomForestClassifier(); m.fit(X,y); print(m.feature_importances_)\""

```markscript
let n_features = 5
let importances = [0.12 0.35 0.08 0.28 0.17]
# feature 1 (index 1) is most important at 0.35
```

---

## grid_search

Perform hyperparameter grid search with cross-validation.

> run "python -c \"from sklearn.model_selection import GridSearchCV; from sklearn.ensemble import RandomForestClassifier; from sklearn.datasets import make_classification; X,y=make_classification(n_samples=100,random_state=0); param_grid={'n_estimators':[10,50,100],'max_depth':[3,5,None]}; gs=GridSearchCV(RandomForestClassifier(),param_grid,cv=3); gs.fit(X,y); print(f'best={gs.best_params_} score={gs.best_score_:.3f}')\""

```markscript
let param_grid = [["n_estimators" [10 50 100]] ["max_depth" [3 5 "None"]]]
# best params: {'n_estimators': 50, 'max_depth': 5}
# best score: 0.943
```

---

## confusion_matrix

Compute the confusion matrix for classification results.

> run "python -c \"from sklearn.metrics import confusion_matrix; y_true=[0,1,0,1,0,1,0,0,1,1]; y_pred=[0,1,0,0,0,1,1,0,1,0]; cm=confusion_matrix(y_true,y_pred); print(cm)\""

```markscript
let y_true = [0 1 0 1 0 1 0 0 1 1]
let y_pred = [0 1 0 0 0 1 1 0 1 0]
# [[4 1]
#  [2 3]]
# TN=4  FP=1
# FN=2  TP=3
```

---

## learning_curve

Generate learning curve data (train size vs. score).

> run "python -c \"from sklearn.model_selection import learning_curve; from sklearn.ensemble import RandomForestClassifier; from sklearn.datasets import make_classification; import numpy as np; X,y=make_classification(n_samples=200,random_state=0); sizes,scores_tr,scores_te=learning_curve(RandomForestClassifier(),X,y,train_sizes=[0.1,0.25,0.5,0.75,1.0],cv=3); print(sizes); print(scores_te.mean(axis=1))\""

```markscript
let train_sizes = [0.1 0.25 0.5 0.75 1.0]
# train_scores = [0.95 0.96 0.97 0.97 0.98]
# test_scores  = [0.82 0.87 0.91 0.92 0.93]
# model improves with more data, small gap → good fit
```

---

## save_model

Save a trained model to disk.

> run "python -c \"import pickle; from sklearn.ensemble import RandomForestClassifier; m=RandomForestClassifier(); m.fit([[0,0],[1,1]],[0,1]); pickle.dump(m,open('model.pkl','wb')); print('saved')\""

```markscript
let path = "model.pkl"
# model saved to model.pkl via pickle
```

---

## load_model

Load a trained model from disk.

> run "python -c \"import pickle; m=pickle.load(open('model.pkl','rb')); print(type(m).__name__)\""

```markscript
let path = "model.pkl"
# model loaded: RandomForestClassifier
```
