# PhysicsSim

## ComputeForces

> apply gravity

| Mass | Velocity | Drag |
| 1.5  | 10.0     | 0.1  |
| 2.0  | 5.0      | 0.2  |
| 0.5  | 20.0     | 0.05 |

> render frame

```kain
let frame = frame + 1
println("frame: " + str(frame))
```

## Cleanup

> free memory

```c
free(particles);
```
