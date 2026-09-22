# MarkScript JIT --- Native Code Compilation in Kain

> How to write a JIT compiler for MarkScript's bytecode VM using Kain's own semantic stack.
> Every construct needed exists today. No C required. No external JIT libraries.
> Kain compiles through LLVM. The JIT emits x86-64 machine code through raw memory writes.

---

## The Problem

The current VM is a bytecode interpreter:

```
while ip < bc_len:
    let opcode = bc[ip]
    if opcode == OP_PUSH_STACK: ...
    elif opcode == OP_ADD:       ...
    elif opcode == OP_JN:       ...
    # 17 more elif branches
```

Each dispatch: bounds check → indirect branch → stack push/pop → loop. Compiling through Kain's LLVM backend means every opcode goes through an interpreted `while` loop with nested `if/elif`. For a loop of 100 iterations, that's 100× the opcode dispatch overhead.

A JIT replaces this with direct native code: instead of interpreting `while limit > n: n = n + 1`, emit `cmp rcx, rdx; jge end; inc rcx; jmp loop`.

---

## The Kain Toolchain for a JIT

Kain has every construct needed to build a JIT compiler IN Kain. Here's the mapping:

| JIT Component | Kain Construct | Why |
|---------------|---------------|-----|
| **Fast-lane dispatch** | `converge` | Spec = interpreter, Fast = native code. `verify random(N)` fuzzes correctness |
| **Code cache** | `world` + `patch` | Compiler-owned state, journaled cache updates, telemetry |
| **Background compilation** | `actor` | `spawn JITWorker(...)`, `send worker.Compile(...)` -- concurrent JIT jobs |
| **Hot function detection** | `resonate` | Tripwire on execution counter, dampen to batch compiles |
| **Machine code emission** | `collapse`/`observe`/`decay` | Allocate RWX memory, write bytes, execute. Raw pointer safety with ownership state machine |
| **Compilation pipeline** | `orchestrate` | Trace capture → emit → law check → cache commit - typed stage graph |
| **Code cache layout** | `shatter struct` | SoA layout for hot-path vs cold-path separation |
| **Tests** | `converge verify random(N)` | Fuzz JIT output against interpreter --- guaranteed correctness |
| **Safety gates** | `law` | Invariant checks on emitted code (bounds, alignment, no relocations) |
| **Startup timing** | `pulse` | Schedule JIT compilation budget across frame budgets |
| **Cross-world handoff** | `teleport` | Transfer compiled code from JIT world to execution world |

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     MarkScript VM                                │
│                                                                  │
│  converge execute_block(vm, bc, ip) -> ExecResult:               │
│    spec reference:                                               │
│        return interpret_block(vm, bc, ip)    ← interpreter       │
│    fast native_code when capability("jit.enabled"):              │
│        let native = lookup_cache(hash)                           │
│        if is_valid(native):                                      │
│            return run_native(vm, native.ptr)   ← JIT fast lane   │
│        return interpret_block(vm, bc, ip)       ← fallback       │
│    verify random(64)                                             │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                     JIT Subsystem (written in Kain)              │
│                                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │ Counter     │  │ JITWorker    │  │ CodeCache              │  │
│  │ Resonate    │─▶│ Actor        │─▶│ World                  │  │
│  │ (hot detect)│  │ (compile)    │  │ (stored native code)   │  │
│  └─────────────┘  └──────┬───────┘  └────────────────────────┘  │
│                          │                                       │
│                    ┌──────▼────────────────────────────────┐     │
│                    │  orchestrate jit_compile_pipeline      │     │
│                    │  stage 1: trace capture (cpu)          │     │
│                    │  stage 2: code emission (cpu + Unsafe) │     │
│                    │  stage 3: law validation (law)         │     │
│                    │  stage 4: cache commit (patch)         │     │
│                    └───────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Component 1: Converge Dispatch -- Interpreter vs Native

