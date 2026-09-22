# Pandas

MarkScript data frame operations --- reading, transforming, and summarizing
tabular data through Python's pandas library.

---

## read_csv

Read a CSV file into a DataFrame.

> run "python -c \"import pandas as pd; df=pd.read_csv('data.csv'); print(df.shape); print(df.columns.tolist())\""

```markscript
let path = "data.csv"
let shape = [1000 8]
# DataFrame with 1000 rows, 8 columns
```

---

## head

Return the first N rows of a DataFrame.

> run "python -c \"import pandas as pd; df=pd.read_csv('data.csv'); print(df.head(5))\""

```markscript
let n = 5
# |   | col_a | col_b | col_c |
# |---|-------|-------|-------|
# | 0 | 1.2   | foo   | 42    |
# | 1 | 3.4   | bar   | 17    |
# | 2 | 5.6   | baz   | 88    |
# | 3 | 7.8   | qux   | 34    |
# | 4 | 9.0   | quux  | 56    |
```

---

## tail

Return the last N rows of a DataFrame.

> run "python -c \"import pandas as pd; df=pd.read_csv('data.csv'); print(df.tail(3))\""

```markscript
let n = 3
# last 3 rows of the DataFrame
```

---

## describe

Generate descriptive statistics of a DataFrame.

> run "python -c \"import pandas as pd; df=pd.read_csv('data.csv'); print(df.describe())\""

```markscript
let df = "data.csv"
# |       | col_a  | col_b  |
# |-------|--------|--------|
# | count | 1000   | 1000   |
# | mean  | 52.3   | 48.7   |
# | std   | 28.1   | 25.4   |
# | min   | 0.0    | 0.0    |
# | 25%   | 25.6   | 24.1   |
# | 50%   | 51.2   | 49.3   |
# | 75%   | 78.9   | 72.8   |
# | max   | 100.0  | 99.1   |
```

---

## groupby

Group a DataFrame by a column and compute an aggregation.

> run "python -c \"import pandas as pd; df=pd.read_csv('data.csv'); print(df.groupby('category')['value'].mean())\""

```markscript
let by = "category"
let col = "value"
# category
# A    34.5
# B    67.2
# C    51.8
# Name: value, dtype: float64
```

---

## merge

Merge two DataFrames on a key column.

> run "python -c \"import pandas as pd; a=pd.DataFrame({'id':[1,2,3],'x':['a','b','c']}); b=pd.DataFrame({'id':[1,2,4],'y':[10,20,30]}); print(pd.merge(a,b,on='id'))\""

```markscript
let left = [[1 "a"] [2 "b"] [3 "c"]]
let right = [[1 10] [2 20] [4 30]]
#   id x   y
# 0 1  a   10
# 1 2  b   20
# inner merge on 'id'
```

---

## pivot

Reshape a DataFrame from long to wide format using a pivot table.

> run "python -c \"import pandas as pd; df=pd.DataFrame({'date':['2024-01','2024-01','2024-02','2024-02'],'type':['A','B','A','B'],'val':[10,20,15,25]}); print(df.pivot(index='date',columns='type',values='val'))\""

```markscript
let df = [[2024-01 "A" 10] [2024-01 "B" 20] [2024-02 "A" 15] [2024-02 "B" 25]]
# type      A   B
# date
# 2024-01  10  20
# 2024-02  15  25
```

---

## to_csv

Write a DataFrame to a CSV file.

> run "python -c \"import pandas as pd; df=pd.DataFrame({'x':[1,2,3],'y':[4,5,6]}); df.to_csv('output.csv',index=False)\""

```markscript
let data = [[1 4] [2 5] [3 6]]
let path = "output.csv"
# writes to output.csv without index column
```

---

## dropna

Remove rows with missing values.

> run "python -c \"import pandas as pd; df=pd.DataFrame({'a':[1,None,3],'b':[4,5,None]}); print(df.dropna())\""

```markscript
let df = [[1 4] [None 5] [3 None]]
# dropna removes rows with any NaN
# result = [[1 4]]
```

---

## fillna

Fill missing values with a specified value or method.

> run "python -c \"import pandas as pd; df=pd.DataFrame({'a':[1,None,3]}); print(df.fillna(0))\""

```markscript
let df = [1 None 3]
let fill = 0
# [1 0 3]
```

---

## unique

Return unique values from a column.

> run "python -c \"import pandas as pd; df=pd.DataFrame({'cat':['a','b','a','c','b','a']}); print(df['cat'].unique())\""

```markscript
let col = ["a" "b" "a" "c" "b" "a"]
# unique = ["a" "b" "c"]
```

---

## sort

Sort a DataFrame by one or more columns.

> run "python -c \"import pandas as pd; df=pd.DataFrame({'name':['z','a','m'],'val':[3,1,2]}); print(df.sort_values('val'))\""

```markscript
let data = [["z" 3] ["a" 1] ["m" 2]]
let by = "val"
# sorted by val ascending
# [[a 1] [m 2] [z 3]]
```
