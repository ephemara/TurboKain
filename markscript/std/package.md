# Package

Markscript system package manager integration --- install, remove, update,
and search across apt, yum, dnf, and brew.

---

## install

Install a package using the system package manager.

> run "apt install -y curl"

```markscript
# Install curl via apt (Debian/Ubuntu)
push("apt install -y curl")
call("run")
```

> run "yum install -y git"

```markscript
# Install git via yum (RHEL/CentOS 7)
push("yum install -y git")
call("run")
```

> run "dnf install -y podman"

```markscript
# Install podman via dnf (Fedora/RHEL 8+)
push("dnf install -y podman")
call("run")
```

> run "brew install node"

```markscript
# Install node via Homebrew (macOS)
push("brew install node")
call("run")
```

---

## remove

Remove an installed package.

> run "apt remove -y curl"

```markscript
# Remove curl via apt (keeps config)
push("apt remove -y curl")
call("run")
```

> run "apt purge -y curl"

```markscript
# Remove curl with config files
push("apt purge -y curl")
call("run")
```

> run "brew uninstall node"

```markscript
# Uninstall node via Homebrew
push("brew uninstall node")
call("run")
```

---

## update

Update package lists and upgrade installed packages.

> run "apt update && apt upgrade -y"

```markscript
# Update all packages via apt
push("apt update && apt upgrade -y")
call("run")
```

> run "dnf upgrade --refresh -y"

```markscript
# Refresh metadata and update all via dnf
push("dnf upgrade --refresh -y")
call("run")
```

> run "brew update && brew upgrade"

```markscript
# Update all brews (macOS)
push("brew update && brew upgrade")
call("run")
```

---

## search

Search for packages matching a query.

> run "apt search webserver"

```markscript
# Search apt repositories for webserver
push("apt search webserver")
call("run")
```

> run "brew search --desc "text editor""

```markscript
# Search brews by description
push("brew search --desc \"text editor\"")
call("run")
```

---

## list

List installed packages.

> run "apt list --installed | head -30"

```markscript
# List installed apt packages (first 30)
push("apt list --installed | head -30")
call("run")
```

> run "brew list --versions"

```markscript
# List installed brews with versions
push("brew list --versions")
call("run")
```

> run "rpm -qa | grep -i "python""

```markscript
# Find all RPMs matching 'python'
push("rpm -qa | grep -i \"python\"")
call("run")
```
