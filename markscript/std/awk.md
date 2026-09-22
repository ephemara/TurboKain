# Awk

MarkScript column processing --- filter, sum, format, transform structured text.
Wraps `awk` via the IVT for pattern-scanning and column operations.

---

## print_column

Print a specific column from delimited text.

> run "awk '{print $2}' file.txt"

```markscript
let col = 2
let file = "data.tsv"
push("awk '{print $" + col + "}' " + file)
call("run")
# second column printed
```

---

## print_columns

Print multiple columns with custom order.

> run "awk '{print $1, $3, $5}' file.txt"

```markscript
let file = "grades.csv"
push("awk '{print $1, $3, $5}' " + file)
call("run")
# columns 1, 3, 5 printed
```

---

## sum_column

Sum all values in a column.

> run "awk '{s+=$3} END{print s}' file.txt"

```markscript
let col = 3
let file = "sales.txt"
push("awk '{s+=$" + col + "} END{print s}' " + file)
call("run")
# total of column 3
```

---

## average_column

Calculate average of a column.

> run "awk '{s+=$2; c++} END{print s/c}' file.txt"

```markscript
let col = 2
let file = "scores.txt"
push("awk '{s+=$" + col + "; c++} END{print s/c}' " + file)
call("run")
# average of column 2
```

---

## filter

Print lines matching a condition on a column.

> run "awk '$3 > 100' file.txt"

```markscript
let col = 3
let threshold = 100
let file = "inventory.txt"
push("awk '$" + col + " > " + threshold + "' " + file)
call("run")
# lines where column 3 > 100
```

---

## filter_string

Print lines where a column matches a string.

> run "awk '$2 == \"active\"' file.txt"

```markscript
let col = 2
let value = "active"
let file = "users.csv"
push("awk '$" + col + " == \"" + value + "\"' " + file)
call("run")
```

---

## format

Print formatted output with printf.

> run "awk '{printf \"%-20s %5d\\n\", $1, $2}' file.txt"

```markscript
let file = "table.txt"
push("awk '{printf \"%-20s %5d\\n\", $1, $2}' " + file)
call("run")
# left-aligned name, right-aligned number
```

---

## begin_end

Run initialization before processing and summary after.

> run "awk 'BEGIN{print \"START\"} {print $0} END{print \"END\"}' file.txt"

```markscript
let file = "log.txt"
push("awk 'BEGIN{print \"=== BEGIN ===\"} {print NR\": \"$0} END{print \"=== END ===\"}' " + file)
call("run")
# wrapped output with header and footer
```

---

## field_separator

Specify a custom field separator.

> run "awk -F, '{print $1, $3}' file.csv"

```markscript
let sep = ","
let file = "data.csv"
push("awk -F'" + sep + "' '{print $1, $3}' " + file)
call("run")
# CSV parsed by comma
```

---

## header_row

Skip a header row, then process data.

> run "awk 'NR>1{s+=$2} END{print s}' file.txt"

```markscript
let file = "data_with_header.csv"
push("awk 'NR>1{s+=$2} END{print s}' " + file)
call("run")
# skips line 1, sums column 2
```

---

## line_count

Count lines matching a pattern.

> run "awk '/pattern/{c++} END{print c}' file.txt"

```markscript
let pattern = "ERROR"
let file = "system.log"
push("awk '/" + pattern + "/{c++} END{print c}' " + file)
call("run")
# count of ERROR lines
```
