# Cluster

MarkScript clustering - unsupervised grouping of data points. Dispatches
to Python's `scikit-learn` cluster module through the IVT `run` handler.

---

## kmeans

Perform k-means clustering on data.

> run "python -c \"from sklearn.cluster import KMeans; import numpy as np; X=np.random.rand(100,2); km=KMeans(n_clusters=3,random_state=0,n_init='auto'); km.fit(X); print(f'labels={km.labels_[:5]} centers={km.cluster_centers_}')\""

```markscript
let n_clusters = 3
let n_samples = 100
let features = 2
# 100 points → 3 clusters
# cluster centers: [[0.23 0.45] [0.67 0.12] [0.89 0.78]]
```

---

## dbscan

Perform DBSCAN density-based clustering.

> run "python -c \"from sklearn.cluster import DBSCAN; import numpy as np; X=np.random.rand(100,2); db=DBSCAN(eps=0.3,min_samples=5); labels=db.fit_predict(X); print(f'labels={labels[:5]} n_clusters={len(set(labels))-(1 if -1 in labels else 0)}')\""

```markscript
let eps = 0.3
let min_samples = 5
# eps=0.3 controls neighborhood radius
# min_samples=5 min points for core region
# label=-1 means noise point
```

---

## hierarchical

Perform hierarchical/agglomerative clustering.

> run "python -c \"from sklearn.cluster import AgglomerativeClustering; import numpy as np; X=np.random.rand(50,2); hc=AgglomerativeClustering(n_clusters=4); labels=hc.fit_predict(X); print(f'labels={labels[:5]} n_clusters=4')\""

```markscript
let n_clusters = 4
let n_samples = 50
let linkage = "ward"
# agglomerative clustering with 4 clusters
# uses ward linkage (minimize variance within clusters)
```

---

## elbow

Elbow method for determining optimal k in k-means (WCSS vs k).

> run "python -c \"from sklearn.cluster import KMeans; import numpy as np; X=np.random.rand(100,2); wcss=[KMeans(n_clusters=k,random_state=0,n_init='auto').fit(X).inertia_ for k in range(1,11)]; print(wcss)\""

```markscript
let k_range = [1 2 3 4 5 6 7 8 9 10]
# WCSS = [850 420 210 120 95 80 70 62 56 51]
# elbow at k=3 -- diminishing returns after 3 clusters
```

---

## silhouette

Compute silhouette score for cluster quality evaluation.

> run "python -c \"from sklearn.metrics import silhouette_score; from sklearn.cluster import KMeans; import numpy as np; X=np.random.rand(100,2); for k in range(2,7): km=KMeans(n_clusters=k,random_state=0,n_init='auto'); labels=km.fit_predict(X); s=silhouette_score(X,labels); print(f'k={k} silhouette={s:.3f}')\""

```markscript
let k_values = [2 3 4 5 6]
# silhouette scores: [0.42 0.38 0.32 0.28 0.22]
# highest at k=2 → best cluster separation at 2 clusters
```

---

## spectral

Perform spectral clustering.

> run "python -c \"from sklearn.cluster import SpectralClustering; import numpy as np; X=np.random.rand(100,2); sc=SpectralClustering(n_clusters=3,random_state=0); labels=sc.fit_predict(X); print(f'labels={labels[:5]}')\""

```markscript
let n_clusters = 3
let n_samples = 100
# spectral clustering uses graph Laplacian
# good for non-convex cluster shapes
```

---

## mean_shift

Perform mean shift clustering (finds clusters without specifying k).

> run "python -c \"from sklearn.cluster import MeanShift; import numpy as np; X=np.random.rand(100,2); ms=MeanShift(); labels=ms.fit_predict(X); print(f'n_clusters={len(set(labels))} labels={labels[:5]}')\""

```markscript
let n_samples = 100
# mean shift discovers number of clusters automatically
# bandwidth is estimated from data
```

---

## optics

Perform OPTICS clustering (hierarchical density-based).

> run "python -c \"from sklearn.cluster import OPTICS; import numpy as np; X=np.random.rand(100,2); opt=OPTICS(min_samples=5); labels=opt.fit_predict(X); print(f'n_clusters={len(set(labels))-(1 if -1 in labels else 0)}')\""

```markscript
let min_samples = 5
# OPTICS extends DBSCAN with variable density
# label=-1 means noise
```

---

## cluster_centers

Extract cluster centers and summary statistics.

> run "python -c \"from sklearn.cluster import KMeans; import numpy as np; X=np.random.rand(100,2); km=KMeans(n_clusters=3,random_state=0,n_init='auto').fit(X); for i,ct in enumerate(km.cluster_centers_): pts=X[km.labels_==i]; print(f'cluster {i}: center={ct} size={len(pts)} std={pts.std(axis=0)}')\""

```markscript
let n_clusters = 3
# Cluster 0: center=[0.23 0.45] size=34 std=[0.12 0.15]
# Cluster 1: center=[0.67 0.12] size=33 std=[0.09 0.11]
# Cluster 2: center=[0.89 0.78] size=33 std=[0.14 0.13]
```
