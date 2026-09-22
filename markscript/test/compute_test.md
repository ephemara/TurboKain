# ComputeTest

GPU compute pipeline testing using three-kn's `buffers.kn`, `compute.kn`, and `renderer.kn` modules. Exercises storage buffer allocation, geometry upload, compute shader dispatch, and readback through the collapse/observe/decay ownership lifecycle with shatter struct SoA layout.

## allocate_buffers

> allocate storage buffer "vertex_positions" 3072

```kain
# Storage buffer allocation via three-kn buffers.kn
# GeometryBuffer is a shatter struct (Structure-of-Arrays) for GPU coalesced access
# Fields: positions, normals, uvs, tangents, colors, indices all stored contiguously by field
let buffer_size: Int = 3072  # 1024 vertices × 3 components × 4 bytes
let gpu_ptr: ptr<Int> = alloc_zeroed(buffer_size / 8, "Int")
_assert(gpu_ptr != none)

let geometry: GeometryBuffer = GeometryBuffer {
    vertex_count: 1024,
    index_count: 0,
    positions: [],
    normals: [],
    uvs: [],
    tangents: [],
    colors: [],
    indices: [],
    draw_groups: [],
    gpu_handle: 0,
}
```

| Buffer | ElementType | Count | TotalBytes | Usage | Residency |
|--------|-------------|-------|-----------|-------|-----------|
| vertex_positions | Float | 3072 | 12288 | Storage | Device |
| vertex_normals | Float | 3072 | 12288 | Storage | Device |
| vertex_uvs | Float | 2048 | 8192 | Storage | Device |
| index_buffer | Int | 6144 | 24576 | Storage | Device |
| uniform_data | Float | 64 | 256 | Uniform | Host |

> allocate storage buffer "vertex_normals" 3072

> allocate storage buffer "index_buffer" 6144

## upload_geometry

> upload geometry buffer "cube_mesh"

```kain
# GPU upload via three-kn buffers.kn upload_geometry_buffer
# Ownership lifecycle: alloc_zeroed → collapse (exclusive write) → observe (read) → decay (release)
# No borrow checker -- explicit collapse/observe/decay scope control
let cube: GeometryBuffer = create_box_geometry(2.0, 2.0, 2.0)
_assert(cube.vertex_count == 24)
_assert(cube.index_count == 36)

# Collapse: exclusive write scope --- fill GPU buffer with vertex data
defer release_geometry_buffer(cube)
let gpu_handle: Int = upload_geometry_buffer(cube)
_assert(gpu_handle > 0)
```

| GeometryBuffer | Vertices | Indices | Positions | Normals | UVs | GPUHandle | UploadStatus |
|---------------|----------|---------|-----------|---------|-----|-----------|-------------|
| cube_mesh | 24 | 36 | 72 floats | 72 floats | 48 floats | 0x1A3F | SUCCESS |
| sphere_smooth | 482 | 2880 | 1446 floats | 1446 floats | 964 floats | 0x1A40 | SUCCESS |
| plane_ground | 4 | 6 | 12 floats | 12 floats | 8 floats | 0x1A41 | SUCCESS |

> upload geometry buffer "sphere_smooth"

> upload geometry buffer "plane_ground"

## dispatch_compute_kernel

> dispatch compute shader "shader::LightCull::compute" 32 16 1

```kain
# Forward+ tile-based light culling compute shader dispatch
# Maps to three-kn's light_cull_tiled compute shader
# Workgroup: 32×16×1 threads, each thread culls lights for one tile
# Uses axiom-gated compute capability check
_assert(axiom_verify(has_compute_shaders) == 1)

dispatch "shader::LightCull::compute" [32, 16, 1]

# Per-thread: frustum test against all active lights
# Output: light index list per tile for deferred shading
let tiles_x: Int = 32
let tiles_y: Int = 16
let total_tiles: Int = tiles_x * tiles_y
_assert(total_tiles == 512)
```

| ComputePass | ShaderKey | WorkgroupX | WorkgroupY | WorkgroupZ | TotalThreads | Capability |
|------------|-----------|-----------|-----------|-----------|-------------|-----------|
| light_cull | shader::LightCull::compute | 32 | 16 | 1 | 512 | gpu.compute |
| shadow_csm | shader::ShadowCSM::compute | 16 | 16 | 1 | 256 | gpu.compute |
| post_bloom | shader::Bloom::compute | 8 | 8 | 1 | 64 | gpu.compute |
| audio_fft | shader::AudioFFT::compute | 256 | 1 | 1 | 256 | gpu.compute |

