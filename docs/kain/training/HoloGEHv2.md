╔══════════════════════════════════════════════════════════════════════════════╗
║  HOLOGEH v2 — KAIN SPEC  │  105kw · 65 stdlib · 185 errors               ║
║                                                                          ║
║  CHAIN-OF-THOUGHT RULE (mandatory):                                      ║
║  Before writing ANY Kain code, output: // INTENT: [lattice chain]         ║
║  EX: // INTENT: UI event → resonate → patch world → entangle mirror      ║
║  EX: // INTENT: pulse tick → converge dispatch → teleport to GPU          ║
║  This forces architecture planning using Kain's vocabulary.               ║
║                                                                          ║
║  Read order: self-index → lattice → grid → master exemplar → cli         ║
║  Every construct: SYNTAX // EX: // NOT: (inline, single-line)            ║
╚══════════════════════════════════════════════════════════════════════════════╝

// ─── SELF-INDEX ───
// L1 ATH: world,entangle,surface  |  L2 INT: patch,law
// L3 DSP: converge  |  L4 STG: orchestrate
// L5 TMP: pulse,resonate  |  L6 MCH: axiom,shatter,teleport
// L7 SYS: actor,collapse,observe,decay,share,fanout,weak
// UI: component,render,state  |  GPU: shader(v/f/c),uniform,workgroup,dispatch,comptime
// FGN: include(C),import(Python),@extern,@link_name,@callconv,@naked
// CTM: macro!,comptime,const  |  EFF: Pure,IO,GPU,Async,Reactive,Unsafe,with
// TST: test,async,await  |  (emit,receive reserved)
// L0: standard control flow — fn,let,mut,if,elif,else,match,for,while,loop,break,continue,return,defer,struct,enum,trait,impl,use,mod,pub,self,Self,type,where,as,and,or,true,false,none,var,const,test,async,await
//   (Same semantics as Rust/Zig; : instead of {} around blocks. NO ++/--. Struct literal SUPPORTED: let p=Point{x:1,y:2})

// ─── DECISION LATTICE ─── READ FIRST. ───
// global state→world  |  sync fields→entangle  |  bind world→surface
// journaled mutation→patch  |  invariant(Bool)→law  |  platform dispatch→converge
// multi-runtime pipeline→orchestrate  |  timed recurring→pulse
// reactive tripwire→resonate  |  capability+fallback→axiom  |  SoA layout→shatter
// zero-copy cross-world→teleport  |  concurrent entity→actor
// exclusive raw write→collapse  |  read-only scope→observe
// terminal teardown→decay  |  parallel lanes→share/fanout  |  non-owning alias→weak
// UI widget→component+render  |  GPU kernel→shader(v/f/c)  |  binding→uniform@N
// host launch→dispatch  |  C/OS→include<h>as a  |  Python→import
// code gen→macro!  |  compile eval→comptime  |  const→const
// Pure→noIO  |  IO→file/net  |  Async→futures  |  GPU→compute
// Reactive→UIevents  |  Unsafe→rawmem/asm/ABI  |  block cleanup→defer
// C ABI→@extern/@link_name/@callconv  |  test→test
// fallback→fn,let,if,match,struct,enum,trait,impl

