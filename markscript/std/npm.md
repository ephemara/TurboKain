# Npm

Markscript npm integration - package management, scripts, and lifecycle
commands for Node.js projects.

---

## init

Initialize a new npm package.

> run "npm init -y"

```markscript
# Quick init with defaults, create package.json
push("npm init -y")
call("run")
```

---

## install

Install a package to node_modules.

> run "npm install express"

```markscript
# Install a dependency
push("npm install express")
call("run")
```

> run "npm install --save-dev typescript"

```markscript
# Install as dev dependency
push("npm install --save-dev typescript")
call("run")
```

---

## uninstall

Remove a package from node_modules and package.json.

> run "npm uninstall lodash"

```markscript
# Uninstall a package
push("npm uninstall lodash")
call("run")
```

---

## update

Update all packages to their latest compatible versions.

> run "npm update"

```markscript
# Update all deps within semver ranges
push("npm update")
call("run")
```

> run "npm install react@latest"

```markscript
# Update a specific package to latest
push("npm install react@latest")
call("run")
```

---

## run

Run a script defined in package.json.

> run "npm run build"

```markscript
# Run the 'build' script
push("npm run build")
call("run")
```

> run "npm run test -- --coverage"

```markscript
# Run with extra arguments
push("npm run test -- --coverage")
call("run")
```

---

## test

Run the test script from package.json.

> run "npm test"

```markscript
# Run default test suite
push("npm test")
call("run")
```

---

## publish

Publish the package to the npm registry.

> run "npm publish --access public"

```markscript
# Publish a public package
push("npm publish --access public")
call("run")
```

---

## audit

Run a security audit on installed packages.

> run "npm audit"

```markscript
# Check for known vulnerabilities
push("npm audit")
call("run")
```

> run "npm audit fix"

```markscript
# Auto-fix vulnerabilities where possible
push("npm audit fix")
call("run")
```

---

## list

List installed packages with their versions.

> run "npm list --depth=0"

```markscript
# Show top-level installed packages
push("npm list --depth=0")
call("run")
```

> run "npm ls -g --depth=0"

```markscript
# List globally installed packages
push("npm ls -g --depth=0")
call("run")
```

---

## outdated

Show outdated packages with current and latest versions.

> run "npm outdated"

```markscript
# Check what needs updating
push("npm outdated")
call("run")
```