The `converge` block is the JIT's dispatch mechanism. The interpreter is the `spec` reference lane. JIT-compiled native code is a `fast` lane. The `verify random(N)` clause fuzz-tests the JIT output against the interpreter --- any mismatch is caught at verify-time.

```kain
converge execute_block(vm: ptr<MarkScriptVM>, bc: Array<Int>, ip: Int) -> ExecResult:
    spec reference:
        return interpret_block(vm, bc, ip)

    fast native_code when capability("jit.enabled"):
        let hash = block_signature(bc, ip)
        let cached = lookup_cache(CodeAuthority, hash)
        if cached.is_valid:
            let result = run_native(vm, cached.code_ptr, cached.stack_depth)
            return result
        // Not compiled yet - fall through to interpreter
        return interpret_block(vm, bc, ip)

    verify random(64)
```

**How `verify random(N)` works for JIT:** The runtime generates 64 random bytecode snippets, runs both the interpreter lane and the native-code lane, and compares results. Any mismatch increments `converge_mismatch_count()`. The operator or CI tooling alerts on non-zero mismatch counts -- this is the canary that the JIT has a correctness bug.

---

## Component 2: Hot Function Detection via Resonate

A `resonate` handler on the execution counter world field triggers JIT compilation when a function crosses the hot threshold.

```kain
world CodeAuthority:
    state execution_counter: Array<Int>   // per-block-hash counter
    state counter_epoch:     Int = 0
    state hot_threshold:     Int = 100    // compile after N executions
    state pending_compiles:  Int = 0

// When a counter crosses the threshold, a resonating actor
// picks up the compile job
resonate CodeAuthority.counter_epoch dampen 16ms:
    // Scan counters, find hot blocks, spawn compilation
    // The scan is batched - dampen 16ms prevents storming
    let new_threshold = CodeAuthority.hot_threshold
    // ... spawn JITWorker for each hot block
```

---

## Component 3: Background JIT Compilation via Actor

Each compilation job runs in a dedicated actor. The actor receives the bytecode trace, compiles it to machine code, registers it in the cache, and replies to the caller.

```kain
actor JITWorker:
    state worker_id: Int
    state compiles_done: Int = 0

    on Compile(reply_to: P, block_hash: Int, bytecode: Array<Int>, stack_depth: Int):
        self.compiles_done = self.compiles_done + 1

        // 1. Emit native code (raw memory ops, Unsafe effect)
        let result = emit_native_block(bytecode, stack_depth)

        // 2. Validate emitted code
        if result.error != "":
            send reply_to.CompileFailed(hash = block_hash, error = result.error)
            return

        // 3. Register in code cache via patch
        let entry_ptr = patch_register_code(CodeAuthority, block_hash, result)

        // 4. Reply with status
        send reply_to.Compiled(hash = block_hash, code_ptr = entry_ptr)
```

---

## Component 4: Machine Code Emission via Collapse/Decay

This is where Kain's ownership semantics shine. Raw memory is managed through `collapse` (exclusive write), `observe` (read-only), and `decay` (deterministic teardown). The emitted code is written byte-by-byte to an executable buffer.

