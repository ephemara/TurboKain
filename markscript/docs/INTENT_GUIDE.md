# 📖 MKS Intent Authoring Guide

> How to add new blockquote intent keywords to the Markscript runtime.
> Scale to hundreds or thousands -- the architecture is designed for it.

---

## Architecture (Why This Is Easy Now)

```
std/intents.md   ← YOU EDIT THIS FILE to add a new keyword
      │
      ├─▶ registry.kn          (loads keywords at startup)
      │      └─▶ parser.kn     (checks keywords during compilation)
      │
      └─▶ bridge.kn            (YOU ALSO EDIT: handler code + IVT registration)
             └─▶ dispatch_fn() (routes intent → handler function)
```

**The parser never changes.** `bridge.kn` changes only for new handler logic -- if your
new intent reuses an existing handler, you only touch `intents.md`.

---

## Quick Recipe: Adding a New Intent

### Step 1 -- Add Keyword to `std/intents.md`

Add one row to the table. Choose a **single lowercase word** as the keyword.

```diff
 | close      | handler_ui_on_close      | 74        | Handle UI close           |
+| encrypt    | handler_encrypt          | 99        | Encrypt a string          |
```

**Rules for keywords:**
- Single word, lowercase, no spaces (e.g., `encrypt` not `encrypt string`)
- Must NOT collide with any word in the prose-starter list (see Appendix)
- Must NOT be a Kain reserved keyword
- Handler ID must be unique - use the next available integer

### Step 2 - Register Handler in `bridge.kn`

Every handler requires **5 touchpoints** in `bridge.kn`. Walk through each:

#### 2a. Add function ID constant (`FN_*`)

```kn
pub const FN_ENCRYPT: Int = 99   // ← unique ID
```

#### 2b. Add to `BUILTIN_NAMES` and `BUILTIN_IDS` tables

```kn
const BUILTIN_NAMES: Array<String> = [
    ...
    "ui_create_widget",
    "encrypt_handler"         // ← function name string
]

const BUILTIN_IDS: Array<Int> = [
    ...
    FN_UI_CREATE_WIDGET,
    FN_ENCRYPT               // ← matching constant
]
```

#### 2c. Bump `REGISTRY_SIZE`

```kn
const REGISTRY_SIZE: Int = 66   // ← was 66, now 67
```

#### 2d. Register in IVT via `register_stdlib_handlers()`

```kn
pub fn register_stdlib_handlers(vm: MarkScriptVM) -> MarkScriptVM:
    var v = vm
    ...
    v = register_handler(v, hash_name("close"), FN_UI_ON_CLOSE)
    v = register_handler(v, hash_name("encrypt"), FN_ENCRYPT)   // ← single-word intent
```

#### 2e. Write handler function

```kn
fn handler_encrypt(vm: MarkScriptVM, args: Array<MarkValue>) -> HandlerResult:
    var input: String = ""
    if len(args) > 0:
        input = mark_value_to_string(args[0])
    if input == "":
        return HandlerResult { vm: vm, value: mark_string(""), err: "encrypt: no input" }

    // --- Your implementation ---
    var result: String = ""
    var i: Int = 0
    while i < len(input):
        let ch = text_substring_string(input, i, 1)
        let cv = text_ord(ch)
        // ROT13-style demo
        var shifted = cv + 13
        if shifted > 122:
            shifted = shifted - 26
        result = result + text_make_string(text_from_char(shifted))
        i = i + 1

    return HandlerResult { vm: vm, value: mark_string(result), err: "" }
```

#### 2f. Add dispatch branch in `dispatch_fn()`

```kn
pub fn dispatch_fn(vm: MarkScriptVM, fn_id: Int, args: Array<MarkValue>) -> HandlerResult:
    ...
    elif fn_id == FN_ENCRYPT:
        hr = handler_encrypt(vm, norm_args)
    ...
```

### Step 3 -- Rebuild and Verify

```bash
# Build
cd X:/blades/markscript
kain build

# Quick smoke test
./mks.exe eval '> encrypt "hello"'

# Full verification (use a test file)
./mks.exe run examples/verified/intent_registry_demo.md
```

---

## Verification Checklist (MANDATORY)

After adding any new intent, run through every item:

