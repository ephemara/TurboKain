# String Operations

Exercise every registered string handler via markscript function calls.

```markscript
print(concat("hello", " ", "world"))
print(split("apple,banana,grape", ","))
print(join(" | ", "x", "y", "z"))
print(substr("hello world", 0, 5))
print(replace("the cat sat", "cat", "dog"))
print(upper("hello"))
print(lower("WORLD"))
print(trim("  padded  "))
print(contains("hello world", "world"))
```

## verify

```markscript
print("string_ops: all 9 string handlers executed")
```