// ─── CONSTRUCT GRID (L1-L7 + UI + GPU + FGN + CTM) ───
// L#CAT|kw       | SYNTAX // EX: // NOT:
//──────┼─────────┼────────────────────────────────────────────────────────────
L1 ATH | world      | world N: state f:T=init / surface K=>C // world App: state cnt:Int=0 / surface native_ui=>Panel // NOT: var global
L1 ATH | entangle   | entangle W1.f <-> W2.f with single_writer // ALSO: entangle from W1.f to W2.f with single_writer // Auth.signal<->Mir.signal_copy // NOT: manual sync
L1 ATH | surface    | surface native_ui/web/shader_canvas/viewport3d => Comp // native_ui=>App // NOT: two same-kind on one world
L2 INT | patch      | patch n(w:W,p)->T: w.f=v // set_sig(a:Auth,v:Int)->Int: a.signal=v // NOT: fn writes world field directly
L2 INT | law        | law n(p)->Bool: return BoolExpr // valid(v:Int)->Bool: v>=0 and v<M // NOT: if-check in fn for invariant
L3 DSP | converge   | converge n(p)->T: spec ref: b / fast L when G: b / verify r(N) // fmix(v,s) // NOT: #[cfg] for platform
L4 STG | orchestrate| orch n(p)->T: stage N: kind fn(a) clauses / ret e // clauses: when,after,deps[..],residency,transfer,guarded by,fallback,requires,policy // kinds: cpu,gpu,converge,law,patch,world,dispatch,c,python,rust,node,kain // NOT: fn calls when stage metadata matters
L5 TMP | pulse      | pulse n every Nms jitter Mms: body // locals: pulse_tick,pulse_dt_ms,pulse_missed // tele: runtime_machine_pulse_total_fire_count() // NOT: while+sleep
L5 TMP | resonate   | resonate W.f dampen Nms: body // locals: resonate_new/old_i64,resonate_fired // tele: resonate_fire_count() // fires AFTER patch, BEFORE entangle. No self-trigger. // NOT: polling loop for change
L6 MCH | axiom      | axiom n: when p(v) / guarantee"s" / fallback f // preds: target,arch,capability // machine_truth: target("llvm"),arch("x86_64"),cap("memory.shatter") // NOT: comment for capability
L6 MCH | shatter    | shatter struct N: f:T // SoA per-field lane // Particle: x:Float/y:Float/vx:Float/vy:Float/alive:Bool // NOT: regular struct for hot lane data
L6 MCH | teleport   | teleport e from Src to Dst via ch // zero-copy destructive. Src MOVED. // tele: runtime_machine_teleport_count() // NOT: copy for cross-world
L7 SYS | actor      | actor N: state f:T=init / on M(reply_to:P,p): / send reply_to.Reply(v) // spawn: h=spawn N(f=v) // ask: r=ask(h,"M",pack(v,s)) blocks 30s // mailbox: bounded(1024)/unbounded, Block/DropNewest/Oldest/FailSender // lifecycle: UNINIT→INIT→RUNNING→SHUTDOWN→TERMINATED/FAILED // supervision: OneForOne/All/Rest/S1O1 + Perm/Temp/Trans // NOT: raw thread for msg-passing
L7 SYS | collapse   | collapse p: body // exclusive write. no return/break/continue. // c: mem_store(ptr_offset(c,i,"T"),v) // NOT: raw mem_store
L7 SYS | observe    | observe p: body // read-only. no mem_store. // c: s+=mem_load(ptr_offset(c,i,"T")) // NOT: raw pointer read
L7 SYS | decay      | decay p // terminal. p DEAD. Heap→FreeHeap, Alloca→LifetimeEnd, Imported→LifetimeEnd // NOT: manual free
L7 SYS | share/fanot| share p: fanout v in r: body // parallel disjoint writes // cnt: fanout w in 0..4: atomic_add(cnt,1,"acq_rel") // NOT: manual threading
L7 SYS | weak       | weak alias = p // non-owning. DO NOT decay. // w:ptr<Int>=raw // NOT: decaying weak alias
UI CMP | component  | component N(p): state f:T=init / render<JSX/> // C(v:Int): state c=v / render<box><text/></box> // NOT: fn returning UI
UI CMP | render     | render <Tag a={e}>ch</Tag> // JSX. for/if inside. Tag Uppercase. // <VStack spacing=8><Button/></VStack> // NOT: lowercase tag
UI CMP | state      | state n:T=init // persists frames. vtable 8/9(i64),19/20(f64),21/22(str) // NOT: let inside render
// Widgets: Button,Label,TextInput,Slider,Toggle,Checkbox,ProgressBar,Spinner
// Layout: HStack,VStack,ZStack,Grid,ScrollView,Spacer,Padding,Divider
// Primitives: box,text,panel,RoundedRect,Circle,Image,GradientRect,InteractiveArea
// Events(slot23): on_click,change,focus,blur,mouseenter,mouseleave,submit,cancel
// 24-slot vtable: 0=session_create,1=destroy,2=element_begin,3=end,4=set_text,5=attr_i64,6=attr_f64,7=attr_string,8/9=state_i64,10=begin_frame,11=end_frame,12=present,13=poll_event,14=should_close,15=window_open,16=host_pump,17=attach_platform,18=get_gpu_extension,19/20=state_f64,21/22=state_string,23=element_set_callback
GPU SHD | shader     | shader<kind>N(p)->R[wg(W,H,D)]: uniform T@N / body // kinds: vertex,fragment,compute,mesh,task,raygen,anyhit,closesthit,miss,intersection,callable // compute K(id:UVec3)->Void wg(8,8,1): uniform src:StorageBuffer<Float>@0 // NOT: CPU loop for GPU work
GPU SHD | uniform    | uniform N: T @N // T: StorageBuffer<T>(RW),Sampler2D,SamplerState,Vec4,Mat4,Float,Int,UInt,Bool // LOCAL_SIZE_X/Y/Z = compile const // NOT: hardcoded @N
GPU SHD | workgroup  | workgroup(W,H,D) after return type on compute // LOCAL thread group. NOT dispatch grid.
GPU SHD | dispatch   | dispatch"key"[X,Y,Z] // with GPU,Unsafe. Indirect: dispatch"key"from buf // X/Y/Z = workgroup counts
GPU SHD | comptime   | comptime: let compute=(wg,dispatch,tensors,streams,nodes[,spec_constants]) // shader metadata DSL. AST-matched. NOT interpreted.
FGN INT | include    | include<h>as a / include"p/h"as a // libclang. System(angle),Local(quoted)+comp.c // Tiers:Dynamic(DLL),Static(link),Inline(bitcode) // Versioned: include<sqlite3.h>3.45.0 as sql // NOT: use c::module(deprecated)
FGN INT | import     | import m as a / from m import n // Python obj. Named args→kwargs // GIL: python_region_begin/end // Tensor: kain_tensor_from_py(s/owned) // GPU: python_gpu_storage_buffer(t,n)→StorageBuffer // NOT: py_eval all
FGN INT | @extern    | @extern fn n(p)->T / @link_name("sym") / @callconv("win64"/"sysv64"/"stdcall"/"vectorcall") // @naked=no prologue @section("name")=custom section // NOT: manual C wrappers
COM CTM | macro!     | macro n!(p:kind): body // kinds: expr,type,ident,block,token // ! MANDATORY // fold!(x:expr): mod(x,M) // NOT: fn for syntax gen
COM CTM | comptime   | comptime: block / comptime: expr // module: bake AST. expr→literal. // NOT: runtime for compile-known
COM CTM | const      | const N:T=val // inline-folded. NOT interpreted like comptime.
EFF CTX | with       | fn n()->T with E: // lattice: Pure<IO<Async<GPU/Reactive<Unsafe // Pure=noIO, Unsafe=top // KNOWN GAPS: dispatch not GPU-gated. mem ops not Unsafe-gated.