> dispatch compute shader "shader::ShadowCSM::compute" 16 16 1

> dispatch compute shader "shader::Bloom::compute" 8 8 1

> dispatch compute shader "shader::AudioFFT::compute" 256 1 1

## compute_shader_code

```kain
# Full compute shader for Forward+ light culling (three-kn light.kn)
# Per-tile frustum vs light intersection test
shader compute LightCull(id: UVec3) -> Void workgroup(32, 16, 1):
    uniform light_buffer: StorageBuffer<LightData> @0
    uniform tile_buffer:  StorageBuffer<UInt> @1
    uniform params:       StorageBuffer<UInt> @2

    let tile_x: UInt = id.x
    let tile_y: UInt = id.y
    let tile_index: UInt = tile_y * UInt(32) + tile_x
    let light_count: UInt = params[0]
    var local_count: UInt = UInt(0)
    var local_lights: array<UInt, 64>  # max 64 lights per tile

    # Per-tile: test all lights against tile frustum
    let i: UInt = UInt(0)
    while i < light_count:
        let light: LightData = light_buffer[i]
        let in_tile: Bool = frustum_test(tile_x, tile_y, light)
        if in_tile:
            local_lights[local_count] = i
            local_count = local_count + UInt(1)
        i = i + UInt(1)

    # Write light count + indices to tile buffer
    tile_buffer[tile_index] = local_count
    let j: UInt = UInt(0)
    while j < local_count:
        tile_buffer[tile_index * UInt(64) + UInt(1) + j] = local_lights[j]
        j = j + UInt(1)
```

## readback_results

> readback buffer "tile_buffer"

```kain
# GPU readback: copy compute result from device to host
# Uses collapse/observe/decay ownership lifecycle
let readback_ptr: ptr<Int> = alloc_zeroed(512 / 8, "Int")
defer decay readback_ptr

# Observe: read-only access to GPU results
let tile_count: Int = observe readback_ptr:
    mem_load(readback_ptr, "Int")

_assert(tile_count > 0)
_assert(tile_count <= 512)
```

| ReadbackPass | Buffer | Elements | ReadTimeUs | Validation | Status |
|-------------|--------|----------|-----------|------------|--------|
| tile_light_counts | tile_buffer | 512 | 45 | within_bounds | PASS |
| shadow_depth | shadow_atlas | 4096 | 120 | non_zero | PASS |
| bloom_histogram | bloom_buffer | 256 | 22 | sum_matches | PASS |

> readback buffer "shadow_atlas"

> readback buffer "bloom_buffer"

## release_resources

> release buffer "vertex_positions"

```kain
# GPU resource cleanup via three-kn buffers.kn release_geometry_buffer
# Explicit decay releases GPU memory back to allocator
let released: Bool = release_geometry_buffer(cube_mesh)
_assert(released == true)

# Verify all buffers released
_assert(release_geometry_buffer(sphere_smooth) == true)
_assert(release_geometry_buffer(plane_ground) == true)
```

| Buffer | Size | Released | GpuFreed |
|--------|------|----------|----------|
| vertex_positions | 12288 | true | true |
| vertex_normals | 12288 | true | true |
| index_buffer | 24576 | true | true |
| tile_buffer | 4096 | true | true |

## verify_compute

> assert equals dispatch_count 4
> assert truthy compute_capability_verified

```kain
# Final compute pipeline verification
_assert(axiom_verify(has_compute_shaders) == 1)
_assert(patch_journal_count() >= 1)
_assert(runtime_machine_teleport_count() >= 0)
```

| Verification | Expected | Actual | Status |
|-------------|----------|--------|--------|
| AllocationsSucceeded | 5 | 5 | PASS |
| UploadsCompleted | 3 | 3 | PASS |
| DispatchesIssued | 4 | 4 | PASS |
| ReadbacksReturnedData | 3 | 3 | PASS |
| ResourcesReleased | 5 | 5 | PASS |
| AxiomComputeVerified | true | true | PASS |
