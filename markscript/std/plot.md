# Plot

MarkScript data visualization - plotting and charting through Python's
Matplotlib. Dispatches through `> run "python ..."`.

---

## line

Create a line plot from x and y data.

> run "python -c \"import matplotlib.pyplot as plt; plt.plot([1,2,3,4,5],[2,4,6,8,10]); plt.savefig('line.png')\""

```markscript
let x = [1 2 3 4 5]
let y = [2 4 6 8 10]
# line plot saved as line.png
```

---

## bar

Create a bar chart.

> run "python -c \"import matplotlib.pyplot as plt; plt.bar(['A','B','C','D'],[3,7,2,5]); plt.savefig('bar.png')\""

```markscript
let categories = ["A" "B" "C" "D"]
let values = [3 7 2 5]
# bar chart saved as bar.png
```

---

## scatter

Create a scatter plot of x and y points.

> run "python -c \"import matplotlib.pyplot as plt; import numpy as np; x=np.random.rand(50); y=np.random.rand(50); plt.scatter(x,y); plt.savefig('scatter.png')\""

```markscript
let n = 50
let x = [0.23 0.67 0.12 0.89 ...]
let y = [0.45 0.33 0.78 0.21 ...]
# scatter plot saved as scatter.png
```

---

## histogram

Create a histogram from data values.

> run "python -c \"import matplotlib.pyplot as plt; import numpy as np; data=np.random.normal(0,1,1000); plt.hist(data,bins=30); plt.savefig('hist.png')\""

```markscript
let data = 1000
let bins = 30
# histogram with 30 bins from 1000 normal samples
# saved as hist.png
```

---

## pie

Create a pie chart from category values.

> run "python -c \"import matplotlib.pyplot as plt; plt.pie([30,25,20,15,10],labels=['A','B','C','D','E']); plt.savefig('pie.png')\""

```markscript
let values = [30 25 20 15 10]
let labels = ["A" "B" "C" "D" "E"]
# pie chart saved as pie.png
```

---

## heatmap

Create a heatmap from a 2D matrix.

> run "python -c \"import matplotlib.pyplot as plt; import numpy as np; data=np.random.rand(10,10); plt.imshow(data,cmap='viridis'); plt.colorbar(); plt.savefig('heatmap.png')\""

```markscript
let rows = 10
let cols = 10
# 10x10 heatmap with viridis colormap
# saved as heatmap.png
```

---

## save

Save the current figure to a file.

> run "python -c \"import matplotlib.pyplot as plt; plt.plot([1,2,3],[1,2,3]); plt.savefig('output.png',dpi=300,bbox_inches='tight')\""

```markscript
let filename = "output.png"
let dpi = 300
# figure saved at 300 DPI with tight bounding box
```

---

## show

Display the plot interactively (GUI popup).

> run "python -c \"import matplotlib.pyplot as plt; plt.plot([1,2,3],[1,2,3]); plt.show()\""

```markscript
# opens an interactive matplotlib window
```

---

## title

Set the plot title.

> run "python -c \"import matplotlib.pyplot as plt; plt.plot([1,2,3],[1,2,3]); plt.title('My Chart'); plt.savefig('titled.png')\""

```markscript
let text = "My Chart"
# sets "My Chart" as the plot title
```

---

## legend

Add a legend to the plot.

> run "python -c \"import matplotlib.pyplot as plt; plt.plot([1,2,3],[1,2,3],label='line1'); plt.plot([1,2,3],[3,2,1],label='line2'); plt.legend(); plt.savefig('legend.png')\""

```markscript
let labels = ["line1" "line2"]
# legend with two entries
```

---

## xlabel

Set the x-axis label.

> run "python -c \"import matplotlib.pyplot as plt; plt.plot([1,2,3],[1,2,3]); plt.xlabel('Time (s)'); plt.savefig('xlabel.png')\""

```markscript
let label = "Time (s)"
# x-axis labeled "Time (s)"
```

---

## ylabel

Set the y-axis label.

> run "python -c \"import matplotlib.pyplot as plt; plt.plot([1,2,3],[1,2,3]); plt.ylabel('Value'); plt.savefig('ylabel.png')\""

```markscript
let label = "Value"
# y-axis labeled "Value"
```

---

## subplots

Create multiple subplots in a single figure.

> run "python -c \"import matplotlib.pyplot as plt; fig,(ax1,ax2)=plt.subplots(1,2); ax1.plot([1,2,3],[1,2,3]); ax2.bar(['A','B'],[3,7]); plt.savefig('subplots.png')\""

```markscript
let rows = 1
let cols = 2
# figure with 1 row, 2 columns of subplots
# left: line plot, right: bar chart
# saved as subplots.png
```

---

## style

Set the plot style/theme.

> run "python -c \"import matplotlib.pyplot as plt; plt.style.use('seaborn-v0_8-darkgrid'); plt.plot([1,2,3],[1,2,3]); plt.savefig('styled.png')\""

```markscript
let theme = "seaborn-v0_8-darkgrid"
# plot with seaborn darkgrid style applied
```