| # | Test | Command | Must See |
|---|------|---------|----------|
| 1 | **Build** | `kain build` | `Build succeeded` |
| 2 | **Eval dispatch** | `mks eval '> keyword arg'` | Registry loads, handler dispatches, result visible |
| 3 | **Prose guard** | `mks eval '> The quick brown fox'` | `Nothing to execute` (prose-starter blocks it) |
| 4 | **Unknown word** | `mks eval '> zzznonexistent arg'` | `Nothing to execute` (not in registry) |
| 5 | **Error path** | `mks eval '> keyword'` (no args) | Handler error message, no crash |
| 6 | **Test file** | Create a `.md` test in `examples/verified/` with `> keyword arg` | Clean dispatch |
| 7 | **Oracle** | `oracle launch mks.exe --args "eval '> keyword arg'"` | Process exits cleanly |
| 8 | **No regression** | `mks run examples/verified/full_stdlib_exercise.md` | All existing intents still work |

**⚠️ DO NOT skip any verification step.** Every intent must prove itself before merging.

---

## Prose-Starter Collision Warning

The parser has a built-in list of ~50 English sentence-starters (`The`, `In`, `However`, `Therefore`, etc.).
If your keyword collides with one, blockquotes starting with that word will be treated as prose
and **will never dispatch**.

**Current prose-starters you CANNOT use as intent keywords:**

```
The, This, That, These, Those, A, An, Some, Any, All,
Each, Every, One, No, Other, I, We, You, He, She, It, They,
In, At, On, By, From, To, With, For, As, So, Not, Just, Also,
And, But, Or, If, Because, However, Who, What, When, Where,
Why, Which, How, Then, Now, Here, There, Still,
Therefore, However, Meanwhile, Nevertheless,
Furthermore, Moreover, Thus, Hence
```

To check: after adding your keyword, run `mks eval '> YourKeyword test'` - if it dispatches, you're clear.

---

## Scaling Patterns

### Reusing Existing Handlers (no bridge.kn changes)

If your new intent does something an existing handler already does, just add the keyword:

```diff
 | close      | handler_ui_on_close      | 74        | Handle UI close           |
+| shutdown   | handler_ui_on_close      | 74        | Alias for close           |
```

Then register in `bridge.kn`'s `register_stdlib_handlers()`:
```kn
v = register_handler(v, hash_name("shutdown"), FN_UI_ON_CLOSE)
```

No new handler function needed. No new dispatch branch. No new constant.

### Adding Entire New Categories (5+ related handlers)

When adding a category (e.g., `encrypt`, `decrypt`, `sign`, `verify`, `hash`):

1. **Group them in `intents.md`** with a section comment:
   ```markdown
   ## Crypto
   | keyword    | handler_fn        | handler_id | description        |
   |------------|-------------------|-----------|--------------------|
   | encrypt    | handler_encrypt   | 99        | Encrypt a string   |
   | decrypt    | handler_decrypt   | 100       | Decrypt a string   |
   ```

2. **Group the handler constants** in `bridge.kn`:
   ```kn
   // --- EPSILON: Crypto handlers (99-103) ---
   pub const FN_ENCRYPT: Int = 99
   pub const FN_DECRYPT: Int = 100
   ```

3. **Create a verified example** in `examples/verified/crypto_demo.md`

---

## Quick Reference: File Touchpoints

| File | When You Edit It | What You Add |
|------|-----------------|-------------|
| **`std/intents.md`** | ALWAYS | One table row per keyword |
| **`src/bridge.kn`** | New handler logic needed | FN_* const, BUILTIN_NAMES row, BUILTIN_IDS row, REGISTRY_SIZE bump, IVT registration, handler fn, dispatch branch |
| **`src/parser.kn`** | **NEVER** | Nothing - data-driven, not code-driven |
| **`src/registry.kn`** | **NEVER** | Nothing -- loads whatever is in `intents.md` |
| **`src/main.kn`** | **NEVER** | Nothing - registry loading is automatic |

---

## Appendix: Current Intent Categories (57 keywords)

| Category | Handler IDs | Keywords |
|----------|-----------|----------|
| **File I/O** | 2-3, 33-37 | read, write, exists, mkdir, readdir, stat, touch, chmod |
| **String** | 13-21 | concat, split, join, substr, replace, upper, lower, trim, contains |
| **Math** | 22-30, 49-50 | sin, cos, sqrt, abs, min, max, clamp, random, randint, randfloat, randrange, randfrange, maybe, diceroll |
| **JSON** | 31-32 | parse, stringify |
| **Process** | 4-5, 38-40, 51-59 | run, spawn, await, kill, exitcode, stdout, stderr, pipe, env, cwd |
| **Time** | 41-43 | time, sleep |
| **Network** | 44-45 | template (render) |
| **UI** | 71-78 | click, key, focus, close, find, set, get, create |
| **Core** | 1, 6-12 | import, assert, print |
