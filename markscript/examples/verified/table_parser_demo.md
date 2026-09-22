# Table Parser Demo

Demonstrates the table/matrix parser with pipe tables,
header rows, separator rows, data rows, and type inference.

---

## Simple Pipe Table

A basic table with header, separator, and data rows:

| Name | Count | Active |
|------|-------|--------|
| Alpha | 10 | true |
| Beta | 20 | false |
| Gamma | 30 | true |

---

## Mixed Types (int, float, string)

The parser infers column types from cell values.
Floats widen to ints; strings dominate.

| Item | Price | Weight | Category |
|------|-------|--------|----------|
| Widget | 9.99 | 150 | hardware |
| Gizmo | 24.50 | 75 | hardware |
| Service | 0 | 0 | software |
| Plan | 49.99 | 0 | subscription |

---

## Numeric Table

All integer columns --- useful for config matrices:

| X | Y | Z | W |
|---|---|---|---|
| 1 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 |
| 0 | 0 | 1 | 0 |
| 0 | 0 | 0 | 1 |

---

## Single Row Table

| Key | Value |
|-----|-------|
| port | 8080 |

---

## Wide Table

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |

---

## Verify

```markscript
print("table_parser_demo: table parsing exercised")
```
