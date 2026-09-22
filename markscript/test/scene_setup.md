# SceneSetup

Scene construction, camera configuration, geometry creation, lighting, fog, and render target setup for the three-kn 3D engine. All intents bridge to three-kn's `camera.kn`, `scene_graph.kn`, `light.kn`, `buffers.kn`, `texture.kn` worlds and patches via the IVT handler registry.

## create_scene

> create scene "main_scene"
> set background color 0.12 0.12 0.14
> begin graphics session

| Property | Value | Notes |
|----------|-------|-------|
| SceneName | main_scene | Primary render scene |
| BackgroundR | 0.12 | Linear sRGB |
| BackgroundG | 0.12 | Linear sRGB |
| BackgroundB | 0.14 | Linear sRGB |
| EnableFog | true | Exponential fog |
| GraphicsSession | active | Initiated via begin graphics session |

## setup_camera

> create perspective camera "main_camera"
> set camera position 0.0 5.0 10.0
> build view matrix 0.0 5.0 10.0 0.0 0.0 0.0

```kain
# Perspective camera via three-kn camera.kn camera_state_valid law
# FOV: 75° (standard game FOV)
# Near clip: 0.1 units
# Far clip: 1000.0 units
# Aspect: 16:9 derived from viewport
let cam: CameraState = CameraState {
    projection_type: ProjectionKind::Perspective,
    fov: 75.0,
    aspect: 1.7778,
    near: 0.1,
    far: 1000.0,
    position: Vec3Wrapper { x: 0.0, y: 5.0, z: 10.0 },
    target: Vec3Wrapper { x: 0.0, y: 0.0, z: 0.0 },
    up: Vec3Wrapper { x: 0.0, y: 1.0, z: 0.0 },
    epoch: 1,
}
let _ = set_perspective(cam, 75.0, 1.7778, 0.1, 1000.0)
let _ = update_view(cam)
let law_status = law_status(camera_state_valid(cam))
_assert(law_status == 1)
```

> set camera "main_camera" as active

| Camera CameraState | FOV | Near | Far | Position | Target |
|--------------------|-----|------|-----|----------|--------|
| main_camera | 75.0 | 0.1 | 1000.0 | (0, 5, 10) | (0, 0, 0) |

## create_geometry

> create box geometry "cube_main" 2.0 2.0 2.0

```kain
# Box geometry via three-kn buffers.kn create_box_geometry
# Produces 24 vertices with normals + UVs.
# The GeometryBuffer is a shatter struct (SoA layout) for GPU-optimal access.
let cube: GeometryBuffer = create_box_geometry(2.0, 2.0, 2.0)
let vertex_count: Int = cube.get_vertex_count()
let index_count: Int  = cube.get_index_count()
_assert(vertex_count == 24)
_assert(index_count == 36)
let byte_len: Int = cube.gpu_byte_length()
_assert(byte_len > 0)
```

> create sphere geometry "sphere_smooth" 1.5 32 24

| Geometry | Type | Width | Height | Depth | Radius | SegW | SegH | Vertices | Indices |
|----------|------|-------|--------|-------|--------|------|------|----------|---------|
| cube_main | Box | 2.0 | 2.0 | 2.0 | -- | --- | - | 24 | 36 |
| sphere_smooth | Sphere | - | -- | - | 1.5 | 32 | 24 | - | --- |
| plane_ground | Plane | 20.0 | 20.0 | --- | - | -- | -- | --- | - |

> create plane geometry "plane_ground" 20.0 20.0

| PlaneParams | Width | Height | Orientation |
|-------------|-------|--------|-------------|
| plane_ground | 20.0 | 20.0 | XZ (Y-up) |

## setup_lights

> create ambient light "ambient_sky"

| AmbientLight | Color_R | Color_G | Color_B | Intensity |
|-------------|---------|---------|---------|-----------|
| ambient_sky | 0.4 | 0.4 | 0.5 | 0.6 |

> create directional light "sun_main"

```kain
# Directional light via three-kn light.kn create_directional_light
# Intensity is in physical units (lux-equivalent for PBR)
let sun: LightDef = create_directional_light(
    Vec3Wrapper { x: 1.0, y: 1.0, z: 0.0 },
    Vec3Wrapper { x: 1.0, y: 0.95, z: 0.9 },
    2.0,
)
_assert(sun.kind == LightKind::Directional)
_assert(sun.intensity == 2.0)
let _ = render_directional_shadow_maps()
```

