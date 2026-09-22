# Lexer Torture

> Every token type, every nesting level, every adversarial structure.
> Spec claim under test: markdown has NO syntax errors — this file must
> COMPILE no matter what. Execution behavior is recorded, not assumed.

## h1_top

### h3_skipped_level

###### h6_bottom

####### h7_beyond_spec

# EmptyHeadersFollow
##
###
# TrailingHash #
#  Spaced  Out  #

## symbols_everywhere

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |

| ragged | row |
|---|---|
| one | two | three | four |
| single |

|  |

| empty |  | cells |
|---|---|---|
|  | x |  |

- dash item
* star item
1. numbered one
2. numbered two
   - nested dash
     1. deep numbered
        - deeper still

[link text](https://example.com/path?q=1&r=2)
[parens](https://example.com/a_(b)_c)
![image alt](img.png)

*italic* **bold** ***both*** `code span` **bold with *nested italic* inside**

> print "lexer torture alive"

## unicode_soup

日本語テスト 中文測試 한국어 테스트
Emoji storm: 🔥🚀💀🎯🧬⚡️🌊🌀
Math symbols: ∑∏∫√∞≠≤≥ ±×÷ ∀∃∈∉
RTL: مرحبا עברית
Zalgo-ish: c o m b i n i n g ~ ~ ~

> print "unicode survived"

## fence_games

```markscript
let fence_a = 1
print(fence_a)
```

```unknownlangtag
this is stored by language tag, not executed
```

```
no tag at all
```

```markscript
let empty_above = 0
```

> print "fences survived"

## quote_games

> print "level one"

>> print "level two nested"

> > print "spaced nested"

>
> print "after empty quote"

Not a quote > mid-line greater-than 5 > 3.
#Not a header, no space after hash.

## giant_line

```markscript
let giant = 0
let gi = 0
while gi < 2000:
    giant = giant + 1
    gi = gi + 1
```

> assert giant 2000

## routine_count_check

```markscript
let lexer_proof = 40 + 2
```

> assert lexer_proof 42
> print "LEXER TORTURE DONE"
