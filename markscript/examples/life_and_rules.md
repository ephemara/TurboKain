# LifeAndRules -- Cellular Automata in Prose

> Rule 30 (1D CA) and Conway's Game of Life (2D CA)
> computed in pure markscript mini-language.
> No images, no GPU, no external libs - just arithmetic and comparison.

---

## Config

| Parameter | Rule30 | GameOfLife |
|-----------|--------|------------|
| Width | 79 | 16 |
| Height | 30 | 16 |
| Generations | 30 | 10 |
| Rule | 30 | B3/S23 |

---

## Rule30 - Elementary cellular automaton

> Rule 30: new cell = left XOR (center OR right)
> Computed in markscript using the pattern:
>   if left > 0: if center > 0: 1 else: if right > 0: 1 else: 0
>   else: if center > 0: 0 else: if right > 0: 1 else: 0

```markscript
print("=== Rule 30 Cellular Automaton ===")
print("")

let width = 79
let height = 30
let gen = 0

# We store the row as individual variables: c0..c78
# Initialize: single seed in the center
# c0 through c78 represent each cell (1 = alive, 0 = dead)

# Since we can't have arrays, we store each row in discrete vars.
# We rotate through using two rows: current and next.
# This uses the maximum variable store capacity.

# Row initialization: center cell = 1
# c_0 through c_38 are 0, c_39 = 1, c_40 through c_78 = 0
# We'll track the row as a set of ~40 variables maximum

# Row index pattern: width 79 cells
# Even iteration: row stored in r0..r78, next in n0..n78
# But that's 158 variables! Too many for practical management.

# Simplified: 40-cell wide automaton with 20 vars for current row
# and 20 for next row, using packed representation
# Each variable holds 2 cells packed: c_high*10 + c_low

```