// ─── TELEMETRY ─── (runtime counters proving each construct fired)
// entangle→propagation_count()  |  patch→journal_count()  |  law→status(valid)
// resonate→fire_count()  |  converge→mismatch_count(==0=ok)  |  orch→stage_count()
// teleport→machine_teleport_count()  |  pulse→machine_pulse_total_fire_count()
// actor→scheduler_queue_depth()  |  world→runtime_world_field_count(name)

// ─── ANTIPATTERNS ───
// var global→world  |  struct for state→world  |  fn writes global→patch
// if-check invariant→law  |  #[cfg]→converge  |  while+sleep→pulse
// poll for change→resonate  |  copy for xfer→teleport  |  manual free→decay
// ++/--→+=1  |  one world→decompose  |  world w/o epoch→add epoch  |  Cargo→Bazel

// ─── MASTER EXEMPLAR ─── (~45 lines)  Sensor Dashboard: UI + Actor + Compute + State
// Combines L1-L7 in ONE causal chain. Read from bottom up for architecture flow.
// Demonstrates how layers COMPOSE — this is the core test of LLM understanding.

// L1-L2: World owns state, patch mutates, law guards, entangle syncs
world SensorWorld: state raw:Int=0 / state filtered:Int=0 / state alert:Bool=false / state epoch:Int=0 / surface native_ui=>Dashboard
world DisplayWorld: state display_val:Int=0 / state alert_led:Bool=false
entangle SensorWorld.filtered<->DisplayWorld.display_val with single_writer
law in_range(v:Int)->Bool: return v>=0 and v<1000
patch ingest(w:SensorWorld,v:Int)->Int: w.raw=v; if in_range(v): w.filtered=v; w.epoch++

