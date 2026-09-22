# Test

Markscript's test standard library - assert utilities, benchmarks, and test
suite management routines. Each intent dispatches through the IVT to Kain's
stdlib bridge.

---

## assert_eq

> assert actual expected

Assert that two values are equal. Dispatches to Kain's `FN_ASSERT` handler.

```markscript
# assert_eq compares two values on the stack
# Expected input: actual value, expected value
# Result: asserts equality, prints PASS or FAIL

push(actual)
push(expected)
call("assert")
```

---

## assert_gt

Assert that the first value is greater than the second.

> assert a b where a > b

```markscript
# Load values and compare
push(a)
push(b)
push(a)
push(b)
# Call the comparison handler
call("assert")
```

---

## assert_lt

Assert that the first value is less than the second.

> assert a b where a < b

```markscript
# Load values and compare (reversed)
push(b)
push(a)
push(a)
push(b)
call("assert")
```

---

## benchmark

> run "benchmark command"

Execute a benchmark command and report timing. Dispatches to Kain's
`FN_PROCESS_OUTPUT` handler through the "run" IVT entry.

```markscript
# Run the benchmark command and capture output
push("benchmark command")
call("run")
```

---

## suite

> print "Running test suite"

Indicate the start of a test suite. Dispatches to the "print" IVT entry.

```markscript
# Print suite start message
push("Running test suite")
call("print")
```

---

## setup

> print "Setting up test environment"

Prepare the test environment. Called before each test suite run.

```markscript
# Setup placeholder
push("Setting up test environment")
call("print")
```

---

## teardown

> print "Tearing down test environment"

Clean up after a test suite run. Called after each test suite completes.

```markscript
# Teardown placeholder
push("Tearing down test environment")
call("print")
```

---

## expect_error

> assert expected_error

Assert that an error was produced with the expected error kind.

```markscript
# Compare error kind with expected value
push(expected_error_kind)
push(actual_error_kind)
call("assert")
```

---

## skip

> print "SKIPPED: <reason>"

Mark a test as skipped with an optional reason.

```markscript
# Print skip message with reason
push(reason)
call("print")
```
