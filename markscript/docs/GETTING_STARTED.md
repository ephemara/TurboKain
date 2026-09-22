# MarkScript - Getting Started

> Build, run, and write your first MarkScript program in 2 minutes.

## 1. Build the VM

```bash
cd blades/markscript
kain build          # typecheck + LLVM compile + native link → mks.exe
```

Output: `mks.exe` in `blades/markscript/`.

## 2. Run Your First Script

```bash
mks run examples/game_engine.md
mks run examples/fizzbuzz.md
mks run README.md   # yes, this README compiles
```

## 3. Write a Script

Create a `.md` file:

```markdown
# MyProject

## setup
> print "hello world"

| Item | Count |
|------|-------|
| A    | 42    |
| B    | 99    |
```

Run it:

```bash
mks run my_script.md
```

## 4. Validate Without Executing

```bash
mks check my_script.md
# → CHECK PASSED --- N bytecode ops, 0 errors
```

## 5. Debug Bytecode

```bash
mks disasm my_script.md
# → OP_ENTER_DOMAIN hash=...
# → OP_ROUTINE_HEADER hash=...
# → OP_PUSH_PARAM hash=...
# → OP_EXECUTE_CALL
# → OP_PUSH_MATRIX handle=0...
```

## 6. Next Steps

| Guide | What You'll Learn |
|-------|-------------------|
| `AUTHORING_GUIDE.md` | Full language reference |
| `CLI_REFERENCE.md` | Every subcommand and flag |
| `IVT_AND_HANDLERS.md` | The intent dispatch system |
| `POSSIBILITIES.md` | What you can build |

## Quick Reference

| Construct | Syntax | Bytecode |
|-----------|--------|----------|
| Domain | `# Name` | `OP_ENTER_DOMAIN` |
| Routine | `## Name` | `OP_ROUTINE_HEADER` |
| Intent | `> phrase` | `OP_PUSH_PARAM` + `OP_EXECUTE_CALL` |
| Table | `\| a \| b \|` | `OP_PUSH_MATRIX` |
| Code block | `` ```lang `` | `OP_FENCED_CODE` |
| Import | `@import "path"` | Inlined at compile time |