// L3-L4: Converge selects platform-optimized filter, orchestrate pipelines it
converge adaptive_filter(v:Int)->Int:
  spec reference: (v*31+7)%1000
  fast simd when cap("cpu.x86.avx2"): (v*53+11)%1000
  verify random(4)
orchestrate process_pipe(v:Int,e:Int)->Int:
  stage h:cpu adaptive_filter(v+e) residency host
  stage check:law in_range(h) residency host guarded by law(in_range)
  return check

// L5: Pulse drives sampling clock, resonate reacts to threshold breaches
pulse sample_clock every 16ms jitter 2ms: SensorWorld.raw = (SensorWorld.raw + pulse_tick*7) % 1000
resonate SensorWorld.filtered dampen 50ms:
  SensorWorld.alert = resonate_new_i64 > 900
  DisplayWorld.alert_led = SensorWorld.alert

// L7: Actor backgrounds heavy processing, teleports result
actor DataWorker: state buf:Int=0
  on Process(reply_to:P,val:Int):
    let mut cells:ptr<Int> = alloc_zeroed(4,"Int")
    collapse cells: for i in 0..4: mem_store(ptr_offset(cells,i,"Int"),val+i*val)
    let sum:Int = observe cells: var s=0; for j in 0..4: s+=mem_load(ptr_offset(cells,j,"Int")); s
    decay cells
    send reply_to.Reply(value=sum%1000)

// L7: share/fanout for parallel reduce
fn parallel_reduce(data:ptr<Int>,n:Int)->Int:
  let mut result:ptr<Int> = alloc_zeroed(1,"Int")
  share result: fanout w in 0..4: // 4 parallel workers
    var acc=0; var i=w*n/4; while i<(w+1)*n/4: acc+=mem_load(ptr_offset(data,i,"Int")); i+=1
    atomic_add(result,acc,"acq_rel")
  let r=observe result: mem_load(result,"Int"); decay result; r

// UI: Component renders dashboard, bound to world via surface
component Dashboard():
  render <VStack spacing=8>
    <text value={"Raw: "+SensorWorld.raw}/>
    <text value={"Filtered: "+SensorWorld.filtered}/>
    <box fill_color={if SensorWorld.alert:"#FF0000" else:"#00FF00"} width=20 height=20/>
    <Button label="Reset" on_click={fn(): patch ingest(SensorWorld,0)}/>
  </VStack>

// fn main ties it all together: init → pulse → converge → actor → teleport → shutdown
fn main()->Int: let r=runtime_init(); if r!=0: return r
  let h=spawn DataWorker(buf=0)
  // pulse runs automatically; converge, actor, teleport in causal chain
  let actor_v=ask(h,"Process",pack(42,SensorWorld.epoch))
  teleport actor_v from SensorWorld to DisplayWorld via result_bus
  let ok=patch_journal_count()>0 and resonate_fire_count()>0
  runtime_shutdown(); if !ok: return 1; return 0

