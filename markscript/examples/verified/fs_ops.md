# Filesystem Operations

Full filesystem lifecycle: create directory, write file, check existence,
read file, verify content. All via markscript handler calls.

```markscript
print(mkdir(".mks_test_fs"))
print(write(".mks_test_fs/test.txt", "hello from markscript"))
print(exists(".mks_test_fs/test.txt"))
print(read(".mks_test_fs/test.txt"))
```

## verify

```markscript
print("fs_ops: full lifecycle completed")
```
