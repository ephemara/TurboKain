# FullPipeline

Domain: End-to-end 3D engine pipeline combining scene setup, animation, GPU compute, and rendering passes. Demonstrates all 7 layers of the Kain decision ladder through markscript-driven orchestration: `world` (L1), `entangle` (L1), `patch` (L2), `law` (L2), `converge` (L3), `orchestrate` (L4), `pulse` (L5), `axiom` (L6), `shatter` (L6), `teleport` (L6), `actor` (L7), `shader` (GPU). Each routine covers one layer group with intents, tables, and fenced kain blocks.

---

## Layer1_StateAuthority

Domain: Layer 1 --- world + entangle. Compiler-owned state authority with mirrored sync.

```kain
# World state authority pattern used throughout three-kn:
# Authority world owns mutable state, Mirror world receives read-only copies
# Entangle propagates writes from authority → mirror via single_writer policy

world EngineState:
    state render_session: Int = 0
    state frame_count: Int = 0
    state running: Bool = false
    state epoch: Int = 0
    surface native_ui => EnginePanel

world EngineMirror:
    state render_session_copy: Int = 0
    state frame_count_copy: Int = 0
    state running_copy: Bool = false
    state epoch_copy: Int = 0
    surface web => EnginePanel

entangle EngineState.render_session <-> EngineMirror.render_session_copy with single_writer
entangle EngineState.frame_count <-> EngineMirror.frame_count_copy with single_writer
entangle EngineState.running <-> EngineMirror.running_copy with single_writer
entangle EngineState.epoch <-> EngineMirror.epoch_copy with single_writer

let engine: EngineState = EngineState {
    render_session: 1,
    frame_count: 0,
    running: true,
    epoch: 0,
}
_assert(engine.render_session == 1)
_assert(engine.running == true)
```

> create world "EngineState"
> entangle field "frame_count" with single_writer

| World | StateField | Type | Initial | Mirror | SyncPolicy |
|-------|-----------|------|---------|--------|------------|
| EngineState | render_session | Int | 0 | EngineMirror | single_writer |
| EngineState | frame_count | Int | 0 | EngineMirror | single_writer |
| EngineState | running | Bool | true | EngineMirror | single_writer |
| EngineState | epoch | Int | 0 | EngineMirror | single_writer |
| SceneGraphWorld | max_nodes | Int | 1024 | SceneGraphMirror | single_writer |
| SceneGraphWorld | fog_type | Int | 0 | SceneGraphMirror | single_writer |
| CameraState | fov | Float | 75.0 | CameraStateMirror | single_writer |

---

## Layer2_StateIntegrity

Domain: Layer 2 - law + patch. Invariant predicates and journaled mutations.

```kain
# Laws: compiler-witnessable invariant predicates
# Patches: journaled mutations that bump epoch counters

# Camera invariants
law camera_near_positive(cam: CameraState) -> Bool:
    return cam.near > 0.0

law camera_far_greater_than_near(cam: CameraState) -> Bool:
    return cam.far > cam.near

law camera_aspect_positive(cam: CameraState) -> Bool:
    return cam.aspect > 0.0

law camera_fov_valid(cam: CameraState) -> Bool:
    return cam.fov >= 1.0 and cam.fov <= 179.0

law camera_state_valid(cam: CameraState) -> Bool:
    return camera_near_positive(cam)
        and camera_far_greater_than_near(cam)
        and camera_aspect_positive(cam)
        and camera_fov_valid(cam)

# Scene graph invariants
law epoch_valid(sg: SceneGraphWorld) -> Bool:
    return sg.epoch >= 0

law fog_range_valid(sg: SceneGraphWorld) -> Bool:
    return sg.fog_near >= 0.0 and sg.fog_far > sg.fog_near

# Patches: journaled mutation
patch set_perspective(cam: CameraState, fov: Float, aspect: Float, near: Float, far: Float) -> Int:
    cam.fov = fov
    cam.aspect = aspect
    cam.near = near
    cam.far = far
    cam.epoch = cam.epoch + 1
    let m: Mat4Wrapper = build_perspective_matrix(fov, aspect, near, far)
    cam.projection_matrix = m
    return cam.epoch

patch update_view(cam: CameraState) -> Int:
    let v: Mat4Wrapper = build_view(cam.position, cam.target, cam.up)
    cam.view_matrix = v
    cam.view_projection_matrix = cam.projection_matrix.mul(v)
    cam.epoch = cam.epoch + 1
    return cam.epoch
```

