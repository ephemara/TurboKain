# Cut

MarkScript column extraction -- select bytes, characters, or fields from each line.
Wraps `cut` via the IVT for text slicing operations.

---

## bytes

Extract specific byte positions from each line.

> run "cut -b 1-10 file.txt"

```markscript
let range = "1-10"
let file = "fixed_width.txt"
push("cut -b " + range + " " + file)
call("run")
# bytes 1 through 10
```

---

## byte_list

Extract specific individual byte positions.

> run "cut -b 1,3,5 file.txt"

```markscript
let positions = "1,3,5"
let file = "bytes.txt"
push("cut -b " + positions + " " + file)
call("run")
# bytes 1, 3, and 5
```

---

## byte_range_open

Extract from a position to end of line.

> run "cut -b 5- file.txt"

```markscript
let start = "5-"
let file = "skip_first.txt"
push("cut -b " + start + " " + file)
call("run")
# byte 5 to end of line
```

---

## chars

Extract specific character positions.

> run "cut -c 1-10 file.txt"

```markscript
let range = "1-10"
let file = "text.txt"
push("cut -c " + range + " " + file)
call("run")
# characters 1 through 10
```

---

## char_list

Extract specific character positions.

> run "cut -c 2,4,6 file.txt"

```markscript
let positions = "2,4,6"
let file = "every_other.txt"
push("cut -c " + positions + " " + file)
call("run")
# every other character
```

---

## fields

Extract specific fields (columns).

> run "cut -f 2 file.txt"

```markscript
let field = 2
let file = "columns.txt"
push("cut -f " + field + " " + file)
call("run")
# second field on each line
```

---

## field_range

Extract a range of fields.

> run "cut -f 2-5 file.txt"

```markscript
let range = "2-5"
let file = "data.txt"
push("cut -f " + range + " " + file)
call("run")
# fields 2 through 5
```

---

## field_list

Extract specific fields.

> run "cut -f 1,3,5 file.txt"

```markscript
let fields = "1,3,5"
let file = "spreadsheet.tsv"
push("cut -f " + fields + " " + file)
call("run")
# fields 1, 3, and 5
```

---

## delimiter

Use a custom delimiter instead of tab.

> run "cut -d',' -f 2 file.csv"

```markscript
let delim = ","
let field = 2
let file = "data.csv"
push("cut -d'" + delim + "' -f " + field + " " + file)
call("run")
# comma-separated files
```

---

## complement

Select everything EXCEPT the specified fields.

> run "cut --complement -f 2 file.txt"

```markscript
let exclude = 2
let file = "table.txt"
push("cut --complement -f " + exclude + " " + file)
call("run")
# all fields except field 2
```

---

## output_delimiter

Specify a custom output delimiter between fields.

> run "cut -d':' -f 1,3 --output-delimiter=' ' file.txt"

```markscript
let in_delim = ":"
let out_delim = " "
let fields = "1,3"
let file = "passwd.txt"
push("cut -d'" + in_delim + "' -f " + fields + " --output-delimiter='" + out_delim + "' " + file)
call("run")
# fields joined with space
```

---

## only_delimited

Only output lines that contain the delimiter.

> run "cut -d',' -f 2 -s file.csv"

```markscript
let delim = ","
let field = 2
let file = "messy.csv"
push("cut -d'" + delim + "' -f " + field + " -s " + file)
call("run")
# skips lines without delimiter
```
