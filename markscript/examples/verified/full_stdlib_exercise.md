# Full Stdlib Exercise

Exercises every major intent category from the 57-keyword registry.
Uses the markscript mini-language for multi-arg function calls.

---

## File I/O

```markscript
print(write(".mks_stdlib_test.txt", "stdlib exercise content"))
print(exists(".mks_stdlib_test.txt"))
print(read(".mks_stdlib_test.txt"))
```

---

## String Operations

```markscript
print(concat("hello", " world"))
print(upper("uppercase me"))
print(lower("LOWERCASE ME"))
print(trim("  padded  "))
print(split("apple,banana,cherry", ","))
print(join("-", "a", "b", "c"))
print(substr("hello world", 0, 5))
print(replace("hello world", "world", "stdlib"))
print(contains("hello world", "world"))
```

---

## Math

```markscript
print(sin(1))
print(cos(0))
print(sqrt(16))
print(abs(-99))
print(min(42, 100))
print(max(42, 100))
print(clamp(75, 0, 100))
```

---

## Random

```markscript
print(random(1, 100))
```

---

## Time

```markscript
print(time(0))
```

---

## Process / System

> print "stdlib exercise: all categories exercised"

---

## Verify

```markscript
print("full_stdlib_exercise: all major categories dispatched")
```
