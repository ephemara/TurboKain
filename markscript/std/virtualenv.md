# Virtualenv

Markscript virtual environment management - create, activate, deactivate,
and manage isolated Python environments.

---

## create

Create a new Python virtual environment.

> run "python3 -m venv .venv"

```markscript
# Create a venv in .venv directory
push("python3 -m venv .venv")
call("run")
```

> run "virtualenv -p python3.11 myenv"

```markscript
# Create a virtualenv with a specific Python version
push("virtualenv -p python3.11 myenv")
call("run")
```

> run "conda create -n myenv python=3.10 -y"

```markscript
# Create a conda environment with Python 3.10
push("conda create -n myenv python=3.10 -y")
call("run")
```

---

## activate

Activate a virtual environment for subsequent commands.

> run ".venv/Scripts/activate"

```markscript
# Activate venv on Windows
push(".venv/Scripts/activate && echo \"activated\"")
call("run")
```

> run "source .venv/bin/activate && which python"

```markscript
# Activate venv on macOS/Linux and verify python path
push("source .venv/bin/activate && which python")
call("run")
```

> run "conda activate myenv && python --version"

```markscript
# Activate a conda environment and check Python version
push("conda activate myenv && python --version")
call("run")
```

---

## deactivate

Deactivate the current virtual environment.

> run "deactivate"

```markscript
# Deactivate the active venv/virtualenv
push("deactivate")
call("run")
```

> run "conda deactivate"

```markscript
# Deactivate a conda environment
push("conda deactivate")
call("run")
```

---

## list

List all available virtual environments.

> run "ls -d */ 2>/dev/null | findstr .venv"

```markscript
# Find .venv directories in current folder (Windows)
push("dir /ad /b .venv 2>nul")
call("run")
```

> run "conda env list"

```markscript
# List all conda environments
push("conda env list")
call("run")
```

> run "ls ~/.virtualenvs/"

```markscript
# List virtualenvwrapper environments
push("ls ~/.virtualenvs/")
call("run")
```

---

## remove

Remove a virtual environment.

> run "rm -rf .venv"

```markscript
# Delete a venv directory
push("rm -rf .venv")
call("run")
```

> run "conda env remove -n myenv -y"

```markscript
# Remove a conda environment
push("conda env remove -n myenv -y")
call("run")
```

> workon

Create an environment using virtualenvwrapper's mkvirtualenv.

> run "mkvirtualenv -p python3.11 myproject"

```markscript
# Create a virtualenvwrapper-managed project env
push("mkvirtualenv -p python3.11 myproject")
call("run")
```
