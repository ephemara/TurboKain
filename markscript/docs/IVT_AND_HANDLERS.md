# IVT & Handlers -- The Intent Dispatch System

> The Intent Vector Table is the bridge between MarkScript prose and Kain execution.

---

## How Dispatch Works

```
.md source → lex → parse → OP_PUSH_PARAM(phrase_hash) → OP_EXECUTE_CALL
                                                               │
                                                               ▼
                                                   IVT lookup by phrase_hash
                                                               │
                                                   ┌───────────┴───────────┐
                                                   │ found                  │ not found
                                                   ▼                        ▼
                                         call handler(args)         NAME_ERROR
                                         return value to VM
```

## Built-in Handlers (12)

| ID | Handler | Intent Pattern | Kain Bridge |
|----|---------|---------------|-------------|
| 1 | `FN_FS_READ_TEXT` | `> read file "path"` | `std::fs::fs_read_text()` |
| 2 | `FN_FS_WRITE_TEXT` | `> write file "path" "content"` | `std::fs::fs_write_text()` |
| 3 | `FN_FS_EXISTS` | `> file exists "path"` | `std::fs::fs_path_exists()` |
| 4 | `FN_PROCESS_OUTPUT` | `> run "command"` | `std::process::process_spawn()` |
| 5 | `FN_PROCESS_SPAWN` | `> spawn "command"` | Full process API |
| 6 | `FN_IMPORT_KAIN` | `> import kain "module"` | Kain module loader |
| 7 | `FN_ASSERT` | `> assert value expected` | Equality check, error on mismatch |
| 8 | `FN_PRINTLN` | `> print value` | `println(str(value))` |
| 9 | `FN_STR` | Implicit in mini-language | `str()` value-to-string |
| 10 | `FN_LEN` | Implicit in mini-language | `len()` container size |
| 11 | `FN_PUSH` | Internal | Push value to VM stack |
| 12 | `FN_POP` | Internal | Pop value from VM stack |

## Handler Signature

Every handler is a Kain function with this shape:

```kain
fn my_handler(vm: MarkScriptVM, args: Array<MarkValue>) -> HandlerResult:
    // Process args, access stdlib, return result
    return HandlerResult {
        vm: vm,
        value: mark_int(42),
        err: "",
    }
```

Where:

```
struct MarkValue:
    kind:       Int     // MARK_INT, MARK_FLOAT, MARK_STRING, MARK_TABLE, MARK_CODE
    int_val:    Int
    float_val:  Float
    str_val:    String

struct HandlerResult:
    vm:     MarkScriptVM   // updated VM state
    value:  MarkValue      // result value
    err:    String         // empty = success, non-empty = error
```

## Adding a Custom Handler

### 1. Add a Function ID Constant

In `bridge.kn`:

```kain
pub const FN_MY_CUSTOM: Int = 13
```

### 2. Write the Handler Function

```kain
fn handler_custom_fn(vm: MarkScriptVM, args: Array<MarkValue>) -> HandlerResult:
    // Validate args
    if len(args) < 1:
        return HandlerResult { vm: vm, value: mark_int(0), err: "missing argument" }
    // Do work
    let input = args[0]
    let result = do_something(input.int_val)
    return HandlerResult { vm: vm, value: mark_int(result), err: "" }
```

### 3. Add an Elif Branch in `dispatch_fn()`

```kain
elif fn_id == FN_MY_CUSTOM:
    hr = handler_custom_fn(vm, args)
```

### 4. Register the Intent Mapping

In `init_vm_with_builtins()`:

```kain
let vm = register_handler(vm, hash("my command"), FN_MY_CUSTOM)
```

### 5. Use It

```markdown
> my command 42
```

## Did-You-Mean Hints

When an IVT lookup fails, the error engine searches all registered handler phrases for the closest match (edit distance ≤ 3):

```markdown
> apply graviti
# → Error: name error: unknown intent "apply graviti"
#   suggestion: did you mean "apply gravity"?
```

This works automatically -- no configuration needed. The error engine compares the failed hash against all registered phrase hashes.

## Handler Registration Flow

```
init_vm_with_builtins()
  │
  ├─ register_handler(vm, hash("print"), FN_PRINTLN)
  ├─ register_handler(vm, hash("read file"), FN_FS_READ_TEXT)
  ├─ register_handler(vm, hash("write file"), FN_FS_WRITE_TEXT)
  ├─ register_handler(vm, hash("file exists"), FN_FS_EXISTS)
  ├─ register_handler(vm, hash("run"), FN_PROCESS_OUTPUT)
  ├─ register_handler(vm, hash("spawn"), FN_PROCESS_SPAWN)
  ├─ register_handler(vm, hash("import kain"), FN_IMPORT_KAIN)
  ├─ register_handler(vm, hash("assert"), FN_ASSERT)
  │
  └─ ... custom handlers registered here
```

The IVT is stored in the VM as `Array<IVTEntry>`:

```kain
struct IVTEntry:
    phrase_hash: Int
    handler_id:  Int
```

## Handler Dispatch Loop

At runtime, `execute_bytecode()` returns with `handler_id > 0` when it encounters an `OP_EXECUTE_CALL`. The main loop in `main.kn` handles the dispatch:

```
execute_bytecode → handler_id > 0
    → extract args from VM stack
    → dispatch_fn(vm, handler_id, args)
    → resume_execution(vm, bc, handler_result)
    → loop until handler_id == 0
```

This decouples markdown scripts from implementation. Domain experts write intents. Engineers write IVT handlers.