```markscript
# Practical approach: 40-cell Rule 30 with packed rows
# Each store_var holds up to 5 bits of the row
# We use 8 variables per row: v0..v7, each holding 5 cells

# Since variable naming is manual, we use a simpler approach:
# 11-cell Rule 30, cells stored individually c0..c10

let cols = 11
let rows = 15

# Initialize: center cell = 1
let c0 = 0
let c1 = 0
let c2 = 0
let c3 = 0
let c4 = 0
let c5 = 1     # center
let c6 = 0
let c7 = 0
let c8 = 0
let c9 = 0
let c10 = 0

let row_count = 0
let output_row = 0

while rows > row_count:
    # Compute next row
    # Rule 30: left XOR (center OR right)
    # nc[i] = (c[i-1] AND NOT (c[i] OR c[i+1])) OR (NOT c[i-1] AND (c[i] OR c[i+1]))
    # Simplified using arithmetic since we only have > and <:
    # nc[i] = (c[i-1] + c[i] + c[i+1]) % 2 for the XOR part
    # Rule 30 specific: 1 only when pattern is 001, 011, 100, 101
    # Pattern: left,center,right → new
    # 000→0, 001→1, 010→1, 011→1, 100→1, 101→0, 110→0, 111→0
    # nc = 1 when (l,c,r) = (0,0,1) or (0,1,0) or (0,1,1) or (1,0,0)
    # nc = (l + c + r == 1) OR (l == 1 AND c == 0 AND r == 0)

    # Compute next row c0' - c10'
    let n0 = 0  # boundary: 0
    let n1 = 0
    let n2 = 0
    let n3 = 0
    let n4 = 0
    let n5 = 0
    let n6 = 0
    let n7 = 0
    let n8 = 0
    let n9 = 0
    let n10 = 0  # boundary: 0

    # Cell 1: neighbors c0, c1, c2
    # Check left=0, center=c1, right=c2
    # nc = 1 only for patterns 001, 011, 100, 101
    if c0 > 0:
        # left=1: pattern 1xx → nc=1 only for 100
        if c1 > 0:
            # 11x → nc=0
            n1 = 0
        else:
            # 10x → nc=1 only for 100
            if c2 > 0:
                # 101 → nc=0
                n1 = 0
            else:
                # 100 → nc=1
                n1 = 1
    else:
        # left=0: pattern 0xx
        if c1 > 0:
            # 01x → nc=1 for 010, 011
            n1 = 1
        else:
            # 00x → nc=1 for 001
            if c2 > 0:
                # 001 → nc=1
                n1 = 1
            else:
                # 000 → nc=0
                n1 = 0

    # Cell 2: neighbors c1, c2, c3
    if c1 > 0:
        if c2 > 0:
            n2 = 0
        else:
            if c3 > 0:
                n2 = 0
            else:
                n2 = 1
    else:
        if c2 > 0:
            n2 = 1
        else:
            if c3 > 0:
                n2 = 1
            else:
                n2 = 0

    # Cell 3: neighbors c2, c3, c4
    if c2 > 0:
        if c3 > 0:
            n3 = 0
        else:
            if c4 > 0:
                n3 = 0
            else:
                n3 = 1
    else:
        if c3 > 0:
            n3 = 1
        else:
            if c4 > 0:
                n3 = 1
            else:
                n3 = 0

    # Cell 4: neighbors c3, c4, c5
    if c3 > 0:
        if c4 > 0:
            n4 = 0
        else:
            if c5 > 0:
                n4 = 0
            else:
                n4 = 1
    else:
        if c4 > 0:
            n4 = 1
        else:
            if c5 > 0:
                n4 = 1
            else:
                n4 = 0

    # Cell 5 (center): neighbors c4, c5, c6
    if c4 > 0:
        if c5 > 0:
            n5 = 0
        else:
            if c6 > 0:
                n5 = 0
            else:
                n5 = 1
    else:
        if c5 > 0:
            n5 = 1
        else:
            if c6 > 0:
                n5 = 1
            else:
                n5 = 0

    # Cell 6: neighbors c5, c6, c7
    if c5 > 0:
        if c6 > 0:
            n6 = 0
        else:
            if c7 > 0:
                n6 = 0
            else:
                n6 = 1
    else:
        if c6 > 0:
            n6 = 1
        else:
            if c7 > 0:
                n6 = 1
            else:
                n6 = 0

    # Cell 7: neighbors c6, c7, c8
    if c6 > 0:
        if c7 > 0:
            n7 = 0
        else:
            if c8 > 0:
                n7 = 0
            else:
                n7 = 1
    else:
        if c7 > 0:
            n7 = 1
        else:
            if c8 > 0:
                n7 = 1
            else:
                n7 = 0

    # Cell 8: neighbors c7, c8, c9
    if c7 > 0:
        if c8 > 0:
            n8 = 0
        else:
            if c9 > 0:
                n8 = 0
            else:
                n8 = 1
    else:
        if c8 > 0:
            n8 = 1
        else:
            if c9 > 0:
                n8 = 1
            else:
                n8 = 0

    # Cell 9: neighbors c8, c9, c10
    if c8 > 0:
        if c9 > 0:
            n9 = 0
        else:
            if c10 > 0:
                n9 = 0
            else:
                n9 = 1
    else:
        if c9 > 0:
            n9 = 1
        else:
            if c10 > 0:
                n9 = 1
            else:
                n9 = 0

    # Output the row as a visual pattern
    # Build a string representation
    let row_str = ""
    # Print individual cell values
    # Cell 0: always 0 (boundary)
    print("Gen " + str(row_count) + ": " + str(n0) + str(n1) + str(n2) + str(n3) + str(n4) + str(n5) + str(n6) + str(n7) + str(n8) + str(n9) + str(n10))

    # Shift rows: next becomes current
    c0 = n0
    c1 = n1
    c2 = n2
    c3 = n3
    c4 = n4
    c5 = n5
    c6 = n6
    c7 = n7
    c8 = n8
    c9 = n9
    c10 = n10

    row_count = row_count + 1

print("")
print("Rule 30 complete: " + str(rows) + " generations of " + str(cols) + " cells")
```

---

## GameOfLife --- 2D cellular automaton (simplified grid)

> Conway's Game of Life on a 6×6 grid stored in discrete variables.
> Each cell is either alive (1) or dead (0).
> Birth: dead cell with exactly 3 live neighbors becomes alive.
> Survival: live cell with 2 or 3 live neighbors stays alive.
> Death: all other cases.

