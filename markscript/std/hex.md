# Hex

Hexadecimal encoding, decoding, and binary dump utilities.

## encode

Convert a string or byte sequence to a hexadecimal string.

> print "Hex encoded"

```markscript
let text = "Hello"

let hex_str = hex.encode(text)
# "48656c6c6f"

> assert hex_str "48656c6c6f"
```

## decode

Convert a hexadecimal string back to the original text.

> print "Hex decoded"

```markscript
let hex_str = "48656c6c6f"

let decoded = hex.decode(hex_str)
# "Hello"

> assert decoded "Hello"
```

## dump

Produce a hex dump (hexadecimal + ASCII representation) similar to `xxd` or `hexdump -C`.

> run "python -c \"... hexdump ...\""

```markscript
let data = "Hello World! This is a test."

let dump = hex.dump(data)
# 00000000: 4865 6c6c 6f20 576f 726c 6421 2054 6869  Hello World! Thi
# 00000010: 7320 6973 2061 2074 6573 742e            s is a test.

> print dump
```

## from_hex

Alias for `hex.decode`. Included for symmetry and API consistency.

> print "From hex decoded"

```markscript
let h = "ff00aabb"

let bytes = hex.from_hex(h)
> assert hex.encode(bytes) h
```

## to_hex

Alias for `hex.encode`. Included for symmetry and API consistency.

> print "To hex encoded"

```markscript
let bytes = "\xff\x00\xaa\xbb"

let h = hex.to_hex(bytes)
# "ff00aabb"

> assert h "ff00aabb"
```

## color_hex

Convert between 3-byte RGB and 6-digit hex color strings.

> assert converted expected

```markscript
let rgb = {"r": 255, "g": 128, "b": 0}

let hex_color = hex.color_hex(rgb)
# "FF8000"

> assert hex_color "FF8000"

let back = hex.parse_color("FF8000")
> assert back["r"] 255
> assert back["g"] 128
```

## compare

Lexicographically compare two hex strings (case-insensitive). Returns -1, 0, or 1.

> assert result expected

```markscript
let a = "ff"
let b = "aa"

let cmp = hex.compare(a, b)
> assert cmp 1    # ff > aa

> assert hex.compare("ab", "ab") 0
> assert hex.compare("01", "02") -1
```
