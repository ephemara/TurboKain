# MarkScript - Possibilities

> What you can build with a markdown-native bytecode VM.

---

## 1. Executable Documentation

Write READMEs that compile. Every project's `README.md` becomes its own test, its own spec, and its own executable documentation.

```bash
mks run README.md
# → Your docs just ran. All tables parsed. All intents dispatched.
```

**Who this is for:** Open-source projects, API docs, tutorials that need to stay in sync with code -- because the docs ARE the code.

## 2. Configuration as Executable Prose

Replace YAML/JSON/TOML configs with markdown files that do more:

```markdown
# PipelineConfig

## sources
| Name   | Path          | Format |
|--------|---------------|--------|
| Orders  | /data/orders  | parquet |
| Users   | /api/users    | json   |

> connect to source "Orders"
> connect to source "Users"

## transforms
> apply schema mapping
> deduplicate by "order_id"
> write sink "gold_orders"
```

**Who this is for:** Data pipelines, ETL jobs, infra config - places where configuration files should be self-verifying.

## 3. Game Design Documents That Run

Write game specs in prose. The designer writes the design doc. The same file runs the prototype.

```markdown
# PongGame

## physics_tick
| Body | Mass | Vel_X | Vel_Y |
|------|------|-------|-------|
| Ball | 1    | 3     | 2     |
| PaddleL | 0  | 0     | 0     |

> apply physics
> check collisions
> update positions
```

Check out `examples/pong.md` - 8 domains, 24 routines, 30 intents, 9 data tables, all prose.

**Who this is for:** Game jams, rapid prototyping, design docs that should never go stale.

## 4. Simulation Orchestration

Drive physics simulations, agent-based models, or N-body systems from readable markdown:

```markdown
# NBodySimulation

> import kain "physics/engine.kn"

## setup_scene
| Body  | Mass | Pos_X | Pos_Y |
|-------|------|-------|-------|
| Sun   | 1000 | 0     | 0     |
| Earth | 1    | 100   | 0     |

> set gravity 9.81
> run simulation 1000 steps
```

Check `projects/mks-ultra/` for a working example - a Kain physics engine orchestrated through MarkScript.

**Who this is for:** Scientists, engineers, anyone writing simulation scripts that non-experts should be able to read and modify.

## 5. CI/CD Pipelines

Write pipeline definitions in prose that reads like docs:

```markdown
# BuildPipeline

## lint
> run "kain check src/"
> assert lint_exit_code 0

## test
> run "kain test --json"
> assert test_failures 0

## deploy
> run "kain build --release"
> write file "dist/version.txt" "1.0.0"
> run "rsync -a dist/ deploy-server:/app/"
```

**Who this is for:** DevOps engineers tired of YAML indentation errors and undocumented pipeline configs.

## 6. Hardware Control Scripts

Servo calibration, sensor readout, robot control -- readable by both engineers and operators:

```markdown
# ServoController

## calibrate
| Joint | Min | Max | Center |
|-------|-----|-----|--------|
| Base  | 0   | 180 | 90     |
| Shoulder | 0 | 90  | 45     |

> calibrate joint 0
> home all axes

## emergency_stop
> halt all motion
> set brake 1
```

Check `examples/servo_controller.md` -- includes inline C ISR handlers alongside the markdown orchestration.

**Who this is for:** Robotics, embedded systems, IoT -- places where operator-readability matters as much as correctness.

## 7. Literate Programs

The full literate programming vision --- code and documentation in one file, compiled to one binary.

```markdown
# CompressionTool

This tool compresses files using a run-length encoding algorithm.
The implementation is written in Kain, orchestrated by MarkScript.

## encode

The encoder scans input bytes and collapses runs of identical values.

> read file input.bin
> encode to run-length format
> write file output.rle

```kain
fn rle_encode(data: Array<Byte>) -> Array<Byte>:
    // ... implementation
```

## decode

> read file output.rle
> decode from run-length format
> assert decoded == original
```

**Who this is for:** Anyone who believes programs should be read by humans first and machines second.

## 8. Domain-Specific Markdown Dialects

Build custom mini-languages on top of MarkScript. The IVT is the extension point -- register handlers for your domain's vocabulary.

**Examples:**
- **Music:** `> note C4 120bpm` → MIDI output
- **Chemistry:** `> react H2 + O2 -> H2O` → reaction simulator
- **Network:** `> tcp connect host:port` → connection tester
- **Finance:** `> price option --type call --strike 100` → Black-Scholes
- **Graphics:** `> draw rect 10 10 50 50` → 2D renderer

Since MarkScript is compiled through Kain's LLVM backend, no interpreter overhead stands between you and native performance.

---

## The Big Idea

MarkScript proves a thesis: **your README can be your executable**. The boundary between documentation and code is artificial. When you compile prose to native code, every design decision is self-documenting, every table is self-describing, and every pipeline is self-verifying.

The future of MarkScript isn't adding features - it's showing that one file can be both the clearest explanation and the most correct implementation simultaneously.
