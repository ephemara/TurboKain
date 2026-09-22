# SCP

Markscript SCP integration -- secure file transfer over SSH through
shell dispatch.

---

## upload

Upload a local file to a remote host.

> run "scp local_file.txt user@hostname:/remote/path/"

```markscript
# Upload a single file
push("scp local_file.txt user@hostname:/remote/path/")
call("run")
```

> run "scp ./dist/app.tar.gz user@hostname:/opt/app/"

```markscript
# Upload a build artifact
push("scp ./dist/app.tar.gz user@hostname:/opt/app/")
call("run")
```

---

## download

Download a file from a remote host to the local machine.

> run "scp user@hostname:/remote/logs/app.log ./logs/"

```markscript
# Download a remote file
push("scp user@hostname:/remote/logs/app.log ./logs/")
call("run")
```

> run "scp user@hostname:/data/backup.sql.gz ./backups/"

```markscript
# Download a database backup
push("scp user@hostname:/data/backup.sql.gz ./backups/")
call("run")
```

---

## recursive

Recursively copy an entire directory.

> run "scp -r ./build/ user@hostname:/var/www/html/"

```markscript
# Recursively upload a directory
push("scp -r ./build/ user@hostname:/var/www/html/")
call("run")
```

> run "scp -r user@hostname:/etc/nginx/ ./nginx-backup/"

```markscript
# Recursively download a remote directory
push("scp -r user@hostname:/etc/nginx/ ./nginx-backup/")
call("run")
```

---

## preserve

Copy with file attributes preserved (permissions, timestamps).

> run "scp -p config.env user@hostname:/app/config.env"

```markscript
# Upload preserving file attributes
push("scp -p config.env user@hostname:/app/config.env")
call("run")
```

---

## batch

Copy multiple files in a single command.

> run "scp file1.txt file2.log config.yml user@hostname:/data/"

```markscript
# Upload multiple files at once
push("scp file1.txt file2.log config.yml user@hostname:/data/")
call("run")
```

> run "scp user@hostname:/data/{log1.txt,log2.txt,meta.json} ."

```markscript
# Download multiple specific files using brace expansion
push("scp user@hostname:/data/{log1.txt,log2.txt,meta.json} .")
call("run")
```
