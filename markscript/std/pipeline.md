# Pipeline

MarkScript ML pipelines - composing preprocessing and model steps into
reproducible workflows. Dispatches to Python's `scikit-learn` `Pipeline`.

---

## create

Create a machine learning pipeline from a sequence of steps.

> run "python -c \"from sklearn.pipeline import Pipeline; from sklearn.preprocessing import StandardScaler; from sklearn.ensemble import RandomForestClassifier; pipeline=Pipeline([('scaler',StandardScaler()),('clf',RandomForestClassifier())]); print(pipeline)\""

```markscript
let steps = [["scaler" "StandardScaler"] ["clf" "RandomForestClassifier"]]
# Pipeline(steps=[('scaler', StandardScaler()), ('clf', RandomForestClassifier())])
```

---

## fit

Fit the pipeline to training data.

> run "python -c \"from sklearn.pipeline import Pipeline; from sklearn.preprocessing import StandardScaler; from sklearn.ensemble import RandomForestClassifier; import numpy as np; X=np.random.rand(100,4); y=np.random.randint(0,2,100); pipeline=Pipeline([('scaler',StandardScaler()),('clf',RandomForestClassifier())]); pipeline.fit(X,y); print('pipeline fitted')\""

```markscript
let X = np.random.rand(100, 4)
let y = np.random.randint(0, 2, 100)
# pipeline fitted to 100 samples
# each step.fit() is called in sequence
```

---

## transform

Transform data through the pipeline (without final estimator).

> run "python -c \"from sklearn.pipeline import Pipeline; from sklearn.preprocessing import StandardScaler; from sklearn.decomposition import PCA; import numpy as np; X=np.random.rand(100,5); pipeline=Pipeline([('scaler',StandardScaler()),('pca',PCA(n_components=2))]); Xt=pipeline.fit_transform(X); print(f'X transformed: {Xt.shape}')\""

```markscript
let X = [[100 samples, 5 features]]
# transformed shape: (100, 2)
# data scaled then reduced to 2 PCA components
```

---

## predict

Generate predictions using a fitted pipeline.

> run "python -c \"from sklearn.pipeline import Pipeline; from sklearn.preprocessing import StandardScaler; from sklearn.ensemble import RandomForestClassifier; import numpy as np; X=np.random.rand(100,4); y=np.random.randint(0,2,100); pipeline=Pipeline([('scaler',StandardScaler()),('clf',RandomForestClassifier())]); pipeline.fit(X,y); preds=pipeline.predict(X[:5]); print(preds)\""

```markscript
let n_samples = 5
# predictions: [0 1 0 1 1]
# data automatically scaled before prediction
```

---

## save

Save a fitted pipeline to disk for later use.

> run "python -c \"import joblib; from sklearn.pipeline import Pipeline; from sklearn.preprocessing import StandardScaler; from sklearn.ensemble import RandomForestClassifier; import numpy as np; X=np.random.rand(100,4); y=np.random.randint(0,2,100); pipeline=Pipeline([('scaler',StandardScaler()),('clf',RandomForestClassifier())]); pipeline.fit(X,y); joblib.dump(pipeline,'pipeline.joblib'); print('saved')\""

```markscript
let path = "pipeline.joblib"
# pipeline saved to disk
# includes all fitted parameters from every step
```

---

## load

Load a previously saved pipeline from disk.

> run "python -c \"import joblib; pipeline=joblib.load('pipeline.joblib'); print(f'loaded: {pipeline}')\""

```markscript
let path = "pipeline.joblib"
# Pipeline loaded from disk
# ready for predict() or transform()
```

---

## params

Get or set pipeline parameters.

> run "python -c \"from sklearn.pipeline import Pipeline; from sklearn.preprocessing import StandardScaler; from sklearn.ensemble import RandomForestClassifier; pipeline=Pipeline([('scaler',StandardScaler()),('clf',RandomForestClassifier())]); params=pipeline.get_params(); print([k for k in params.keys()][:5])\""

```markscript
# Pipeline parameters:
# scaler__copy: True
# scaler__with_mean: True
# scaler__with_std: True
# clf__bootstrap: True
# clf__max_depth: None
# clf__n_estimators: 100
# ... accessible via set_params()
```

---

## cross_validate

Cross-validate an entire pipeline.

> run "python -c \"from sklearn.pipeline import Pipeline; from sklearn.preprocessing import StandardScaler; from sklearn.ensemble import RandomForestClassifier; from sklearn.model_selection import cross_val_score; import numpy as np; X=np.random.rand(100,4); y=np.random.randint(0,2,100); pipeline=Pipeline([('scaler',StandardScaler()),('clf',RandomForestClassifier())]); scores=cross_val_score(pipeline,X,y,cv=5); print(f'scores={scores} mean={scores.mean():.3f}')\""

```markscript
let cv = 5
# cross-validation scores: [0.90 0.85 0.95 0.88 0.92]
# mean: 0.90
# each fold: fit → transform → predict
```

---

## grid_search

Perform grid search over pipeline parameters.

> run "python -c \"from sklearn.pipeline import Pipeline; from sklearn.preprocessing import StandardScaler; from sklearn.svm import SVC; from sklearn.model_selection import GridSearchCV; import numpy as np; X=np.random.rand(100,4); y=np.random.randint(0,2,100); pipeline=Pipeline([('scaler',StandardScaler()),('svm',SVC())]); param_grid={'svm__C':[0.1,1,10],'svm__kernel':['linear','rbf']}; gs=GridSearchCV(pipeline,param_grid,cv=3); gs.fit(X,y); print(f'best_params={gs.best_params_} best_score={gs.best_score_:.3f}')\""

```markscript
let param_grid = {"svm__C": [0.1 1 10] "svm__kernel": ["linear" "rbf"]}
# best_params: {'svm__C': 10, 'svm__kernel': 'rbf'}
# best_score: 0.923
```

---

## make_pipeline

Quickly create a pipeline using the shorthand constructor.

> run "python -c \"from sklearn.pipeline import make_pipeline; from sklearn.preprocessing import StandardScaler, MinMaxScaler; from sklearn.ensemble import GradientBoostingClassifier; pipeline=make_pipeline(StandardScaler(),GradientBoostingClassifier(n_estimators=50)); print(pipeline)\""

```markscript
# make_pipeline automatically names steps by class
# Pipeline(steps=[('standardscaler', StandardScaler()),
#                 ('gradientboostingclassifier', GradientBoostingClassifier())])
```

---

## feature_union

Combine multiple feature extraction pipelines (FeatureUnion).

> run "python -c \"from sklearn.pipeline import FeatureUnion, Pipeline; from sklearn.decomposition import PCA; from sklearn.preprocessing import StandardScaler; from sklearn.ensemble import RandomForestClassifier; import numpy as np; X=np.random.rand(100,10); union=FeatureUnion([('pca',PCA(n_components=3)),('scaler',StandardScaler())]); pipeline=Pipeline([('union',union),('clf',RandomForestClassifier())]); pipeline.fit(X,np.random.randint(0,2,100)); print('pipeline with FeatureUnion fitted')\""

```markscript
# FeatureUnion runs transformers in parallel
# PCA reduces to 3 components
# StandardScaler keeps all 10 features (standardized)
# Both outputs are concatenated → 13 features for classifier
```
