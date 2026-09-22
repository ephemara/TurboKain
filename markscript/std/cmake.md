# CMake

Markscript CMake integration - configure, build, install cycle for
C/C++ projects using CMake.

---

## configure

Configure the project with CMake.

> run "cmake -S . -B build -DCMAKE_BUILD_TYPE=Release"

```markscript
# Configure with release build type
push("cmake -S . -B build -DCMAKE_BUILD_TYPE=Release")
call("run")
```

> run "cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug"

```markscript
# Configure with Ninja generator and debug type
push("cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug")
call("run")
```

---

## build

Build the configured project.

> run "cmake --build build --config Release"

```markscript
# Build the Release configuration
push("cmake --build build --config Release")
call("run")
```

> run "cmake --build build --parallel 8"

```markscript
# Build with 8 parallel jobs
push("cmake --build build --parallel 8")
call("run")
```

---

## install

Install built artifacts to the install prefix.

> run "cmake --install build --prefix /usr/local"

```markscript
# Install to /usr/local
push("cmake --install build --prefix /usr/local")
call("run")
```

> run "cmake --install build --prefix ./dist"

```markscript
# Install to a local dist directory
push("cmake --install build --prefix ./dist")
call("run")
```

---

## clean

Remove the build directory.

> run "cmake --build build --target clean"

```markscript
# Clean build artifacts
push("cmake --build build --target clean")
call("run")
```

> run "rm -rf build"

```markscript
# Wipe the entire build directory
push("rm -rf build")
call("run")
```

---

## target

Build a specific CMake target.

> run "cmake --build build --target my_lib_static"

```markscript
# Build only a specific target
push("cmake --build build --target my_lib_static")
call("run")
```

> run "cmake --build build --target tests"

```markscript
# Build only the test target
push("cmake --build build --target tests")
call("run")
```

---

## preset

Use a CMake preset for configuration and build.

> run "cmake --preset ci"

```markscript
# Configure using 'ci' preset from CMakePresets.json
push("cmake --preset ci")
call("run")
```

> run "cmake --build --preset ci-release"

```markscript
# Build using 'ci-release' preset
push("cmake --build --preset ci-release")
call("run")
```
