# Fuzz Corpus

> Adversarial markdown: hostile structures that must NEVER crash the
> lexer, parser, or VM. Every section must compile; exec behavior is
> recorded in REPORT.md. A crash here is a fuzzer-grade find.

## fence_inside_quote

> ```
> print "this is fenced text inside a quote, not an intent"
> ```

> print "fence-in-quote survived"

## quote_inside_fence

```markscript
let fq = 1
```

```text
> this looks like an intent but lives inside a fence
> print "must never dispatch"
```

> print "quote-in-fence survived"

## table_inside_fence

```text
| not | a |
|---|---|
| real | table |
```

> print "table-in-fence survived"

## unclosed_everything

```markscript
let unclosed = 999

> print "unclosed fence above must not eat the file"

## hash_midline_and_gt_midline

Value # not a header and 5 > 3 not a quote, a > b > c chains.

## empty_file_sections

##

###

> print "empty sections survived"

## pathological_nesting

- l1
  - l2
    - l3
      - l4
        - l5
          - l6
            - l7
              - l8
                - l9
                  - l10
                    - l11
                      - l12

1. n1
   1. n2
      1. n3
         1. n4
            1. n5

## link_maze

[a](b) [c](d(e)) [empty]() [](empty) [nested [brackets] here](http://x.y/z)
![img](a.png) ![img2](b.png "titled")

## code_span_storm

`one` ``two`` ```three``` `unclosed span
normal text `closed` more text `a+b*c/d_e-f`

## thematic_breaks

---
***
___
- - -
* * *

## html_and_frontmatter

<div class="x">raw html block</div>
<script>alert("not js")</script>
---
title: fake frontmatter
count: 3
---

## deep_headers_then_code

###### h6 direct to code

```markscript
let fuzz_proof = 7 * 6
```

> assert fuzz_proof 42
> print "FUZZ CORPUS DONE"
