# Sort

MarkScript file sorting - order, filter duplicates, randomize.
Wraps `sort` via the IVT for ordering operations.

---

## sort_default

Sort lines alphabetically ascending.

> run "sort file.txt"

```markscript
let file = "names.txt"
push("sort " + file)
call("run")
# alphabetical ascending
```

---

## numeric

Sort lines numerically.

> run "sort -n file.txt"

```markscript
let file = "scores.txt"
push("sort -n " + file)
call("run")
# 1, 2, 10, 100 (not 1, 10, 100, 2)
```

---

## reverse

Sort lines in reverse order.

> run "sort -r file.txt"

```markscript
let file = "dates.txt"
push("sort -r " + file)
call("run")
# Z to A, highest to lowest
```

---

## numeric_reverse

Sort numerically in descending order.

> run "sort -nr file.txt"

```markscript
let file = "prices.txt"
push("sort -nr " + file)
call("run")
# highest to lowest
```

---

## unique

Sort and remove duplicate lines.

> run "sort -u file.txt"

```markscript
let file = "tags.txt"
push("sort -u " + file)
call("run")
# sorted unique lines
```

---

## field

Sort by a specific field (column).

> run "sort -k 2 file.txt"

```markscript
let field = 2
let file = "data.tsv"
push("sort -k " + field + " " + file)
call("run")
# sorted by column 2
```

---

## field_numeric

Sort by a numeric field.

> run "sort -k 3 -n file.txt"

```markscript
let field = 3
let file = "stats.txt"
push("sort -k " + field + " -n " + file)
call("run")
# numerically sorted by column 3
```

---

## field_separator

Sort using a custom field delimiter.

> run "sort -t, -k 2 file.csv"

```markscript
let sep = ","
let field = 2
let file = "data.csv"
push("sort -t'" + sep + "' -k " + field + " " + file)
call("run")
# CSV sorted by column 2
```

---

## case_insensitive

Perform case-insensitive sort.

> run "sort -f file.txt"

```markscript
let file = "mixed_case.txt"
push("sort -f " + file)
call("run")
# A == a for sorting
```

---

## random

Shuffle lines randomly.

> run "sort -R file.txt"

```markscript
let file = "cards.txt"
push("sort -R " + file)
call("run")
# random order each time
```

---

## check_sorted

Check if a file is already sorted.

> run "sort -c file.txt"

```markscript
let file = "sorted_list.txt"
push("sort -c " + file)
call("run")
# silent if sorted, error with first disorder
```

---

## check_sorted_unique

Check if file is sorted and has no duplicates.

> run "sort -cu file.txt"

```markscript
let file = "unique_sorted.txt"
push("sort -cu " + file)
call("run")
# checks both ordering and uniqueness
```

---

## human_numeric

Sort with human-readable numbers (K, M, G).

> run "sort -h file.txt"

```markscript
let file = "sizes.txt"
push("sort -h " + file)
call("run")
# 100K, 1M, 2G sorted correctly
```

---

## stable_sort

Preserve original order of equal lines.

> run "sort -s file.txt"

```markscript
let file = "stable.txt"
push("sort -s " + file)
call("run")
# ties maintain input order
```

---

## month_sort

Sort by month names (Jan, Feb, ...).

> run "sort -M file.txt"

```markscript
let file = "months.txt"
push("sort -M " + file)
call("run")
# Jan, Feb, Mar... not alphabetical
```
