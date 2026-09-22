# Git

Markscript Git integration --- full VCS lifecycle through shell dispatch.
Every intent runs a `git` command and captures its output.

---

## clone

Clone a remote repository into a local directory.

> run "git clone https://github.com/user/repo.git"

```markscript
# Clone a repo by URL
push("git clone https://github.com/user/repo.git")
call("run")
# Creates ./repo with full history
```

---

## pull

Fetch and merge changes from the remote tracking branch.

> run "git pull origin main"

```markscript
# Pull latest from origin/main
push("cd repo && git pull origin main")
call("run")
```

---

## commit

Stage all changes and commit with a message.

> run "git add -A && git commit -m "feat: add login flow""

```markscript
# Stage everything and commit
push("git add -A && git commit -m \"feat: add login flow\"")
call("run")
```

---

## push

Push local commits to the remote repository.

> run "git push origin main"

```markscript
# Push to origin/main
push("git push origin main")
call("run")
```

---

## branch

List, create, or switch branches.

> run "git branch"

```markscript
# List local branches
push("git branch")
call("run")
```

> run "git checkout -b feature/new-feature"

```markscript
# Create and switch to a new branch
push("git checkout -b feature/new-feature")
call("run")
```

---

## tag

List or create tags.

> run "git tag"

```markscript
# List all tags
push("git tag")
call("run")
```

> run "git tag v1.0.0 -m \"Release v1.0.0\""

```markscript
# Create an annotated tag
push("git tag v1.0.0 -m \"Release v1.0.0\"")
call("run")
```

---

## log

View commit history with formatting.

> run "git log --oneline --graph --decorate -20"

```markscript
# Show last 20 commits as a graph
push("git log --oneline --graph --decorate -20")
call("run")
```

---

## diff

Show unstaged or staged changes.

> run "git diff"

```markscript
# Show unstaged changes
push("git diff")
call("run")
```

> run "git diff --cached"

```markscript
# Show staged (cached) changes
push("git diff --cached")
call("run")
```

---

## stash

Stash dirty working directory changes.

> run "git stash push -m \"WIP: partial refactor\""

```markscript
# Stash with a message
push("git stash push -m \"WIP: partial refactor\"")
call("run")
```

> run "git stash pop"

```markscript
# Restore the most recent stash
push("git stash pop")
call("run")
```

---

## merge

Merge another branch into the current branch.

> run "git merge feature/new-feature --no-ff"

```markscript
# Merge with explicit no-fast-forward
push("git merge feature/new-feature --no-ff")
call("run")
```

---

## rebase

Rebase the current branch onto another base.

> run "git rebase main"

```markscript
# Rebase current branch onto main
push("git rebase main")
call("run")
```

---

## status

Show working tree status.

> run "git status --short"

```markscript
# Show concise status
push("git status --short")
call("run")
```

---

## blame

Annotate a file line-by-line with commit information.

> run "git blame src/main.js"

```markscript
# Show blame for a file
push("git blame src/main.js")
call("run")
```
