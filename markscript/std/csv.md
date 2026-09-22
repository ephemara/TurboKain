# CSV

Comma-separated values: reading, writing, filtering, and analysis routines.

## read

Parse a CSV string into a table: a list of dicts keyed by header row.

> read file "data.csv"

```markscript
let csv_text = `name,age,city\nAlice,30,NYC\nBob,25,LA\nCarol,35,Chicago`

let rows = csv.read(csv_text)
# rows = [
#   {"name":"Alice","age":"30","city":"NYC"},
#   {"name":"Bob","age":"25","city":"LA"},
#   {"name":"Carol","age":"35","city":"Chicago"}
# ]

> assert rows[0]["name"] "Alice"
> assert rows[2]["city"] "Chicago"
```

## write

Serialize a table (list of dicts) back to CSV text.

> write file "output.csv" content

```markscript
let rows = []
rows[0] = {"product":"Widget","price":"9.99","qty":"100"}
rows[1] = {"product":"Gadget","price":"24.99","qty":"50"}

let out = csv.write(rows)
# product,price,qty
# Widget,9.99,100
# Gadget,24.99,50

> write file "inventory.csv" out
```

## headers

Extract the column header names from a CSV string.

> print "Headers found"

```markscript
let csv_text = `id,name,email,role\n1,admin,admin@x.com,admin`

let cols = csv.headers(csv_text)
# ["id","name","email","role"]

> assert cols[0] "id"
> assert cols[3] "role"
```

## rows

Get the data rows (without headers) as a list of lists.

> run "python -c \"import csv; print(list(csv.reader(open('f.csv'))))\""

```markscript
let csv_text = `a,b,c\n1,2,3\n4,5,6\n7,8,9`

let data = csv.rows(csv_text)
# [["1","2","3"],["4","5","6"],["7","8","9"]]

> assert data[1][0] "4"
> assert data[2][2] "9"
```

## filter

Return only rows where a column matches a condition.

> run "python -c \"import csv; ...\""

```markscript
let csv_text = `city,state,pop\nNYC,NY,8336817\nLA,CA,3898747\nChicago,IL,2746388`

let rows = csv.read(csv_text)

# filter to rows where pop > 3_000_000
let big = csv.filter(rows, "pop", fn(v) -> int(v) > 3000000)

> assert csv.length(big) 2
> assert big[0]["city"] "NYC"
```

## sort

Sort the table by a column, ascending or descending.

> run "python -c \"import csv; ... sort ...\""

```markscript
let csv_text = `name,salary\nAlice,95000\nBob,120000\nCarol,72000`

let rows = csv.read(csv_text)

let sorted = csv.sort(rows, "salary", "desc")
# Carol(72000), Alice(95000), Bob(120000) --- ascending sort then reversed

> assert sorted[0]["name"] "Bob"
> assert sorted[2]["name"] "Carol"
```

## stats

Compute summary statistics for a numeric column.

> print "Column stats computed"

```markscript
let csv_text = `val\n10\n20\n30\n40\n50`

let rows = csv.read(csv_text)
let s = csv.stats(rows, "val")

> assert s["count"] 5
> assert s["min"] 10
> assert s["max"] 50
> assert s["mean"] 30
> assert s["sum"] 150
```

## to_json

Convert a CSV table to a JSON string.

> run "python -c \"import csv,json, sys; ...\""

```markscript
let csv_text = `name,role\nAlice,admin\nBob,user`

let json_str = csv.to_json(csv_text)
# [{"name":"Alice","role":"admin"},{"name":"Bob","role":"user"}]

> run "echo '" + json_str + "' | jq ."
```