```kain
fn emit_native_block(bytecode: Array<Int>, stack_depth: Int) -> EmitResult with Unsafe:
    let estimated_size = estimate_code_size(bytecode, stack_depth)

    // Allocate executable memory (RWX)
    let code_buf: ptr<Byte> = platform_alloc_executable(estimated_size)
    if code_buf == null:
        return EmitResult { error: "allocation failed" }

    // Exclusive mutation: write machine code to the buffer
    collapse code_buf:
        var emit_ip: Int = 0          // write position in native buffer
        var bc_ip: Int = 0            // read position in bytecode
        let bc_len = len(bytecode)

        // Emit function prologue: push rbp; mov rbp, rsp; sub rsp, stack_frame
        emit_prologue(code_buf, emit_ip, stack_depth)
        emit_ip = emit_ip + prologue_size

        while bc_ip < bc_len:
            let op = bytecode[bc_ip]

            if op == OP_PUSH_STACK:
                let operand = bytecode[bc_ip + 1]
                // Emit: mov rax, operand; push rax
                emit_push_imm(code_buf, emit_ip, operand)
                bc_ip = bc_ip + 2
                emit_ip = emit_ip + push_imm_size

            elif op == OP_ADD:
                // Emit: pop rax; pop rbx; add rax, rbx; push rax
                emit_add(code_buf, emit_ip)
                bc_ip = bc_ip + 1
                emit_ip = emit_ip + add_size

            elif op == OP_STORE_VAR:
                let name_hash = bytecode[bc_ip + 1]
                // Emit: pop rax; mov [var_table + hash_offset], rax
                emit_store_var(code_buf, emit_ip, find_var_offset(name_hash))
                bc_ip = bc_ip + 2
                emit_ip = emit_ip + store_var_size

            elif op == OP_LOAD_VAR:
                let name_hash = bytecode[bc_ip + 1]
                emit_load_var(code_buf, emit_ip, find_var_offset(name_hash))
                bc_ip = bc_ip + 2
                emit_ip = emit_ip + load_var_size

            elif op == OP_JN:
                let target = bytecode[bc_ip + 1]
                // Emit: pop rax; test rax, rax; jns +next; jmp target
                emit_jn(code_buf, emit_ip, resolve_offset(bc_ip, target, emit_ip))
                bc_ip = bc_ip + 2
                emit_ip = emit_ip + jn_size

            elif op == OP_HALT:
                // Emit function epilogue
                emit_epilogue(code_buf, emit_ip)
                bc_ip = bc_ip + 1
                emit_ip = emit_ip + epilogue_size

            else:
                // Unsupported op --- emit interpreter callout
                emit_interp_fallback(code_buf, emit_ip, op)
                bc_ip = bc_ip + bytecode_op_length(op)
                emit_ip = emit_ip + interp_callout_size

        // Flush instruction cache (required for JIT on x86)
        platform_flush_icache(code_buf, emit_ip)

        // Return the buffer via collapse expression value
        (code_buf, emit_ip)   // pointer + actual size

    // Read-only verification of the emitted code
    let valid = observe code_buf:
        verify_emitted_code(code_buf, estimated_size)

    // Teardown on failure, keep on success
    if valid == false:
        decay code_buf
        return EmitResult { error: "verification failed" }

    return EmitResult { code_ptr: code_buf, size: estimated_size, error: "" }
```

**Key properties:**
- `collapse code_buf:` ensures exclusive write access during code emission
- `observe code_buf:` provides read-only verification after emission
- `decay code_buf:` is the deterministic teardown path for failed compilations
- If no error, the pointer escapes to the code cache -- the ownership transfers to the cache world
- `platform_alloc_executable` and `platform_flush_icache` are FFI calls to `mmap`/`VirtualAlloc` and `__clear_cache`/`FlushInstructionCache`

---

## Component 5: Orchestrate Pipeline for JIT Compilation

The orchestrate block structures the JIT compilation as a typed, verifiable stage graph.

```kain
orchestrate jit_compile(block_hash: Int, bytecode: Array<Int>, stack_depth: Int) -> CodeCacheEntry:
    // Stage 1: Trace analysis + memory allocation
    stage analyze: cpu analyze_trace(bytecode, stack_depth)
        when capability("cpu.scalar")
        residency host
        policy telemetry_prefer_cpu

    // Stage 2: Machine code emission (raw memory writes)
    stage emit: cpu emit_native_block(bytecode, stack_depth)
        deps [analyze]
        residency host
        policy telemetry_balance_latency

    // Stage 3: Invariant validation on emitted code
    stage validate: law emitted_code_valid(emit.code_ptr, emit.size)
        after emit
        residency host
        policy static

    // Stage 4: Register in code cache
    stage cache: patch patch_register_code(CodeAuthority, block_hash, emit.code_ptr, emit.size)
        deps [emit]
        requires validate
        residency host
        policy static

    return CodeCacheEntry {
        hash: block_hash,
        code_ptr: emit.code_ptr,
        size: emit.size
    }
```