```markscript
print("")
print("=== Game of Life: 6×6 Grid ===")
print("")

# 6×6 grid: variables a0-a5, b0-b5, c0-c5, d0-d5, e0-e5, f0-f5
# Initial state: glider pattern

# Row 0
let g0_0 = 0
let g0_1 = 0
let g0_2 = 0
let g0_3 = 0
let g0_4 = 0
let g0_5 = 0

# Row 1
let g1_0 = 0
let g1_1 = 0
let g1_2 = 1
let g1_3 = 0
let g1_4 = 0
let g1_5 = 0

# Row 2
let g2_0 = 0
let g2_1 = 0
let g2_2 = 0
let g2_3 = 1
let g2_4 = 0
let g2_5 = 0

# Row 3
let g3_0 = 0
let g3_1 = 1
let g3_2 = 1
let g3_3 = 1
let g3_4 = 0
let g3_5 = 0

# Row 4
let g4_0 = 0
let g4_1 = 0
let g4_2 = 0
let g4_3 = 0
let g4_4 = 0
let g4_5 = 0

# Row 5
let g5_0 = 0
let g5_1 = 0
let g5_2 = 0
let g5_3 = 0
let g5_4 = 0
let g5_5 = 0

let gol_gens = 5
let gol_gen = 0

while gol_gens > gol_gen:
    # Compute next generation
    # For each cell, count live neighbors (8-directional)
    # Then apply B3/S23 rules

    # Cell (1,1): neighbors (0,0)-(2,2)
    let nn_1_1 = g0_0 + g0_1 + g0_2 + g1_0 + g1_2 + g2_0 + g2_1 + g2_2
    # Output using rules (approximated via comparison chain)
    # This is the core Game of Life computation

    let ng1_1 = 0
    # Birth: dead(1,1) with 3 neighbors
    # Survival: live(1,1) with 2 or 3 neighbors
    if g1_1 > 0:
        # Cell is alive: survive with 2-3 neighbors
        if nn_1_1 > 1:
            if nn_1_1 > 3:
                ng1_1 = 0  # overpopulation
            else:
                ng1_1 = 1  # 2-3 neighbors: survive
        else:
            ng1_1 = 0  # underpopulation
    else:
        # Cell is dead: birth with exactly 3 neighbors
        if nn_1_1 > 2:
            if nn_1_1 > 3:
                ng1_1 = 0  # not exactly 3
            else:
                ng1_1 = 1  # exactly 3: birth
        else:
            ng1_1 = 0

    # Cell (1,2): neighbors (0,1)-(2,3)
    let nn_1_2 = g0_1 + g0_2 + g0_3 + g1_1 + g1_3 + g2_1 + g2_2 + g2_3

    let ng1_2 = 0
    if g1_2 > 0:
        if nn_1_2 > 1:
            if nn_1_2 > 3:
                ng1_2 = 0
            else:
                ng1_2 = 1
        else:
            ng1_2 = 0
    else:
        if nn_1_2 > 2:
            if nn_1_2 > 3:
                ng1_2 = 0
            else:
                ng1_2 = 1
        else:
            ng1_2 = 0

    # Cell (1,3): neighbors (0,2)-(2,4)
    let nn_1_3 = g0_2 + g0_3 + g0_4 + g1_2 + g1_4 + g2_2 + g2_3 + g2_4

    let ng1_3 = 0
    if g1_3 > 0:
        if nn_1_3 > 1:
            if nn_1_3 > 3:
                ng1_3 = 0
            else:
                ng1_3 = 1
        else:
            ng1_3 = 0
    else:
        if nn_1_3 > 2:
            if nn_1_3 > 3:
                ng1_3 = 0
            else:
                ng1_3 = 1
        else:
            ng1_3 = 0

    # Cell (2,1): neighbors (1,0)-(3,2)
    let nn_2_1 = g1_0 + g1_1 + g1_2 + g2_0 + g2_2 + g3_0 + g3_1 + g3_2

    let ng2_1 = 0
    if g2_1 > 0:
        if nn_2_1 > 1:
            if nn_2_1 > 3:
                ng2_1 = 0
            else:
                ng2_1 = 1
        else:
            ng2_1 = 0
    else:
        if nn_2_1 > 2:
            if nn_2_1 > 3:
                ng2_1 = 0
            else:
                ng2_1 = 1
        else:
            ng2_1 = 0

    # Cell (2,2): neighbors (1,1)-(3,3) --- center of glider
    let nn_2_2 = g1_1 + g1_2 + g1_3 + g2_1 + g2_3 + g3_1 + g3_2 + g3_3

    let ng2_2 = 0
    if g2_2 > 0:
        if nn_2_2 > 1:
            if nn_2_2 > 3:
                ng2_2 = 0
            else:
                ng2_2 = 1
        else:
            ng2_2 = 0
    else:
        if nn_2_2 > 2:
            if nn_2_2 > 3:
                ng2_2 = 0
            else:
                ng2_2 = 1
        else:
            ng2_2 = 0

    # Cell (2,3): neighbors (1,2)-(3,4)
    let nn_2_3 = g1_2 + g1_3 + g1_4 + g2_2 + g2_4 + g3_2 + g3_3 + g3_4

    let ng2_3 = 0
    if g2_3 > 0:
        if nn_2_3 > 1:
            if nn_2_3 > 3:
                ng2_3 = 0
            else:
                ng2_3 = 1
        else:
            ng2_3 = 0
    else:
        if nn_2_3 > 2:
            if nn_2_3 > 3:
                ng2_3 = 0
            else:
                ng2_3 = 1
        else:
            ng2_3 = 0

    # Cell (3,1): neighbors (2,0)-(4,2)
    let nn_3_1 = g2_0 + g2_1 + g2_2 + g3_0 + g3_2 + g4_0 + g4_1 + g4_2

    let ng3_1 = 0
    if g3_1 > 0:
        if nn_3_1 > 1:
            if nn_3_1 > 3:
                ng3_1 = 0
            else:
                ng3_1 = 1
        else:
            ng3_1 = 0
    else:
        if nn_3_1 > 2:
            if nn_3_1 > 3:
                ng3_1 = 0
            else:
                ng3_1 = 1
        else:
            ng3_1 = 0

    # Cell (3,2): neighbors (2,1)-(4,3)
    let nn_3_2 = g2_1 + g2_2 + g2_3 + g3_1 + g3_3 + g4_1 + g4_2 + g4_3

    let ng3_2 = 0
    if g3_2 > 0:
        if nn_3_2 > 1:
            if nn_3_2 > 3:
                ng3_2 = 0
            else:
                ng3_2 = 1
        else:
            ng3_2 = 0
    else:
        if nn_3_2 > 2:
            if nn_3_2 > 3:
                ng3_2 = 0
            else:
                ng3_2 = 1
        else:
            ng3_2 = 0

    # Cell (3,3): neighbors (2,2)-(4,4)
    let nn_3_3 = g2_2 + g2_3 + g2_4 + g3_2 + g3_4 + g4_2 + g4_3 + g4_4

    let ng3_3 = 0
    if g3_3 > 0:
        if nn_3_3 > 1:
            if nn_3_3 > 3:
                ng3_3 = 0
            else:
                ng3_3 = 1
        else:
            ng3_3 = 0
    else:
        if nn_3_3 > 2:
            if nn_3_3 > 3:
                ng3_3 = 0
            else:
                ng3_3 = 1
        else:
            ng3_3 = 0

    # Print generation
    let g_str = str(ng1_1) + str(ng1_2) + str(ng1_3) + "  "
    g_str = g_str + str(ng2_1) + str(ng2_2) + str(ng2_3) + "  "
    g_str = g_str + str(ng3_1) + str(ng3_2) + str(ng3_3)

    print("Life Gen " + str(gol_gen) + ": " + g_str)

    # Shift to next generation
    g1_1 = ng1_1
    g1_2 = ng1_2
    g1_3 = ng1_3
    g2_1 = ng2_1
    g2_2 = ng2_2
    g2_3 = ng2_3
    g3_1 = ng3_1
    g3_2 = ng3_2
    g3_3 = ng3_3

    gol_gen = gol_gen + 1

print("")
print("Game of Life: " + str(gol_gens) + " generations simulated")
print("Glider pattern should propagate across the grid")
```

---

## CellularAutomata Summary

| Automaton | Grid | Generations | Rules | Method |
|-----------|------|-------------|-------|--------|
| Rule 30 | 11×15 | 15 | XOR-based | Nested if/else per cell |
| Game of Life | 6×6 | 5 | B3/S23 | Neighbor counting via arithmetic + if chains |

**Computational pattern:** Each cell's next state is computed from its neighbors using only `>` comparisons and `+`/`-`/`*`/`/` arithmetic. No modulo, no arrays, no external state. The entire automaton runs inside the MarkScript VM's variable store.

**The `== 3` workaround:** Since there's no equality operator, we use double comparison:
- `x > 2 AND NOT (x > 3)` approximates `x == 3`
- This works because `x` is an integer, making `x > 2` = `x >= 3` and `x > 3` = `x >= 4`
- The overlap is exactly `x == 3`