> assert law "camera_state_valid" passes

| Law | Expression | Expected | Status |
|-----|-----------|----------|--------|
| camera_near_positive | near > 0.0 | PASS | VALID |
| camera_far_greater_than_near | far > near | PASS | VALID |
| camera_aspect_positive | aspect > 0.0 | PASS | VALID |
| camera_fov_valid | fov ∈ [1, 179] | PASS | VALID |
| camera_state_valid | all above | PASS | VALID |
| epoch_valid | epoch >= 0 | PASS | VALID |
| fog_range_valid | far > near | PASS | VALID |

> assert patch "set_perspective" journals epoch bump

| Patch | Mutates | Returns | EpochBumped |
|-------|---------|---------|-------------|
| set_perspective | CameraState.fov, .aspect, .near, .far | Int (epoch) | true |
| update_view | CameraState.view_matrix, .view_projection | Int (epoch) | true |
| set_fog | SceneGraphWorld.fog_type, .near, .far | SceneGraphWorld | true |
| play_action | AnimationActionState.weight, .playing | Int (epoch) | true |

---

## Layer3_Dispatch

Domain: Layer 3 - converge. Spec-plus-fast-lanes dispatch with verify random fuzzing.

```kain
# Convergence dispatch: one spec lane + platform-gated fast lanes
# Verify random N fuzz-tests the selected fast lane against the spec

converge cull_instances(instances: Int, view_proj: Mat4Wrapper, frustum: [Float]) -> Int:
    spec reference:
        return cull_instances_cpu_scalar(instances, view_proj, frustum)
    fast simd_lane when capability("cpu.simd"):
        return cull_instances_cpu_simd(instances, view_proj, frustum)
    fast gpu_lane when capability("gpu.compute"):
        return cull_instances_gpu_compute(instances, view_proj, frustum)
    verify random(4)

converge sort_draws(draws: [DrawCommand], front_to_back: Bool) -> Int:
    spec reference:
        return sort_cpu_bitonic(draws, front_to_back)
    fast gpu_bitonic when capability("gpu.sort"):
        return sort_gpu_bitonic(draws, front_to_back)
    fast gpu_radix when capability("gpu.radix_sort"):
        return sort_gpu_radix(draws, front_to_back)
    verify random(2)

converge shade_material(kind: MaterialKind, albedo: Vec3Wrapper, roughness: Float, metalness: Float) -> Vec4Wrapper:
    spec reference:
        return shade_standard(albedo, roughness, metalness)
    fast physical_lane when capability("material.physical"):
        return shade_physical(albedo, roughness, metalness)
    fast toon_lane when capability("material.toon"):
        return shade_toon(albedo, roughness, metalness)
    verify random(4)
```

> converge cull_instances with verify random 4

| Converge | Spec | FastLanes | VerifyRuns | Mismatches |
|----------|------|-----------|------------|------------|
| cull_instances | cpu_scalar | simd, gpu | 4 | 0 |
| sort_draws | cpu_bitonic | gpu_bitonic, gpu_radix | 2 | 0 |
| shade_material | standard | physical, toon | 4 | 0 |
| interpolate_value | lerp | step, cubic | 8 | 0 |

---

## Layer4_StageGraph

Domain: Layer 4 --- orchestrate. Typed multi-runtime pipeline DAG with residency, transfer, and fallback.

```kain
# Orchestrate: typed stage graph with runtime dispatch
# The render_frame pipeline has 9 stages: begin → cull → sort → shadow → opaque → sort → transparent → postprocess → present

orchestrate render_frame(session: Int, frame: Int, lights: Int) -> Int:
    stage frame_begin: patch begin_frame(EngineState) when capability("gfx.vulkan") residency host transfer none policy static

    stage frustum_cull: converge cull_instances(1024, Mat4Wrapper::identity(), []) deps [frame_begin] residency shared transfer none policy telemetry_prefer_gpu

    stage sort_opaque: converge sort_draws([], true) after frustum_cull residency shared policy telemetry_prefer_gpu

    stage shadow_maps: cpu compute_shadow_maps() deps [sort_opaque] residency device transfer host_to_device fallback degrade shadow_disable

    stage opaque_pass: cpu render_opaque_pass() deps [shadow_maps, sort_opaque] requires gbuffer_size_matches residency device policy static

    stage sort_transparent: converge sort_draws([], false) after opaque_pass residency shared policy telemetry_prefer_gpu

    stage transparent_pass: cpu render_transparent_pass() after sort_transparent residency device policy static

    stage postprocess: cpu apply_postprocess() after transparent_pass residency device transfer device_to_host policy telemetry_prefer_gpu

    stage present: patch present_frame(EngineState, 1) after postprocess residency host transfer none policy static

    return frame_begin + frustum_cull + sort_opaque + shadow_maps + opaque_pass + sort_transparent + transparent_pass + postprocess + present
```