**What the pipeline guarantees:**
- `deps [analyze]` --- analysis completes before emission starts
- `law emitted_code_valid(...)` --- the emitted code passes structural validation before it enters the cache
- `requires validate` -- the cache stage won't execute if validation fails
- `residency host` --- all stages run on CPU (machine code emission is a CPU task)
- The pipeline is self-documenting: any engineer can read the stages and understand the compilation flow

---

## Component 6: Code Cache via World + Patch

The code cache is a `world` with `patch` for journaled updates. Patches are atomic and recorded in the patch journal for telemetry.

```kain
world CodeAuthority:
    state cache_entries:  Array<CodeCacheEntry>  // compiled native blocks
    state cache_bytes:    Int = 0                // total allocated bytes
    state max_cache:      Int = 1048576          // 1MB limit
    state compile_count:  Int = 0                // total compilations
    state evict_count:    Int = 0                // cache evictions

    // Surface for monitoring JIT health
    surface native_ui => JITDashboard

shatter struct CodeCacheEntry:
    block_hash:  Int             // signature of the bytecode basic block
    code_ptr:    ptr<Byte>       // pointer to emitted native code
    code_size:   Int             // size in bytes
    exec_count:  Int             // how many times it's been executed
    stack_depth: Int             // required native stack depth

// Patch to register compiled code
patch patch_register_code(world: CodeAuthority, hash: Int, ptr: ptr<Byte>, size: Int) -> Int:
    // Evict if cache is full
    if world.cache_bytes + size > world.max_cache:
        // Simple FIFO eviction - real version uses LRU/hotness
        let evicted = world.cache_entries[0]
        platform_free_executable(evicted.code_ptr, evicted.code_size)
        world.cache_bytes = world.cache_bytes - evicted.code_size
        world.evict_count = world.evict_count + 1
        // Shift cache entries (or use circular buffer)
        var i: Int = 1
        while i < len(world.cache_entries):
            world.cache_entries[i - 1] = world.cache_entries[i]
            i = i + 1
        pop(world.cache_entries)

    // Append new entry
    push(world.cache_entries, CodeCacheEntry {
        block_hash: hash,
        code_ptr: ptr,
        code_size: size,
        exec_count: 0,
        stack_depth: estimate_stack_depth(size)
    })
    world.cache_bytes = world.cache_bytes + size
    world.compile_count = world.compile_count + 1
    return len(world.cache_entries) - 1
```

---

## Component 7: Running Native Code

Once code is emitted and cached, the `converge` fast lane needs to call it. This uses Kain's FFI or raw function pointer dispatch:

```kain
// Native code calling convention:
// Arguments: VM state pointer, bytecode array handle
// Returns: ExecResult fields in registers/stack

type JITFunction = fn(vm: ptr<MarkScriptVM>, stack_base: ptr<MarkValue>) -> Int

fn run_native(vm: ptr<MarkScriptVM>, code_ptr: ptr<Byte>) -> ExecResult with Unsafe:
    // Cast the code buffer to a function pointer and call it
    // (asm wrapper handles ABI: save callee-saved regs, set up stack frame)
    let fn_ptr: ptr<JITFunction> = code_ptr as ptr<JITFunction>
    let result = fn_ptr(vm, vm.stack_base)
    return unpack_exec_result(result, vm)
```

The native code expects:
- `rdi` = pointer to VM struct (or key fields)
- `rsi` = pointer to stack base
- Returns exit condition in `rax`

The native emit generates:
```
push rbp
mov rbp, rsp
sub rsp, stack_frame

; ... body: inlined bytecode operations ...

; Epilogue
mov rsp, rbp
pop rbp
ret
```

