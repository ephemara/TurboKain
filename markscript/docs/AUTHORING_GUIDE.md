# MarkScript Authoring Guide

> Write executable documentation. Every valid `.md` file is a valid MarkScript program.

---

## The Markdown → Semantics Mapping

| Markdown | Becomes | Bytecode |
|----------|---------|----------|
| `# Title` | **Domain** --- named scope | `OP_ENTER_DOMAIN` |
| `## Title` | **Routine** --- executable block | `OP_ROUTINE_HEADER` |
| `> phrase` | **Intent** - natural-language command | `OP_PUSH_PARAM` + `OP_EXECUTE_CALL` |
| `\| a \| b \|` | **Matrix** --- typed data table | `OP_PUSH_MATRIX` |
| `` ```lang `` | **Fenced code** -- stored by lang+content | `OP_FENCED_CODE` |
| Plain text | Documentation - silently skipped | None |

---

## Domains (`#`)

Top-level headings are **domains** - the top-level namespace.

```markdown
# PhysicsSim
# DataPipeline
# GameConfig
```

A file should have at least one domain. Domains contain routines.

## Routines (`##`)

Second-level headings are **routines** - executable blocks containing intents, tables, and code.

```markdown
## compute_forces
## render_frame
## validate_output
```

Use descriptive, intent-friendly names - they become the context in error messages.

## Intents (`>`)

Blockquotes are the execution unit. Each `>` line dispatches through the IVT:

```markdown
> print "hello"
> assert result 42
> read file "config.json"
> write file "output.txt" "done"
```

**Multi-word phrases** are hashed and matched as a single intent:

```markdown
> apply gravity
> resolve collisions
> present swapchain
```

The IVT matches by hash of the entire phrase.

**Arguments** are whitespace-delimited words after the intent phrase. Quoted strings count as one argument:

```markdown
> write file "C:/path/with spaces/config.json" "content"
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^
                arg 1                            arg 2
```

## Data Tables (`|`)

Tables become contiguous bytecode matrices - zero-copy, zero-indirection data:

```markdown
| Object | Mass | Velocity |
|--------|------|----------|
| Player | 80   | 0        |
| Crate  | 200  | 12       |
```

**Rules:**
- First row before `|---|` separator is the **header** (column names)
- Separator rows (`|----|`, `|:---|---:|`) are skipped
- Empty rows within tables are ignored
- Mixing types: if a column has `Int` and `Float`, column becomes `Float`. Any `String` makes the whole column `String`

**Access at runtime:** Tables are stored in `VM.data_table` keyed by handle ID. The handle ID is the ordinal position (0, 1, 2...).

## Fenced Code Blocks (`` ``` ``)

Extract code by language tag:

````markdown
```kain
fn physics_step(dt: Float) -> Float:
    return dt * 0.016
```

```c
void isr_handler() {
    PORTB |= (1 << 3);
}
```

```python
import numpy as np
```

```markscript
let x = 1
while x <= 10:
    print(x)
    x = x + 1
```
````

The Markscript mini-language inside ` ```markscript ` blocks supports:

| Feature | Syntax |
|---------|--------|
| Variables | `let name = value` |
| Assignment | `name = value` |
| Arithmetic | `+`, `-`, `*`, `/`, `%` |
| While loops | `while condition:` |
| If/elif/else | `if cond:` / `elif cond:` / `else:` |
| Print | `print(value)` |
| String conversion | `str(value)` |
| Length | `len(container)` |
| Comparison | `==`, `!=`, `<`, `>`, `<=`, `>=` |

## Multi-File Projects (`@import`)

Compose larger programs from modules:

```markdown
@import "config/settings.md"
@import "../common/physics.md"
@import "game/ai_behaviors.md"
```

Or import Kain modules directly:

```markdown
> import kain "src/engine/physics.kn"
```

Then call imported functions as intents:

```markdown
> call physics.apply_gravity bodies timestep
```

## Documentation

Everything NOT structural is documentation. Write freely:

```markdown
# PhysicsSim

This domain simulates rigid body physics using a fixed timestep.
Gravity is applied as a constant downward acceleration.

## compute_forces

The following table defines the simulation bodies.
Each row is a rigid body with mass and velocity.

| Body | Mass | Vel_X | Vel_Y |
```

The sentences between are consumed and produce no bytecode. This means you can (and should) write rich documentation alongside your executable logic.

## Best Practices

1. **One domain per concern** --- `# Config`, `# Physics`, `# Rendering`
2. **Routines as transactions** --- each `##` does one thing
3. **Intent names are API design** - choose clear, unique, discoverable phrases
4. **Tables are schemas** --- the header row is your type definition
5. **Use `mks check` early** - catch import and compilation issues fast
6. **Use `mks disasm` to debug** --- see exactly what bytecode your markdown produces
