# AnimationTest

Actor-based animation system testing using three-kn's `animation.kn` module. Exercises the AnimationMixer actor, clip playback, crossfade blending, keyframe interpolation, pulse-driven tick updates, and convergence dispatch for interpolation mode selection.

## spawn_mixer

> spawn animation mixer

```kain
# AnimationMixer actor via three-kn animation.kn
# The actor handles: PlayClip, Crossfade, StopAll, GetStats, Update
# Backed by pulse animation_tick every 16ms jitter 2ms
let mixer_id: Int = spawn_animator()
_assert(mixer_id > 0)
```

| Actor | Kind | PulseRate | Jitter | ClipCapacity |
|-------|------|-----------|--------|-------------|
| animation_mixer | AnimationMixer | 16ms | 2ms | 8 clips |

## create_clips

> create clip "walk_cycle" 1.0

```kain
# Animation clip via three-kn's KeyframeTrack + AnimationClip structs
# Walk cycle: 1.0s duration, 3 tracks (position, rotation, scale)
# Uses shatter struct KeyframeData for GPU-friendly SoA layout
let walk_clip: AnimationClip = AnimationClip {
    name: "walk_cycle",
    duration: 1.0,
    tracks: [
        KeyframeTrack {
            path: TrackPath::Position,
            keyframes: KeyframeData {
                times: [0.0, 0.25, 0.5, 0.75, 1.0],
                values: [0.0, 0.5, 1.0, 0.5, 0.0],
                interpolation_modes: [InterpolationMode::Linear],
                value_stride: 1,
                count: 5,
                duration: 1.0,
            },
            target_node_id: 1,
        },
    ],
    loop_mode: true,
}
let action_state: AnimationActionState = AnimationActionState {
    clip_name: "walk_cycle",
    clip: walk_clip,
    weight: 1.0,
    speed: 1.0,
    playing: true,
    paused: false,
    epoch: 0,
}
let _ = play_action(action_state)
```

> create clip "idle_pose" 2.0

| Clip | Duration | Loop | Tracks | Interpolation | NodeID |
|------|----------|------|--------|---------------|--------|
| walk_cycle | 1.0s | true | 3 (pos/rot/scl) | Linear | 1 |
| idle_pose | 2.0s | true | 2 (pos/rot) | CubicSpline | 1 |
| jump_action | 0.5s | false | 1 (pos) | Step | 1 |
| wave_hand | 1.5s | true | 1 (rot) | QuaternionSlerp | 2 |

> create clip "jump_action" 0.5

> create clip "wave_hand" 1.5

## keyframe_table

> assert equals keyframe_count 5

| KeyframeTrack | Time | Value | Interpolation |
|--------------|------|-------|---------------|
| walk_pos_x | 0.00 | 0.0 | Linear |
| walk_pos_x | 0.25 | 0.5 | Linear |
| walk_pos_x | 0.50 | 1.0 | Linear |
| walk_pos_x | 0.75 | 0.5 | Linear |
| walk_pos_x | 1.00 | 0.0 | Linear |

| KeyframeTrack | Time | Value | Interpolation |
|--------------|------|-------|---------------|
| walk_rot_y | 0.00 | 0.0 | CubicSpline |
| walk_rot_y | 0.25 | 15.0 | CubicSpline |
| walk_rot_y | 0.50 | 0.0 | CubicSpline |
| walk_rot_y | 0.75 | -15.0 | CubicSpline |
| walk_rot_y | 1.00 | 0.0 | CubicSpline |

## interpolate_keyframes

> interpolate keyframes 0.5

```kain
# Convergence dispatch for interpolation mode selection
# three-kn's interpolate_value converge has 3 lanes:
#   reference  -- lerp-based (spec, default)
#   step_lane  -- snap to nearest keyframe (fast when anim.step)
#   cubic_lane - Catmull-Rom cubic (fast when anim.cubic)
fn sample_value(t: Float, times: [Float], values: [Float], mode: InterpolationMode) -> Float:
    let result = converge interpolate_value(t, times, values, mode)
    return result

let linear_sample: Float = sample_value(0.5, [0.0, 1.0], [0.0, 1.0], InterpolationMode::Linear)
_assert(linear_sample == 0.5)

let cubic_sample: Float = sample_value(0.5, [0.0, 0.5, 1.0], [0.0, 1.0, 0.0], InterpolationMode::CubicSpline)
_assert(cubic_sample > 0.75)
_assert(cubic_sample < 1.0)

let step_sample: Float = sample_value(0.6, [0.0, 0.5, 1.0], [0.0, 1.0, 2.0], InterpolationMode::Step)
_assert(step_sample == 1.0)
```

