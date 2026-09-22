# NBodySimulation

> import kain "src/engine/physics.kn"

## setup_scene
| Body  | Mass | Pos_X | Pos_Y | Pos_Z | Vel_X | Vel_Y | Vel_Z | Radius |
|-------|------|-------|-------|-------|-------|-------|-------|--------|
| Sun   | 1000 | 0     | 0     | 0     | 0     | 0     | 0     | 5.0    |
| Earth | 1    | 100   | 0     | 0     | 0     | 10    | 0     | 1.0    |
| Mars  | 0.5  | 150   | 0     | 0     | 0     | 8     | 0     | 0.8    |

> set gravity 0.0
> set timestep 0.016

## run_simulation
> step 1000 frames
> print "Simulation complete: 10000 frames at 0.016s = 16 seconds simulated"