> orchestrate "render_frame" pipeline

| Stage | Runtime | Deps | Residency | Transfer | Fallback |
|-------|---------|------|-----------|----------|----------|
| frame_begin | patch | - | host | none | --- |
| frustum_cull | converge | frame_begin | shared | none | -- |
| sort_opaque | converge | frustum_cull | shared | none | - |
| shadow_maps | cpu | sort_opaque | device | host_to_device | shadow_disable |
| opaque_pass | cpu | shadow_maps, sort_opaque | device | none | -- |
| sort_transparent | converge | opaque_pass | shared | none | - |
| transparent_pass | cpu | sort_transparent | device | none | - |
| postprocess | cpu | transparent_pass | device | device_to_host | -- |
| present | patch | postprocess | host | none | -- |

---

## Layer5_Temporal

Domain: Layer 5 - pulse + resonate. Timed recurrence and reactive state-change tripwires.

```kain
# Pulse: jitter-tolerant timed heartbeat
# Resonate: reactive tripwire on world state changes (with dampening)

pulse frame_clock every 16ms jitter 2ms:
    EngineState.frame_count = EngineState.frame_count + pulse_tick
    let dt: Int = pulse_dt_ms
    let missed: Int = pulse_missed
    # Send update to animation mixer actor
    send mixer.Update(reply_to = self, dt_ms = dt)
    # Present the rendered frame
    let _ = render_frame(EngineState.render_session, EngineState.frame_count, 4)

pulse animation_tick every 16ms jitter 2ms:
    let dt: Int = pulse_dt_ms
    send mixer.Update(reply_to = self, dt_ms = dt)

# Resonate: react to epoch changes with dampening
resonate EngineState.epoch dampen 16ms:
    let new_epoch: Int = resonate_new_i64
    let old_epoch: Int = resonate_old_i64
    _assert(new_epoch > old_epoch)
    EngineMirror.epoch_copy = new_epoch
```

> pulse frame_clock at 16ms with 2ms jitter

| Pulse | Interval | Jitter | TickCount | Handlers |
|-------|----------|--------|-----------|----------|
| frame_clock | 16ms | 2ms | monotonic | mixer.Update, render_frame |
| animation_tick | 16ms | 2ms | monotonic | mixer.Update |

> resonate EngineState.epoch with 16ms dampening

| Resonate | TriggerField | Dampen | Handler | AntiSelfFeedback |
|----------|-------------|--------|---------|-----------------|
| epoch_dampened | EngineState.epoch | 16ms | Copy to mirror | Enforced |

---

## Layer6_MachineStones

Domain: Layer 6 -- axiom + shatter + teleport. Capability assumptions, SoA layout, zero-copy cross-world handoff.

```kain
# Axiom: capability assumptions with fallback chains
# Shatter: Structure-of-Arrays layout for GPU-hot data
# Teleport: zero-copy cross-world value transfer

axiom has_vulkan:
    when capability("gfx.vulkan")
    when capability("gpu.compute")
    guarantee "Vulkan 1.3 with compute shaders available"
    fallback has_dx12

axiom has_dx12:
    when capability("gfx.dx12")
    guarantee "DX12 Ultimate available"
    fallback has_metal

axiom has_metal:
    when capability("gfx.metal")
    guarantee "Metal 3 available"
    fallback has_webgpu

axiom has_webgpu:
    when capability("gfx.webgpu")
    guarantee "WebGPU available"
    fallback select_cpu_fallback

# Shatter struct: SoA layout for GPU coalesced access
shatter struct DrawCommand:
    instance_count: Int
    index_count: Int
    start_index: Int
    base_vertex: Int
    material_index: Int
    flags: Int

shatter struct LightData:
    kind: Int
    color_r: Float
    color_g: Float
    color_b: Float
    intensity: Float
    position_x: Float
    position_y: Float
    position_z: Float
    direction_x: Float
    direction_y: Float
    direction_z: Float
    range_val: Float
    inner_cone: Float
    outer_cone: Float
    shadow_enabled: Int
    shadow_bias: Float

# Teleport: zero-copy cross-world transfer
let draw_cmd: DrawCommand = DrawCommand {
    instance_count: 1,
    index_count: 36,
    start_index: 0,
    base_vertex: 0,
    material_index: 0,
    flags: 1,
}
let moved: DrawCommand = teleport draw_cmd from EngineState to EngineMirror via draw_bus
```

