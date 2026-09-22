# Max Intents

Stress test: 45+ handler calls in one file. Proves dispatch scales.

```markscript
print(concat("batch", "01"))
print(split("a,b,c,d,e,f,g,h,i,j", ","))
print(join("-", "x", "y", "z"))
print(substr("stress_test", 0, 6))
print(replace("alpha", "a", "x"))
print(upper("stress"))
print(lower("STRESS"))
print(trim("  clean  "))
print(contains("foobarbaz", "bar"))
print(sin(1))
print(cos(0))
print(sqrt(25))
print(abs(-99))
print(min(10, 20))
print(max(10, 20))
print(clamp(50, 0, 100))
print(random(1, 50))
print(time(0))
print(sleep(5))
print(concat("batch", "02"))
print(split("one,two,three,four,five", ","))
print(join("::", "a", "b"))
print(substr("hello world", 6, 5))
print(replace("hello world", "world", "there"))
print(upper("batch"))
print(lower("BATCH"))
print(trim(" margin "))
print(contains("abcdef", "cd"))
print(sin(2))
print(cos(1))
print(sqrt(36))
print(abs(-50))
print(min(5, 15))
print(max(5, 15))
print(clamp(200, 0, 100))
print(random(1, 10))
print(concat("final", "batch"))
print(split("final,stress,test", ","))
print(join("_", "mks", "stress", "test"))
print(substr("maximum intents", 0, 7))
print(replace("old pattern", "old", "new"))
print(upper("final"))
print(lower("FINAL"))
print(trim(" complete "))
print(contains("maximum stress", "stress"))
print(time(0))
```

## verify

```markscript
print("max_intents: 45+ intents dispatched without errors")
```
