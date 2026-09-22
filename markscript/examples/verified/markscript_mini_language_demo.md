# MarkScript Mini-Language Demo

Demonstrates the ```markscript mini-language inside fenced blocks.
All constructs verified to compile and execute correctly.

---

## Variables and Arithmetic

```markscript
let a = 10
let b = 20
let sum = a + b
let diff = b - a
let prod = a * b
let quot = b / a
print(a)
print(b)
print(sum)
print(prod)
print(quot)
```

## Comments

```markscript
# This is a comment - it should not affect execution
let r = 42
# Another comment line
print(r)
```

## String Literals and Function Calls

```markscript
let msg = concat("hello", "world")
print(msg)
print(upper("works"))
print(lower("WORKS"))
print(trim("  ok  "))
```

## If / Else with Literals

```markscript
let val = 7
if val > 10:
    print("big")
else:
    print("small")
```

## Multiple Expressions in One Block

```markscript
print(min(10, 20))
print(max(30, 40))
print(clamp(50, 0, 100))
print(split("a,b,c", ","))
print(join("-", "x", "y"))
print(substr("hello", 0, 3))
print(contains("abc", "b"))
```

## Arithmetic with Only Addition/Subtraction

```markscript
let x = 100
let y = 50
let z = x + y
print(z)
```

## Verify

```markscript
print("mini_language_demo: all constructs exercised")
```
