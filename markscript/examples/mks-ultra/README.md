# mks-ultra - Markscript-Embedded Kain Physics Engine

A rigid body physics engine written in Kain with orchestration through the [Markscript](https://github.com/kain-lang/markscript) intent engine.

## Architecture

```
┌─────────────────────────────────────────────┐
│              Markscript VM (.md)            │
│  Tables → body data, forces, parameters     │
│  Intents → call physics.xxx                 │
│  Fenced code → kain physics integration     │
└──────────────┬──────────────────────────────┘
               │ IVT dispatch
┌──────────────▼──────────────────────────────┐
│         Kain Physics Engine (src/)           │
│  ┌──────────┐ ┌──────────┐ ┌────────────┐   │
│  │ physics  │ │ collision│ │ integrator │   │
│  │ Vec3     │ │ AABB     │ │ Euler      │   │
│  │ RigidBody│ │ Sphere   │ │ Verlet     │   │
│  │          │ │ Raycast  │ │ RK4        │   │
│  └──────────┘ └──────────┘ └────────────┘   │
└──────────────────────────────────────────────┘
```

## Quick Start

### Check

```powershell
kain check src/main.kn --target llvm
```

### Build

```powershell
kain build . --target llvm
```

### Run (raw Kain entry)

```powershell
kain run src/main.kn --target llvm
```

### Run (with Markscript simulation)

```powershell
kain run scripts/sim.md --target llvm
```

## Engine Modules

| Module | File | Description |
|--------|------|-------------|
| `physics` | `src/engine/physics.kn` | `Vec3`, `RigidBody`, force/impulse application |
| `collision` | `src/engine/collision.kn` | `AABB`, sphere/raycast collision detection |
| `integrator` | `src/engine/integrator.kn` | Euler, Verlet, RK4 force integrators |

## Project Structure

```
mks-ultra/
├── build.kn              # Kain project authority
├── KAIN.toml             # Blade metadata
├── README.md             # ← this file (self-executing docs)
├── src/
│   ├── main.kn           # Entry point, imports engine modules
│   └── engine/
│       ├── physics.kn    # 3D math + rigid body types
│       ├── collision.kn  # Collision detection scaffold
│       └── integrator.kn # Force integration scaffold
└── scripts/
    └── sim.md            # Markscript simulation definition
```

## Simulation Parameters

| Field | Default | Description |
|-------|---------|-------------|
| `dt` | 0.016 | Timestep in seconds (~60 FPS) |
| `gravity` | (0, -9.81, 0) | Gravitational acceleration |
| `integrator` | euler | Integration method (euler / verlet / rk4) |

## License

MIT - see root `LICENSE`.
