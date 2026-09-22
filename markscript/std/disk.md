# Disk

Markscript disk and volume management - query usage, free space, mount
points, volume types, and device info. Dispatches through the IVT to Kain's
`std::fs` and system disk APIs.

---

## usage

Get disk usage percentage for a given mount point or drive.

> run "df -h / 2>nul || wmic logicaldisk get size,freespace,caption"

```markscript
# Query disk usage for a path or drive
push("C:")
call("disk_usage")
# Result: usage percentage as integer (0-100)
```

---

## free

Get free space in bytes on the named volume.

> run "dir C:\ /-C | find "bytes free""

```markscript
# Query free space in bytes
push("C:")
call("disk_free")
# Result: free bytes as a large integer
```

---

## total

Get total capacity in bytes on the named volume.

> run "wmic logicaldisk where caption="C:" get size"

```markscript
# Query total disk capacity in bytes
push("C:")
call("disk_total")
# Result: total bytes as a large integer
```

---

## mount

Mount a filesystem at the specified mount point.

> run "mount -t ext4 /dev/sdb1 /mnt/data 2>nul || net use Z: \\server\share"

```markscript
# Mount a filesystem or network share
push("/dev/sdb1")
push("/mnt/data")
call("disk_mount")
# Result: 1 on success, 0 on failure
```

---

## unmount

Unmount a filesystem from the specified mount point.

> run "umount /mnt/data 2>nul || net use Z: /delete"

```markscript
# Unmount a filesystem or network share
push("/mnt/data")
call("disk_unmount")
# Result: 1 on success, 0 on failure
```

---

## list

List all mounted volumes and their mount points.

> run "wmic logicaldisk get caption,volumename 2>nul || df -h"

```markscript
# List all available volumes
call("disk_list")
# Result: newline-delimited volume list with mount points
```

---

## type

Get the filesystem type for a given volume.

> run "fsutil fsinfo fsInfo C: 2>nul || df -T /"

```markscript
# Query the filesystem type
push("C:")
call("disk_type")
# Result: "NTFS", "FAT32", "ext4", "ZFS", "apfs", etc.
```

---

## device

Get the underlying device path for a mount point.

> run "wmic logicaldisk where caption="C:" get deviceid"

```markscript
# Query the device backing a mount point
push("C:")
call("disk_device")
# Result: device path like "\\.\PhysicalDrive0" or "/dev/sda1"
```