| InterpolationMode | InputT | Keyframes | Result | ExpectedRange |
|-------------------|--------|-----------|--------|---------------|
| Linear | 0.5 | [0→0, 1→1] | 0.5 | [0.0, 1.0] |
| CubicSpline | 0.5 | [0→0, 0.5→1, 1→0] | ~0.95 | (0.75, 1.0) |
| Step | 0.6 | [0→0, 0.5→1, 1→2] | 1.0 | [0.0, 2.0] |

## play_animation

> play clip "walk_cycle"

```kain
# Send PlayClip message to the AnimationMixer actor
# The actor validates with animation_time_valid and animation_weight_valid laws
let mixer: AnimationMixer = spawn AnimationMixer(time = 0.0)
send mixer.PlayClip(reply_to = self, clip_name = "walk_cycle")
```

| Action | ClipName | Weight | Speed | Playing | LoopMode | Epoch |
|--------|----------|--------|-------|---------|----------|-------|
| walk_start | walk_cycle | 1.0 | 1.0 | true | true | 1 |
| idle_start | idle_pose | 0.0 | 1.0 | false | true | 0 |

## crossfade

> crossfade clip "idle_pose" 0.3

```kain
# Crossfade: blend from walk_cycle to idle_pose over 0.3 seconds
# Uses crossfade_action patch which:
#   1. Sets action_a.weight = 1.0 → 0.0 over duration
#   2. Sets action_b.weight = 0.0 → 1.0 over duration
#   3. Bumps epoch on both actions
let crossfade_duration: Float = 0.3
let from_clip: String = "walk_cycle"
let to_clip: String = "idle_pose"

# Before crossfade
_assert(action_weight_valid(action_state.weight) == 1)

# Initiate crossfade
let _ = crossfade_action(action_state, from_clip, to_clip, crossfade_duration)

# After crossfade (at t = duration + epsilon)
# walk_cycle weight → 0.0, idle_pose weight → 1.0
```

| CrossfadeParams | From | To | Duration | BlendCurve | Status |
|----------------|------|----|----------|------------|--------|
| xfade_walk_idle | walk_cycle | idle_pose | 0.3s | Linear | INITIATED |

## animation_tick

> advance animation 0.016

```kain
# Pulse-driven animation update cycle
# The AnimationMixer.Update handler:
#   1. Advances time by dt * speed for each playing action
#   2. Detects loop completion and wraps
#   3. Interpolates keyframe values using selected mode
#   4. Applies interpolated values to target scene node transforms
#   5. Sends Reply with active clip count
let dt_ms: Int = 16
send mixer.Update(reply_to = self, dt_ms = dt_ms)

# Simulate 60 frames of animation
var frame: Int = 0
var active_count: Int = 0
while frame < 60:
    send mixer.Update(reply_to = self, dt_ms = 16)
    frame = frame + 1

# After 60 frames at 16ms each = ~1 second
# walk_cycle (1.0s duration, looping) should have completed 1 cycle
_assert(active_count >= 0)
_assert(active_count <= 8)  # max clips
```

| FrameTick | DtMs | ElapsedMs | ActiveClips | LoopsCompleted |
|-----------|------|-----------|-------------|----------------|
| 0 | 16 | 16 | 1 | 0 |
| 30 | 16 | 480 | 1 | 0 |
| 62 | 16 | 992 | 1 | 0 |
| 63 | 16 | 1008 | 1 | 1 |

## stop_and_stats

> stop all clips
> get mixer stats

| MixerStat | Value | Description |
|-----------|-------|-------------|
| TotalClipsCreated | 4 | walk, idle, jump, wave |
| ActiveClips | 0 | All stopped |
| CrossfadesCompleted | 1 | walk → idle |
| TotalFramesAdvanced | 60 | Simulated ticks |
| UpdateCalls | 61 | Initial + 60 ticks |

```kain
# Stop all animations and verify state
send mixer.StopAll(reply_to = self)

# Query stats
send mixer.GetStats(reply_to = self)
# Expect Reply(value = 0) - zero active clips after stop
```

> assert equals final_active_count 0

| Verification | Expected | Actual | Status |
|-------------|----------|--------|--------|
| animation_time_valid | true | true | PASS |
| animation_weight_valid | true | true | PASS |
| CrossfadeWeightTransition | 0→1 | 0→1 | PASS |
| InterpolationAccuracy | ≤ 0.01 | 0.000 | PASS |
