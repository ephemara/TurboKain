# Rsync

Markscript rsync integration --- high-performance file synchronization
over SSH or local transport.

---

## sync

Synchronize files from source to destination.

> run "rsync -avz ./src/ user@hostname:/dest/"

```markscript
# Archive mode with compression over SSH
push("rsync -avz ./src/ user@hostname:/dest/")
call("run")
```

> run "rsync -a /local/data/ /backup/data/"

```markscript
# Local directory sync
push("rsync -a /local/data/ /backup/data/")
call("run")
```

---

## mirror

Create an exact mirror (delete files that don't exist on source).

> run "rsync -avz --delete ./public/ user@hostname:/var/www/html/"

```markscript
# Mirror with delete - remote matches source exactly
push("rsync -avz --delete ./public/ user@hostname:/var/www/html/")
call("run")
```

---

## dry_run

Preview what would be transferred without actually copying.

> run "rsync -avz --dry-run ./src/ user@hostname:/dest/"

```markscript
# Preview changes without transferring
push("rsync -avz --dry-run ./src/ user@hostname:/dest/")
call("run")
```

> run "rsync -avz --dry-run --delete ./public/ /var/www/html/"

```markscript
# Preview mirror including deletions
push("rsync -avz --dry-run --delete ./public/ /var/www/html/")
call("run")
```

---

## exclude

Sync with specific files or patterns excluded.

> run "rsync -avz --exclude='node_modules' --exclude='.git' ./project/ user@hostname:/project/"

```markscript
# Sync a project excluding common dirs
push("rsync -avz --exclude='node_modules' --exclude='.git' ./project/ user@hostname:/project/")
call("run")
```

> run "rsync -avz --exclude='*.log' --exclude='tmp/' ./ user@hostname:/app/"

```markscript
# Exclude log files and temp directory
push("rsync -avz --exclude='*.log' --exclude='tmp/' ./ user@hostname:/app/")
call("run")
```

---

## delete

Delete extraneous files from destination directory.

> run "rsync -avz --delete --delete-excluded ./src/ /dst/"

```markscript
# Delete files on dst not in src, plus excluded files
push("rsync -avz --delete --delete-excluded ./src/ /dst/")
call("run")
```

> run "rsync -avz --delete-delay ./src/ user@hostname:/dest/"

```markscript
# Delete during the cleanup phase after transfer
push("rsync -avz --delete-delay ./src/ user@hostname:/dest/")
call("run")
```

---

## archive

Full archive mode preserving everything (recursive, links, perms, times, group, owner, devices).

> run "rsync -aHAX ./ user@hostname:/backup/"

```markscript
# Full archive with hardlinks, ACLs, extended attributes
push("rsync -aHAX ./ user@hostname:/backup/")
call("run")
```