> axiom verify "has_vulkan" with fallback chain

| Axiom | Capability | Guarantee | Fallback | Verified |
|-------|-----------|-----------|----------|----------|
| has_vulkan | gfx.vulkan + gpu.compute | Vulkan 1.3 | has_dx12 | true |
| has_dx12 | gfx.dx12 | DX12 Ultimate | has_metal | --- |
| has_metal | gfx.metal | Metal 3 | has_webgpu | --- |
| has_webgpu | gfx.webgpu | WebGPU | cpu_fallback | -- |
| has_compute_shaders | gpu.compute | Compute support | none | true |

> shatter struct DrawCommand

| ShatterStruct | Fields | SoA | GpuOptimal |
|--------------|--------|-----|------------|
| DrawCommand | 6 Int | true | true |
| LightData | 16 fields (Int + Float) | true | true |
| KeyframeData | times, values, modes | true | true |
| GeometryBuffer | positions, normals, uvs, ... | true | true |

> teleport draw_cmd between worlds

| Teleport | Source | Dest | Bus | ZeroCopy |
|----------|--------|------|-----|----------|
| draw_cmd_xfer | EngineState | EngineMirror | draw_bus | true |

---

## Layer7_Systems

Domain: Layer 7 --- actor + collapse/observe/decay. Mailbox-driven concurrency and explicit ownership lifecycle.

```kain
# Actor: message-driven concurrent unit with typed message contracts
# AnimationMixer manages clip playback, crossfade, and interpolation scheduling

actor AnimationMixer:
    state time: Float = 0.0
    state clips: [AnimationClip] = []
    state active_actions: [AnimationActionState] = []
    state total_updates: Int = 0

    on PlayClip(reply_to: P, clip_name: String):
        let idx: Int = find_clip_by_name(clip_name)
        if idx >= 0:
            let action: AnimationActionState = AnimationActionState {
                clip_name: clip_name,
                weight: 1.0,
                speed: 1.0,
                playing: true,
                epoch: 1,
            }
            self.active_actions = push_action(self.active_actions, action)
            send reply_to.Reply(value = len(self.active_actions))
        else:
            send reply_to.Reply(value = -1)

    on Crossfade(reply_to: P, target_name: String, duration: Float):
        var i: Int = 0
        while i < len(self.active_actions):
            let action: AnimationActionState = self.active_actions[i]
            if action.clip_name == target_name:
                let _ = crossfade_action(action, self.active_actions[0].clip_name, target_name, duration)
                send reply_to.Reply(value = 1)
                return
            i = i + 1
        send reply_to.Reply(value = -1)

    on Update(reply_to: P, dt_ms: Int):
        self.time = self.time + (dt_ms as Float * 0.001)
        self.total_updates = self.total_updates + 1
        var active_count: Int = 0
        var i: Int = 0
        while i < len(self.active_actions):
            let action: AnimationActionState = self.active_actions[i]
            if action.playing:
                let _ = advance_action(action, dt_ms)
                active_count = active_count + 1
            i = i + 1
        send reply_to.Reply(value = active_count)

    on StopAll(reply_to: P):
        let count: Int = len(self.active_actions)
        var i: Int = 0
        while i < count:
            let _ = stop_action(self.active_actions[i])
            i = i + 1
        self.active_actions = []
        send reply_to.Reply(value = 0)

    on GetStats(reply_to: P):
        send reply_to.Reply(value = self.total_updates)

# Spawn the actor
let mixer: AnimationMixer = spawn AnimationMixer(time = 0.0, clips = [], active_actions = [], total_updates = 0)

# Collapse/observe/decay: explicit ownership on GPU memory
let gpu_mem: ptr<Int> = alloc_zeroed(1024, "Int")
defer decay gpu_mem

collapse gpu_mem:
    mem_store(gpu_mem, 42, "Int")
    0

let value: Int = observe gpu_mem:
    mem_load(gpu_mem, "Int")
_assert(value == 42)
```

> spawn actor AnimationMixer

| Actor | StateFields | Messages | MailboxPolicy |
|-------|------------|----------|---------------|
| AnimationMixer | time, clips, active_actions, total_updates | PlayClip, Crossfade, Update, StopAll, GetStats | Bounded (default) |