// ─── ERRORS ─── (18 families, 185+ codes)
// BORROW(10):ownership/alias  |  CODEGEN(11):backend  |  ACTOR(8):spawn/mailbox
// COMPTIME(10):macro/law/axiom  |  CONVERGE(8):spec/fast  |  EFFECT(12):annotation
// ENTANGLE(7):cycle/writer  |  WORLD(8):surface/orphan  |  IO(6):file/net
// MEM(8):null/OOB/layout  |  PATCH(7):law/pre/post  |  RUNTIME(8):panic/deadlock
// SHADER(12):stage/uniform  |  STATE(8):cycle/transition  |  TEST(7):assertion/seed
// TYPE(26):ident/trait/return/mutability/missing

// ─── STDLIB (Kain-specific API signatures only) ───
// runtime: init()->Int / shutdown()->Int / heap_validate()->Int
//   cpu_feature_mask()->Int / cpu_has_capability(k:String)->Int
//   machine_teleport_count()->Int / machine_pulse_total_fire_count()->Int
//   simd_dot_scalar/avx2/avx512_mod(a,b,cells,bias,mod)->Int
// intent: entangle_propagation_count()->Int / patch_journal_count()->Int / law_status(Bool)->Int
//   resonate_fire_count()->Int / converge_mismatch_count()->Int
//   orchestrate_stage_count()->Int / converge_choose_int(spec,fast)->Int
// actor: spawn(name:String,payload:String)->Int / send(id,msg,data)->Int / id_is_valid/run/terminal/state
//   registry_lookup/register/has / monitor/link/unlink
//   scheduler_queue/max/enqueued/dequeued/worker/active/busy/depth
// sync: mcs_mutex_new/lock/unlock / teleport_channel_new/send/recv
//   once_new/do/complete / wait_group_new/add/done/wait
//   rwlock_new/read/write / semaphore_new/acquire/release / condvar_new/wait/notify
// gpu: memory_policy(5) / resource_policy / binding_plan / storage/uniform_buffer_binding
//   shared_buffer/zeroed_from_bytes / shared_image/zeroed_from_bytes
//   backend_state/preferred / std140_vec3/4/mat4 / std430_vec3a / cbuffer_mat4
// graphics: session_create/destroy / backend_supported/select / begin/end_frame/present
//   buffer_create / shader_spirv_from_hex / mesh/pipeline_create / draw_mesh
// machine: lfence/sfence/mfence / cpuid_eax/ebx/ecx/edx / rdtsc / cache_flush / prefetch
//   vm_reserve/commit/decommit/protect/lock/map/map_huge / popcount/clz/ctz/rotl/rotr/bswap
//   atomic_raw_load/store/exchange/CAS/fetch_add/sub/wait/notify_one/all
//   bump_create/alloc/destroy / arena_create/alloc/destroy / pool_create/alloc/free/destroy
//   i64x4: splat/lane/replace/add/sub/mul/and/or/xor/blend/dot/hsum/gather/scatter
//   mcs_mutex/rwlock/semaphore/wait_group/once / thread_spawn/join/yield/affinity/name
//   volatile_load/store_int / mmio_field_get/set/w1c / asm("i",args,constraints,clobbers)
//   os_syscall0-6 / os_mmap/munmap/mprotect/make_rw/rx/rwx/madvise/msync/mlock/munlock
// ui: session_create/destroy / element_begin/end / set_text / attr_i64/f64/string
//   state_i64/f64/string g/s / begin/end_frame / present / poll_event / should_close
//   window_open / host_pump / get_gpu_extension / element_set_callback
//   ui_fb_ptr/width/height/stride / native_ui_node_*/reconcile/focus/dirty
//   native_ui_draw_rect/text/resource/gradient / font_create/destroy/measure/line_height
// python: region_begin/end / region_import/getattr/call_raw_f64_trunc_i64/buffer_view
//   tensor_from_py(shared/owned) / image_from_py(shared/owned) / gpu_storage_buffer
//   py_call/async/future_state/done/await / actor_callback/close/delivered
// time: now_millis()->Int / sleep_millis(Int)->Int / duration/instant/deadline/ticker types
// math: Vec2/3/4, Mat2/3/4, Quat, noise, intersections — pure (250 symbols)
// collections: ArrayList, HashMap, SlotMap, PriorityQueue (110 symbols)
// text: TextSlice, StringView, trim, split, join (59)
// fmt: FmtWriter, int/float/bool/hex formatting (76)
// json: parse/serialize (133) | fs: open/read/write/walk/watch (148)
// os: env/mmap/syscall (127) | process: fork/exec/pipe/PTY (63)
// http(44)/net(58)/tls(11)/mcp(73) | input(45):kb/mouse/gamepad
// cuda(93):CUDA/PTX dispatch | wasm(18)/no_std:target

