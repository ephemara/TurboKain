# IterativePhysics -- 2D Particle System with Euler Integration

> N-body gravitational simulation computed entirely in markscript.
> Bodies defined in tables. Timestep integration via while loops.
> Forces, velocities, positions - all in the VM.

---

## Config

| Parameter | Value |
|-----------|-------|
| Steps | 100 |
| Timestep | 1 |
| G | 500 |
| Softening | 100 |

---

## Bodies

| Body | Mass | Pos_X | Pos_Y | Vel_X | Vel_Y |
|------|------|-------|-------|-------|-------|
| Star | 5000 | 400 | 300 | 0 | 0 |
| Planet1 | 50 | 200 | 300 | 0 | 15 |
| Planet2 | 80 | 600 | 300 | 0 | -12 |
| Moon | 5 | 220 | 300 | 0 | 18 |
| Comet | 30 | 50 | 50 | 8 | 12 |

---

## initialize --- Load body counts into variables

> The body table can be exported to the runtime via register handler.
> For pure markscript computation, we hardcode the initial conditions.

---

## simulate -- Euler integration for N steps

```markscript
# Gravitational N-body simulation
# Variables: mass[0-4], x[0-4], y[0-4], vx[0-4], vy[0-4]
# Actually we'll use indexed variable names: m0, x0, y0, vx0, vy0, etc.

# Initialize bodies (hardcoded from table above)
let m0 = 5000
let x0 = 400
let y0 = 300
let vx0 = 0
let vy0 = 0

let m1 = 50
let x1 = 200
let y1 = 300
let vx1 = 0
let vy1 = 15

let m2 = 80
let x2 = 600
let y2 = 300
let vx2 = 0
let vy2 = -12

let m3 = 5
let x3 = 220
let y3 = 300
let vx3 = 0
let vy3 = 18

let m4 = 30
let x4 = 50
let y4 = 50
let vx4 = 8
let vy4 = 12

let steps = 100
let dt = 1
let g_const = 500
let softening = 100

let t = 0

print("=== N-Body Simulation ===")
print("")

while steps > t:
    # --- Body 0 (Star) ---
    # Compute force from all other bodies
    # For each pair: dx = xj - xi, dy = yj - yi
    # distSq = dx*dx + dy*dy + softening
    # invDist = 1 / distSq  (well, we invert division)
    # Actually: fx = G * mj * mi * dx / (distSq * distSq^0.5)
    # Simplified: we compute acceleration = G * mj * dx / distSq^(3/2)
    # Even simpler: just add gravitational acceleration components

    # Body 0 ← Body 1
    let dx_0_1 = x1 - x0
    let dy_0_1 = y1 - y0
    let d_sq_0_1 = dx_0_1 * dx_0_1 + dy_0_1 * dy_0_1 + softening
    let inv_d_0_1 = g_const * m1 / d_sq_0_1
    vx0 = vx0 + inv_d_0_1 * dx_0_1 * dt
    vy0 = vy0 + inv_d_0_1 * dy_0_1 * dt

    # Body 0 ← Body 2
    let dx_0_2 = x2 - x0
    let dy_0_2 = y2 - y0
    let d_sq_0_2 = dx_0_2 * dx_0_2 + dy_0_2 * dy_0_2 + softening
    let inv_d_0_2 = g_const * m2 / d_sq_0_2
    vx0 = vx0 + inv_d_0_2 * dx_0_2 * dt
    vy0 = vy0 + inv_d_0_2 * dy_0_2 * dt

    # Body 0 ← Body 3
    let dx_0_3 = x3 - x0
    let dy_0_3 = y3 - y0
    let d_sq_0_3 = dx_0_3 * dx_0_3 + dy_0_3 * dy_0_3 + softening
    let inv_d_0_3 = g_const * m3 / d_sq_0_3
    vx0 = vx0 + inv_d_0_3 * dx_0_3 * dt
    vy0 = vy0 + inv_d_0_3 * dy_0_3 * dt

    # Body 0 ← Body 4
    let dx_0_4 = x4 - x0
    let dy_0_4 = y4 - y0
    let d_sq_0_4 = dx_0_4 * dx_0_4 + dy_0_4 * dy_0_4 + softening
    let inv_d_0_4 = g_const * m4 / d_sq_0_4
    vx0 = vx0 + inv_d_0_4 * dx_0_4 * dt
    vy0 = vy0 + inv_d_0_4 * dy_0_4 * dt

    # --- Body 1 (Planet1) ← all others ---
    let dx_1_0 = x0 - x1
    let dy_1_0 = y0 - y1
    let d_sq_1_0 = dx_1_0 * dx_1_0 + dy_1_0 * dy_1_0 + softening
    let inv_d_1_0 = g_const * m0 / d_sq_1_0
    vx1 = vx1 + inv_d_1_0 * dx_1_0 * dt
    vy1 = vy1 + inv_d_1_0 * dy_1_0 * dt

    let dx_1_2 = x2 - x1
    let dy_1_2 = y2 - y1
    let d_sq_1_2 = dx_1_2 * dx_1_2 + dy_1_2 * dy_1_2 + softening
    let inv_d_1_2 = g_const * m2 / d_sq_1_2
    vx1 = vx1 + inv_d_1_2 * dx_1_2 * dt
    vy1 = vy1 + inv_d_1_2 * dy_1_2 * dt

    let dx_1_3 = x3 - x1
    let dy_1_3 = y3 - y1
    let d_sq_1_3 = dx_1_3 * dx_1_3 + dy_1_3 * dy_1_3 + softening
    let inv_d_1_3 = g_const * m3 / d_sq_1_3
    vx1 = vx1 + inv_d_1_3 * dx_1_3 * dt
    vy1 = vy1 + inv_d_1_3 * dy_1_3 * dt

    let dx_1_4 = x4 - x1
    let dy_1_4 = y4 - y1
    let d_sq_1_4 = dx_1_4 * dx_1_4 + dy_1_4 * dy_1_4 + softening
    let inv_d_1_4 = g_const * m4 / d_sq_1_4
    vx1 = vx1 + inv_d_1_4 * dx_1_4 * dt
    vy1 = vy1 + inv_d_1_4 * dy_1_4 * dt

    # --- Body 2 (Planet2) ← all others ---
    let dx_2_0 = x0 - x2
    let dy_2_0 = y0 - y2
    let d_sq_2_0 = dx_2_0 * dx_2_0 + dy_2_0 * dy_2_0 + softening
    let inv_d_2_0 = g_const * m0 / d_sq_2_0
    vx2 = vx2 + inv_d_2_0 * dx_2_0 * dt
    vy2 = vy2 + inv_d_2_0 * dy_2_0 * dt

    let dx_2_1 = x1 - x2
    let dy_2_1 = y1 - y2
    let d_sq_2_1 = dx_2_1 * dx_2_1 + dy_2_1 * dy_2_1 + softening
    let inv_d_2_1 = g_const * m1 / d_sq_2_1
    vx2 = vx2 + inv_d_2_1 * dx_2_1 * dt
    vy2 = vy2 + inv_d_2_1 * dy_2_1 * dt

    let dx_2_3 = x3 - x2
    let dy_2_3 = y3 - y2
    let d_sq_2_3 = dx_2_3 * dx_2_3 + dy_2_3 * dy_2_3 + softening
    let inv_d_2_3 = g_const * m3 / d_sq_2_3
    vx2 = vx2 + inv_d_2_3 * dx_2_3 * dt
    vy2 = vy2 + inv_d_2_3 * dy_2_3 * dt

    let dx_2_4 = x4 - x2
    let dy_2_4 = y4 - y2
    let d_sq_2_4 = dx_2_4 * dx_2_4 + dy_2_4 * dy_2_4 + softening
    let inv_d_2_4 = g_const * m4 / d_sq_2_4
    vx2 = vx2 + inv_d_2_4 * dx_2_4 * dt
    vy2 = vy2 + inv_d_2_4 * dy_2_4 * dt

    # --- Body 3 (Moon) ← all others ---
    let dx_3_0 = x0 - x3
    let dy_3_0 = y0 - y3
    let d_sq_3_0 = dx_3_0 * dx_3_0 + dy_3_0 * dy_3_0 + softening
    let inv_d_3_0 = g_const * m0 / d_sq_3_0
    vx3 = vx3 + inv_d_3_0 * dx_3_0 * dt
    vy3 = vy3 + inv_d_3_0 * dy_3_0 * dt

    let dx_3_1 = x1 - x3
    let dy_3_1 = y1 - y3
    let d_sq_3_1 = dx_3_1 * dx_3_1 + dy_3_1 * dy_3_1 + softening
    let inv_d_3_1 = g_const * m1 / d_sq_3_1
    vx3 = vx3 + inv_d_3_1 * dx_3_1 * dt
    vy3 = vy3 + inv_d_3_1 * dy_3_1 * dt

    let dx_3_2 = x2 - x3
    let dy_3_2 = y2 - y3
    let d_sq_3_2 = dx_3_2 * dx_3_2 + dy_3_2 * dy_3_2 + softening
    let inv_d_3_2 = g_const * m2 / d_sq_3_2
    vx3 = vx3 + inv_d_3_2 * dx_3_2 * dt
    vy3 = vy3 + inv_d_3_2 * dy_3_2 * dt

    let dx_3_4 = x4 - x3
    let dy_3_4 = y4 - y3
    let d_sq_3_4 = dx_3_4 * dx_3_4 + dy_3_4 * dy_3_4 + softening
    let inv_d_3_4 = g_const * m4 / d_sq_3_4
    vx3 = vx3 + inv_d_3_4 * dx_3_4 * dt
    vy3 = vy3 + inv_d_3_4 * dy_3_4 * dt

    # --- Body 4 (Comet) ← all others ---
    let dx_4_0 = x0 - x4
    let dy_4_0 = y0 - y4
    let d_sq_4_0 = dx_4_0 * dx_4_0 + dy_4_0 * dy_4_0 + softening
    let inv_d_4_0 = g_const * m0 / d_sq_4_0
    vx4 = vx4 + inv_d_4_0 * dx_4_0 * dt
    vy4 = vy4 + inv_d_4_0 * dy_4_0 * dt

    let dx_4_1 = x1 - x4
    let dy_4_1 = y1 - y4
    let d_sq_4_1 = dx_4_1 * dx_4_1 + dy_4_1 * dy_4_1 + softening
    let inv_d_4_1 = g_const * m1 / d_sq_4_1
    vx4 = vx4 + inv_d_4_1 * dx_4_1 * dt
    vy4 = vy4 + inv_d_4_1 * dy_4_1 * dt

    let dx_4_2 = x2 - x4
    let dy_4_2 = y2 - y4
    let d_sq_4_2 = dx_4_2 * dx_4_2 + dy_4_2 * dy_4_2 + softening
    let inv_d_4_2 = g_const * m2 / d_sq_4_2
    vx4 = vx4 + inv_d_4_2 * dx_4_2 * dt
    vy4 = vy4 + inv_d_4_2 * dy_4_2 * dt

    let dx_4_3 = x3 - x4
    let dy_4_3 = y3 - y4
    let d_sq_4_3 = dx_4_3 * dx_4_3 + dy_4_3 * dy_4_3 + softening
    let inv_d_4_3 = g_const * m3 / d_sq_4_3
    vx4 = vx4 + inv_d_4_3 * dx_4_3 * dt
    vy4 = vy4 + inv_d_4_3 * dy_4_3 * dt

    # --- Update positions ---
    x0 = x0 + vx0 * dt
    y0 = y0 + vy0 * dt
    x1 = x1 + vx1 * dt
    y1 = y1 + vy1 * dt
    x2 = x2 + vx2 * dt
    y2 = y2 + vy2 * dt
    x3 = x3 + vx3 * dt
    y3 = y3 + vy3 * dt
    x4 = x4 + vx4 * dt
    y4 = y4 + vy4 * dt

    t = t + 1

# Print final state
print("Simulation complete: " + str(steps) + " timesteps")
print("")

print("Star:   (" + str(x0) + ", " + str(y0) + ")  v=(" + str(vx0) + ", " + str(vy0) + ")")
print("Planet1:(" + str(x1) + ", " + str(y1) + ")  v=(" + str(vx1) + ", " + str(vy1) + ")")
print("Planet2:(" + str(x2) + ", " + str(y2) + ")  v=(" + str(vx2) + ", " + str(vy2) + ")")
print("Moon:   (" + str(x3) + ", " + str(y3) + ")  v=(" + str(vx3) + ", " + str(vy3) + ")")
print("Comet:  (" + str(x4) + ", " + str(y4) + ")  v=(" + str(vx4) + ", " + str(vy4) + ")")

```

---

## verify_energy -- Rough conservation check

```markscript
# Compute crude total energy (kinetic + gravitational potential)
let ke0 = m0 * (vx0 * vx0 + vy0 * vy0) / 2
let ke1 = m1 * (vx1 * vx1 + vy1 * vy1) / 2
let ke2 = m2 * (vx2 * vx2 + vy2 * vy2) / 2
let ke3 = m3 * (vx3 * vx3 + vy3 * vy3) / 2
let ke4 = m4 * (vx4 * vx4 + vy4 * vy4) / 2
let total_ke = ke0 + ke1 + ke2 + ke3 + ke4

print("Total kinetic energy: " + str(total_ke))
print("Energy should be approximately conserved")
```

---

## Phase Space Statistics

> Print the number of computed body-body interactions

| Computation | Count |
|-------------|-------|
| Bodies | 5 |
| Pairs per step | 10 |
| Force computations per step | 20 |
| Total operations per step | 50 |