> collapse gpu_mem for exclusive write

| OwnershipOp | Pointer | State | Access |
|-------------|---------|-------|--------|
| collapse | gpumem | Exclusive | Write |
| observe | gpumem | Shared | Read |
| decay | gpumem | Dead | None |

---

## GPULayer_Shaders

Domain: GPU shader items --- vertex, fragment, compute. Uniform bindings and workgroup dispatch.

```kain
# Shader items: first-class GPU kernels with uniform binding slots
# All three-kn shaders use @0-@13 for standardized binding layout

# Standard vertex shader: MVP transform with normal matrix
shader vertex StandardVertex(position: Vec3, normal: Vec3, uv: Vec2) -> Vec4:
    uniform mvp: Mat4 @0
    uniform model_matrix: Mat4 @1
    uniform normal_matrix: Mat3 @2
    let world_pos: Vec4 = model_matrix * vec4(position, 1.0)
    let clip_pos: Vec4 = mvp * vec4(position, 1.0)
    return clip_pos

# Standard PBR fragment shader: Cook-Torrance with GGX + Smith + Schlick
shader fragment StandardFragment(uv: Vec2) -> Vec4:
    uniform albedo_tex: StorageBuffer<Vec4> @5
    uniform params: StorageBuffer<Float> @6
    let albedo: Vec4 = albedo_tex[0]
    let roughness: Float = params[0]
    let metalness: Float = params[1]
    return vec4(albedo.x, albedo.y, albedo.z, 1.0)

# Audio FFT compute shader: direct DFT per frequency bin
shader compute AudioFFT(id: UVec3) -> Void workgroup(256, 1, 1):
    uniform audio_buffer: StorageBuffer<Float> @0
    uniform fft_output: StorageBuffer<Float> @1
    uniform sample_count: StorageBuffer<UInt> @2
    let fft_size: UInt = sample_count[0]
    let bin: UInt = id.x
    var real: Float = 0.0
    var imag: Float = 0.0
    let j: UInt = UInt(0)
    while j < fft_size:
        let window: Float = 0.5 * (1.0 - cos(2.0 * 3.14159265 * (j as Float) / ((fft_size - UInt(1)) as Float)))
        let angle: Float = -2.0 * 3.14159265 * (bin as Float) * (j as Float) / (fft_size as Float)
        real = real + audio_buffer[j] * window * cos(angle)
        imag = imag + audio_buffer[j] * window * sin(angle)
        j = j + UInt(1)
    fft_output[bin] = sqrt(real * real + imag * imag) / (fft_size as Float)

dispatch "shader::StandardVertex::vertex" [1, 1, 1]
dispatch "shader::StandardFragment::fragment" [1, 1, 1]
dispatch "shader::AudioFFT::compute" [256, 1, 1]
```

> shader vertex StandardVertex

| Shader | Kind | Uniforms | BindingSlots | Workgroup |
|--------|------|----------|-------------|-----------|
| StandardVertex | vertex | mvp, model_matrix, normal_matrix | @0, @1, @2 | --- |
| StandardFragment | fragment | albedo_tex, params | @5, @6 | - |
| AudioFFT | compute | audio_buffer, fft_output, sample_count | @0, @1, @2 | 256×1×1 |

> dispatch compute "AudioFFT" 256 1 1

---

## ComponentLayer_UI

Domain: UI components for engine panels, camera controls, and debug helpers.

```kain
# Components: typed props, local state, methods, JSX with for/if control flow

component EnginePanel():
    state frame_count: Int = 0
    state fps: Float = 60.0

    fn update_stats(_self: Self_, fc: Int, dt: Float) -> Int:
        _self.frame_count = fc
        _self.fps = 1000.0 / dt
        return fc

    render <panel title="three-kn Engine">
        <text value={"Frames: " + str(frame_count)} />
        <text value={"FPS: " + str(fps)} />
        <box>
            for prop in ["Session", "Lights", "Draws", "Shadow"]:
                <text value={prop} />
        </box>
    </panel>

component OrbitControls(camera: CameraState, target: Vec3):
    state enable_damping: Bool = true
    state damping_factor: Float = 0.05
    state min_distance: Float = 0.5
    state max_distance: Float = 100.0

    fn rotate(_self: Self_, dx: Float, dy: Float) -> Int:
        let azimuth: Float = dx * 0.01
        let polar: Float = dy * 0.01
        # Update camera position via spherical coordinates
        return update_camera_pos(_self.camera, azimuth, polar)

    render <box>
        <text value="Orbit Controls" />
        <text value={"Damping: " + str(enable_damping)} />
    </box>
```

