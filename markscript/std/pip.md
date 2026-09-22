# Pip

Markscript pip integration - Python package management through
shell dispatch.

---

## install

Install a Python package.

> run "pip install requests"

```markscript
# Install a package from PyPI
push("pip install requests")
call("run")
```

> run "pip install torch==2.0.1 --index-url https://download.pytorch.org/whl/cu118"

```markscript
# Install a specific version with custom index
push("pip install torch==2.0.1 --index-url https://download.pytorch.org/whl/cu118")
call("run")
```

---

## uninstall

Remove an installed Python package.

> run "pip uninstall -y requests"

```markscript
# Uninstall without confirmation prompt
push("pip uninstall -y requests")
call("run")
```

---

## freeze

List installed packages in pip freeze format (pinned versions).

> run "pip freeze"

```markscript
# Output all installed packages with versions
push("pip freeze")
call("run")
```

> run "pip freeze > requirements.txt"

```markscript
# Save current environment to requirements file
push("pip freeze > requirements.txt")
call("run")
```

---

## list

List installed packages.

> run "pip list"

```markscript
# Show all installed packages
push("pip list")
call("run")
```

> run "pip list --outdated"

```markscript
# Show only outdated packages
push("pip list --outdated")
call("run")
```

---

## upgrade

Upgrade an installed package to the latest version.

> run "pip install --upgrade pip"

```markscript
# Upgrade pip itself
push("pip install --upgrade pip")
call("run")
```

> run "pip install --upgrade numpy"

```markscript
# Upgrade a specific package
push("pip install --upgrade numpy")
call("run")
```

---

## requirements

Install packages from a requirements file.

> run "pip install -r requirements.txt"

```markscript
# Install all deps from requirements file
push("pip install -r requirements.txt")
call("run")
```

> run "pip install -r requirements-dev.txt"

```markscript
# Install dev dependencies
push("pip install -r requirements-dev.txt")
call("run")
```