Each opcode is lowered directly to x86-64:
| Bytecode | Native (x86-64) |
|----------|----------------|
| `PUSH_STACK imm` | `mov rax, imm; push rax` |
| `ADD` | `pop rax; pop rbx; add rax, rbx; push rax` |
| `LOAD_VAR hash` | `mov rax, [vm.var_base + offset]; push rax` |
| `STORE_VAR hash` | `pop rax; mov [vm.var_base + offset], rax` |
| `JN target` | `pop rax; test rax, rax; jns .next; jmp .target` |
| `JMP target` | `jmp .target` |
| `EXECUTE_CALL` | `call handler_dispatch_stub` (bridges back to IVT) |

---

## Testing the JIT: Converge's Verify Random(N)

The `verify random(N)` clause in `execute_block` is the JIT's test harness. It works like this:

```kain
// During converge lane verification:
// 1. Generate a random bytecode snippet (valid but unpredictable)
// 2. Run the interpreter lane → get result A
// 3. Run the JIT native lane → get result B
// 4. If A != B: increment converge_mismatch_count()
// 5. Generate next random snippet, repeat N times
```

For the JIT, this means:
- **Every `verify random(64)` tests 64 random bytecode sequences**
- Any codegen bug in the x86-64 emitter produces a mismatch
- `converge_mismatch_count()` is the health metric --- zero means the JIT matches the interpreter
- The random sequences exercise edge cases: loops with bound=0, deeply nested arithmetic, variable shadowing, overflow conditions

```kain
// In a benchmark or CI test:
fn jit_correctness_test(iterations: Int) -> Int:
    let mismatches = converge_mismatch_count()
    if mismatches > 0:
        println("JIT MISMATCH: " + str(mismatches) + " cases differ from interpreter")
        return -1
    println("JIT verified: " + str(iterations) + " random traces match interpreter")
    return 0
```

---

## What You'd Learn Building This

1. **The `converge` construct is literally designed for this** - spec vs fast-lane dispatch with fuzz verification. The JIT is a textbook case of converge.

2. **Raw memory management in Kain (`collapse`/`observe`/`decay`) is exactly what you need for machine code emission.** No C `malloc`/`free`, no manual error cleanup, no use-after-free. The ownership state machine catches OBOs and double-frees at compile time.

3. **`orchestrate` is for more than GPU pipelines.** The JIT compilation pipeline (trace → analyze → emit → validate → cache) is a natural `orchestrate` graph with typed dependency tracking.

4. **`actor` gives you concurrent compilation for free.** No thread pools, no mutexes, no channels. JIT workers are actors; the runtime handles scheduling.

5. **`resonate` is the right way to detect hot functions.** Instead of polling counters, `resonate` fires the moment a counter hits the threshold - no polling overhead when the function isn't hot.

---

## Current Limitations

| Gap | Workaround | Future |
|-----|------------|--------|
| No `mmap`/`VirtualAlloc` with `PAGE_EXECUTE_READWRITE` in stdlib | `include <sys/mman.h>` or `<windows.h>` via C FFI | Would need `std::mem::alloc_executable` |
| No `memcpy` for code copying | `include <string.h>` via C FFI | Would need `std::mem::copy` |
| JIT calling convention not standardized | Hand-rolled asm stub | Would need `fn` attribute for native ABI |
| `ptr<fn()>` calling not fully tested | Verified in ownership + teleport benchmarks | Already proven in `fusion_chain.kn` --- lowering exists |

None of these are semantic blockers. The C FFI (`include <sys/mman.h> as mmap`) handles OS memory operations, and Kain's `collapse`/`observe`/`decay` handles the safety around the emitted code.

---

## Summary

The MarkScript JIT would be:
- **~200 lines of Kain** for the converge dispatch, actor workers, and orchestrate pipeline
- **~500 lines of Kain** for the x86-64 code emitter (opcode → native translation table)
- **~200 lines of Kain** for the world/patch cache, resonate hot detector, and pulse compilation budget
- **~100 lines of C FFI** for `mmap`/`VirtualAlloc` and `FlushInstructionCache`

Total: ~1000 lines of Kain. Every line authored in the decision ladder.
No C. No LLVM pass. No external JIT library. Just Kain semantics.