// ─── CLI COMMANDS ─── (kain <cmd>)
// check <f> [--json] [--target T]  |  typecheck only // EX: kain check src/main.kn --json
// build native-ui <f> [--app-name N] [--release]  |  build native UI app
// run <f> [--target T] [-g/--debug] [-- <args>]  |  compile+link+execute // kain run src/main.kn --target llvm
// run dev <f>  |  watch+rerun  |  run plan <f> [--json]  |  print plan
// test <f> [--mode check-pass|run-pass] [--json] [--fail-fast]  |  compiletest tests
// doctor [--repair] [--profile safe|aggressive]  |  binary/build diagnostics
// fmt <files> [--check] [-w]  |  formatting  |  clean [--scope all]  |  artifacts
// repl  |  interactive  |  watch <f>  |  rerun on change
// init [path] [--name N]  |  scaffold project
// add <pkg> [--version V] / install / publish  |  capsule packaging
// amalgamate <input> -o OUT [--archive] [--contents src|snap|assets|artifacts|evidence]  |  pack sources
// amalgamate inspect <input> [--json] / unpack <input> [-o DIR]
// import platform <pkg> [--sdk PATH]  |  native SDK via libclang // kain import platform vulkan
// import-c <input> -I inc -D def -o FILE  |  C source  |  import-crate <name> [--mode live|gen]
// gpu-artifacts <input> -o PATH [--target all|spirv|cuda|hlsl|wgsl]  |  compile shaders
// config show [--json] / config set <k> <v>  |  commands list/export/help
// runtime build [--release] / validate  |  build native runtime
// bridge serve --entry <f>  |  JSON-lines bridge  |  omni init|build  |  fabric init|val|run
// stdlib-map [--write] [--check]  |  gen atlas  |  codebase inspect|run
// selfhost bootstrap (deprecated)  |  lsp (stub, deprecated)
// ALL BUILDS: `bazel build //:kain --config=dev` + `kain_sync_binary`. NEVER CARGO.

// ─── LIFECYCLE ───
// runtime_init() = call FIRST in main(). runtime_shutdown() = call LAST before return. Both return Int (0=ok).
// kain check = typecheck only (no runtime needed). kain build --target llvm = .ll→clang→.exe.
// WSL: set KAIN_CLANG_PATH + KAIN_RUNTIME_MANIFEST_PATH + KAIN_HOME.
// Oracle verification (MANDATORY after any .exe build): oracle scan→launch→debug→matrix→verify→delta

// ═══════════════════════════════════════════════════════════════════════════════
// END HOLOGEH v2  |  ~180 lines  |  ~4,500 tokens  |  1 master exemplar (45 lines, L1-L7 fused)
// ═══════════════════════════════════════════════════════════════════════════════
