# Array

Markscript array operations --- creation, access, iteration.
Data flows through the VM operand stack and variable store.

---

## create

Create a new array by pushing values to the stack.

```markscript
let a = 1
let b = 2
let c = 3
# values are on the operand stack
```

---

## access

Access elements by pushing them to the stack.

```markscript
let first = 10
let second = 20
let third = 30
# each variable holds one element
```

---

## length

Count elements in an array.

```markscript
let count = 3
# track count manually
```

---

## sum

Sum all elements in an array.

```markscript
let a = 5
let b = 10
let c = 15
let sum = a + b + c
# sum = 30
```

---

## map

Apply an operation to each element (add 1 to each).

```markscript
let x = 1
let y = 2
let z = 3
x = x + 1
y = y + 1
z = z + 1
# x=2, y=3, z=4
```

---

## filter

Keep only elements matching a condition (positive numbers).

```markscript
let a = -3
let b = 5
let c = -1
let d = 8
# keep b and d, discard a and c
```

---

## reduce

Combine all elements into a single value (product).

```markscript
let a = 2
let b = 3
let c = 4
let product = a * b * c
# product = 24
```

---

## reverse

Reverse element order (swap positions).

```markscript
let first = 1
let last = 9
let temp = first
# first = last
# last = temp
```

---

## find

Find the first element matching a condition.

```markscript
let a = 0
let b = 0
let c = 42
let found = c
# found = 42
```

---

## slice

Extract a sub-range of elements.

```markscript
let v0 = 10
let v1 = 20
let v2 = 30
let v3 = 40
let v4 = 50
# slice 1..3 = [20, 30, 40]
```