| DirectionalLight | Position | Direction | Color | Intensity | ShadowMap |
|------------------|----------|-----------|-------|-----------|-----------|
| sun_main | (50, 50, 0) | (-0.577, -0.577, -0.577) | (1.0, 0.95, 0.9) | 2.0 | 2048×2048 |

> create point light "lantern_point"

| PointLight | Position | Color | Intensity | Range | Decay |
|-----------|----------|-------|-----------|-------|-------|
| lantern_point | (2.0, 1.0, 3.0) | (1.0, 0.7, 0.3) | 1.5 | 10.0 | 2.0 |

> create spot light "flashlight"

| SpotLight | Position | Direction | Color | Intensity | InnerCone | OuterCone | Range |
|-----------|----------|-----------|-------|-----------|-----------|-----------|-------|
| flashlight | (0.0, 1.5, 0.0) | (0, -1, 0) | (0.9, 0.9, 1.0) | 3.0 | 0.3 | 0.6 | 15.0 |

> create hemisphere light "sky_dome"

| HemisphereLight | Sky_R | Sky_G | Sky_B | Ground_R | Ground_G | Ground_B | Intensity |
|----------------|-------|-------|-------|----------|----------|----------|-----------|
| sky_dome | 0.6 | 0.7 | 1.0 | 0.3 | 0.2 | 0.1 | 0.8 |

## setup_fog

> set scene fog 0.01 20.0

```kain
# Fog via three-kn scene_graph.kn set_fog patch
# Exponential fog: density = 0.01, far limit = 20.0
# Laws enforce fog_near >= 0 and fog_far > fog_near
let sg: SceneGraphWorld = SceneGraphWorld {
    max_nodes: 1024,
    epoch: 0,
    fog_type: 1,  # 0 = none, 1 = exponential, 2 = linear
    fog_near: 0.01,
    fog_far: 20.0,
    fog_color: Vec3Wrapper { x: 0.55, y: 0.55, z: 0.6 },
}
let _ = set_fog(sg, 1, 0.01, 20.0)
_assert(law_status(fog_range_valid(sg)) == 1)
```

| FogConfig | FogType | Density | FarLimit | Color_R | Color_G | Color_B |
|-----------|---------|---------|----------|---------|---------|---------|
| scene_fog | Exponential | 0.01 | 20.0 | 0.55 | 0.55 | 0.6 |

## create_render_targets

> init render targets 1920 1080

```kain
# HDR render target via three-kn texture.kn create_render_target
# 1920×1080, RGBA16F format for HDR pipeline, 4x MSAA
let tex: TextureCreateInfo = TextureCreateInfo {
    width: 1920,
    height: 1080,
    depth: 1,
    format: 15,  # RGBA16F
    mip_levels: 1,
    sample_count: 4,
    kind: TextureKind::RenderTarget,
    usage: 0x0E,  # color + depth + resolve
}
let hdr_id: Int = create_render_target()
let depth_id: Int = create_depth_texture()
_assert(hdr_id > 0)
_assert(depth_id > 0)
```

> create render target "hdr_color"
> create render target "depth_buffer"
> create render target "bloom_ping"
> create render target "bloom_pong"

| RenderTarget | Width | Height | Format | Samples | HDR | DepthStencil |
|-------------|-------|--------|--------|---------|-----|-------------|
| hdr_color | 1920 | 1080 | RGBA16F | 4 | true | false |
| depth_buffer | 1920 | 1080 | D32F | 4 | false | true |
| bloom_ping | 960 | 540 | RGBA16F | 1 | true | false |
| bloom_pong | 960 | 540 | RGBA16F | 1 | true | false |

## verify_scene_setup

> assert equals vertex_count 24
> assert equals index_count 36
> assert truthy light_count_valid
> assert truthy gbuffer_size_matches

```kain
# Final scene verification
# All laws must pass: camera, light, texture, renderer
_assert(law_status(camera_state_valid(cam)) == 1)
_assert(law_status(fog_range_valid(sg)) == 1)
_assert(law_status(light_count_valid(LightState)) == 1)
```

| Verification | Status | Expected | Notes |
|-------------|--------|----------|-------|
| CameraLaws | PASS | all valid | FOV, near/far, aspect |
| FogLaws | PASS | fog_near valid | Range ordering |
| LightCount | PASS | ≤ max | 4 lights created |
| RenderTargets | PASS | 4 created | HDR + depth + bloom |
| GeometryUpload | PASS | 3 buffers | Box + sphere + plane |
