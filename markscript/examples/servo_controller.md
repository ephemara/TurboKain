# ServoController

A servo motor control system with fenced code blocks for the PID loop.

```kain
# This is a Kain code block inside a MarkScript file
# It contains the PID controller implementation

fn pid_compute(setpoint: Int, measured: Int, kp: Int, ki: Int, kd: Int) -> Int:
    let error = setpoint - measured
    return error * kp / 100
```

## calibrate

> home servo
> measure backlash
> store calibration

| Servo | Min_PWM | Max_PWM | Home_Pos | Backlash |
|-------|---------|---------|----------|----------|
| Joint1| 100     | 900     | 500      | 2        |
| Joint2| 120     | 880     | 510      | 1        |
| Joint3| 90      | 910     | 490      | 3        |
| Joint4| 110     | 890     | 505      | 1        |
| Joint5| 105     | 895     | 495      | 2        |
| Joint6| 95      | 905     | 500      | 1        |

## move_to_position

> compute inverse kinematics
> plan trajectory
> execute move

```c
// C motor control interrupt handler
void ISR_motor_tick(void) {
    for (int axis = 0; axis < 6; axis++) {
        uint16_t pwm = compute_pwm(axis, target[axis], current[axis]);
        TIM_SetCompare(axis, pwm);
    }
}
```

> verify position
| Axis | Target | Actual  | Error |
|------|--------|---------|-------|
| X    | 150.0  | 149.8   | 0.2   |
| Y    | 200.0  | 200.1   | 0.1   |
| Z    | 75.0   | 74.9    | 0.1   |
| Roll | 0.0    | 0.05    | 0.05  |
| Pitch| 45.0   | 44.8    | 0.2   |
| Yaw  | 90.0   | 90.0    | 0.0   |

## emergency_stop

> kill motor power
> engage brakes
> log fault

| Signal      | Status  | Timestamp |
|-------------|---------|-----------|
| E-Stop      | HIGH    | 12:34:56  |
| PowerRelay  | OPEN    | 12:34:56  |
| BrakeEngage | ACTIVE  | 12:34:57  |
| FaultLog    | WRITTEN | 12:34:57  |
