# Xargs

MarkScript command builder - build and execute command lines from stdin.
Wraps `xargs` via the IVT for batch and parallel execution.

---

## run

Execute a command for each item from stdin.

> run "cat filelist.txt | xargs wc -l"

```markscript
let list = "files.txt"
push("cat " + list + " | xargs wc -l")
call("run")
# word count on every file in list
```

---

## delimiter

Use a custom delimiter instead of whitespace.

> run "xargs -d '\\n' -I {} cp {} /backup/"

```markscript
let dir = "."
let target = "/backup/"
push("find " + dir + " -type f -print0 | xargs -0 -I {} cp {} " + target)
call("run")
# null-delimited for safe filenames
```

---

## max_args

Limit the number of arguments per command invocation.

> run "xargs -n 5 rm < files.txt"

```markscript
let n = 5
push("xargs -n " + n + " rm < files.txt")
call("run")
# rm called with 5 files at a time
```

---

## max_args_dry

Show what would run without executing.

> run "xargs -n 2 --dry-run echo < list.txt"

```markscript
let n = 2
push("xargs -n " + n + " --dry-run echo < list.txt")
call("run")
# previews the commands
```

---

## parallel

Run multiple processes in parallel.

> run "xargs -P 4 -I {} convert {} {}.png < images.txt"

```markscript
let procs = 4
push("xargs -P " + procs + " -I {} convert {} {}.png < images.txt")
call("run")
# up to 4 concurrent processes
```

---

## parallel_maxprocs

Auto-detect CPU count and use all cores.

> run "xargs -P $(nproc) -I {} gzip {} < files.txt"

```markscript
push("xargs -P $(nproc) -I {} gzip {} < files.txt")
call("run")
# uses all available CPU cores
```

---

## replace

Use a replacement string to position arguments.

> run "xargs -I '{}' mv '{}' '{}.bak' < files.txt"

```markscript
let pattern = "{}"
let suffix = ".bak"
push("xargs -I '" + pattern + "' mv '" + pattern + "' '" + pattern + suffix + "' < files.txt")
call("run")
# appends .bak to each file
```

---

## replace_custom

Use a custom replacement token.

> run "xargs -I '@@' cp @@ /backup/@@"

```markscript
let token = "@@"
let target = "/backup/"
push("xargs -I '" + token + "' cp " + token + " " + target + token + " < files.txt")
call("run")
# copies each file to backup
```

---

## interactive

Prompt before each execution.

> run "xargs -p rm < files.txt"

```markscript
push("xargs -p rm < files.txt")
call("run")
# asks "rm file.txt?" before each
```

---

## interactive_verbose

Show command then prompt before executing.

> run "xargs -p -t rm < files.txt"

```markscript
push("xargs -p -t rm < files.txt")
call("run")
# prints command then asks for confirmation
```

---

## max_lines

Use at most N lines per command.

> run "xargs -L 5 wc -l < files.txt"

```markscript
let lines = 5
push("xargs -L " + lines + " wc -l < files.txt")
call("run")
# 5 files per wc invocation
```

---

## exit_status

Exit if xargs encounters a non-zero exit from a command.

> run "xargs -P 2 -I {} sh -c 'command {} || exit 255' < tasks.txt"

```markscript
push("xargs -P 2 -I {} sh -c 'process_file {} || exit 255' < tasks.txt")
call("run")
# stops on first failure
```

---

## find_xargs

Pipe find results into xargs for batch processing.

> run "find . -name '*.tmp' -print0 | xargs -0 rm"

```markscript
let pattern = "*.tmp"
push("find . -name '" + pattern + "' -print0 | xargs -0 rm")
call("run")
# safely removes all .tmp files
```

---

## find_xargs_grep

Search files found by find using grep.

> run "find . -name '*.kn' -print0 | xargs -0 grep -l 'TODO'"

```markscript
let pattern = "*.kn"
let search = "TODO"
push("find . -name '" + pattern + "' -print0 | xargs -0 grep -l '" + search + "'")
call("run")
# filenames with TODO comments
```