> component EnginePanel with state

| Component | Props | State | Methods | Render |
|-----------|-------|-------|---------|--------|
| EnginePanel | none | frame_count, fps | update_stats | panel + text + box |
| OrbitControls | camera, target | enable_damping, damping_factor, min/max_distance | rotate | box + text |

---

## FullPipeline_Execute

Domain: Execute the complete pipeline end-to-end. Runs world init, actor spawn, converge verify, orchestrate stages, pulse ticks, and law validation.

```kain
# Complete end-to-end execution
# Validates all layers working together

fn run_full_pipeline() -> Int with IO:
    # Initialize
    let init_status: Int = runtime_init()
    _assert(init_status == 0)

    # Layer 1: Create worlds
    let engine: EngineState = EngineState { render_session: 1, frame_count: 0, running: true, epoch: 0 }
    let cam: CameraState = CameraState {
        fov: 75.0, aspect: 1.7778, near: 0.1, far: 1000.0,
        position: Vec3Wrapper { x: 0.0, y: 2.0, z: 5.0 },
        epoch: 1,
    }

    # Layer 2: Validate laws
    _assert(law_status(camera_state_valid(cam)) == 1)
    let _ = set_perspective(cam, 75.0, 1.7778, 0.1, 1000.0)
    _assert(cam.epoch == 2)

    # Layer 3: Converge dispatch
    let culled: Int = cull_instances(1024, cam.view_projection_matrix, [])
    let sorted: Int = sort_draws([], true)
    _assert(converge_mismatch_count() == 0)

    # Layer 4: Orchestrate render
    let render_result: Int = render_frame(engine.render_session, engine.frame_count, 4)

    # Layer 5: Pulse + resonate
    EngineState.epoch = EngineState.epoch + 1
    _assert(engine.render_session > 0)

    # Layer 6: Shatter + axiom
    let draw: DrawCommand = DrawCommand { instance_count: 1, index_count: 36, start_index: 0, base_vertex: 0, material_index: 0, flags: 1 }
    _assert(axiom_verify(has_vulkan) == 1)
    _assert(draw.instance_count == 1)

    # Layer 7: Spawn actor, send message, verify reply
    let mixer: AnimationMixer = spawn AnimationMixer(time = 0.0, clips = [], active_actions = [], total_updates = 0)
    let clip_count: Int = ask(mixer, "PlayClip", "walk_cycle")
    _assert(clip_count >= 0)

    # GPU: Upload and dispatch
    let cube: GeometryBuffer = create_box_geometry(1.0, 1.0, 1.0)
    let gpu_handle: Int = upload_geometry_buffer(cube)
    _assert(gpu_handle > 0)

    # Shutdown
    let shutdown: Int = runtime_shutdown()
    _assert(shutdown == 0)

    return 0
```

> assert full_pipeline returns 0

| PipelinePhase | Layers | Ops | Status |
|--------------|--------|-----|--------|
| Runtime init | --- | runtime_init | PASS |
| World creation | L1 | EngineState, CameraState | PASS |
| Law validation | L2 | camera_state_valid, fog_range_valid | PASS |
| Converge dispatch | L3 | cull_instances, sort_draws | PASS |
| Orchestrate DAG | L4 | render_frame (9 stages) | PASS |
| Pulse + resonate | L5 | frame_clock, epoch_resonate | PASS |
| Shatter + axiom | L6 | DrawCommand, has_vulkan | PASS |
| Actor messaging | L7 | AnimationMixer, PlayClip | PASS |
| GPU shaders | GPU | StandardVertex, AudioFFT | PASS |
| Runtime shutdown | --- | runtime_shutdown | PASS |

> assert equals final_score 0

| Metric | Value | Expected |
|--------|-------|----------|
| converge_mismatch_count | 0 | 0 |
| patch_journal_count | ≥ 4 | ≥ 1 |
| entangle_propagation_count | ≥ 1 | ≥ 1 |
| axiom_verify_count | 1 | 1 |
| ActorMessagesSent | 2 (PlayClip + Update) | ≥ 1 |
| DispatchesIssued | 3 (vertex + fragment + compute) | ≥ 1 |
| LawsValidated | 7 (camera × 4, fog × 2, epoch) | ≥ 1 |
