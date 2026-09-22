# GameEngine

The game engine domain runs the main loop: physics, AI, rendering.

## physics_tick

> apply gravity
> resolve collisions
> update transforms

| Object   | Mass | Velocity_X | Velocity_Y |
|----------|------|------------|------------|
| Player   | 80   | 0          | -9         |
| Crate    | 200  | 12         | 0          |
| Debris   | 5    | 45         | -3         |
| Explosive| 50   | -20        | 18         |
| Projectile| 2   | 500        | 0          |

## ai_update

> compute pathfinding
> evaluate behavior trees
> update navmesh

| Agent    | State    | Target_X | Target_Y | Priority |
|----------|----------|----------|----------|----------|
| Guard_1  | Patrol   | 150      | 300      | 0        |
| Guard_2  | Alert    | 200      | 350      | 2        |
| Drone_1  | Scan     | 100      | 100      | 0        |
| Boss     | Combat   | 250      | 250      | 3        |

## render_frame

> cull frustum
> bind textures
> submit draw calls
> present swapchain

| Pass       | DrawCalls | Triangles | GPU_Time_ms |
|------------|-----------|-----------|-------------|
| Shadow     | 1247      | 892000    | 2.3         |
| G-Buffer   | 3412      | 2100000   | 5.1         |
| Lighting   | 892       | 450000    | 3.7         |
| PostFX     | 156       | 24000     | 1.2         |
| UI         | 89        | 12000     | 0.4         |
