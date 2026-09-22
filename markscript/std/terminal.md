# Terminal

Markscript terminal and console management - query size, clear screen,
apply colors, manage cursor, and control terminal modes. Dispatches through
the IVT to Kain's `std::ui` bridge and console APIs.

---

## size

Get the terminal window dimensions (columns and rows).

> run "mode con | findstr Columns"

```markscript
# Query terminal size
call("term_size")
# Result: two integers --- columns, rows
```

---

## clear

Clear the terminal screen and reset the cursor to the top-left corner.

> run "cls"

```markscript
# Clear the terminal screen
call("term_clear")
# Result: 1 on success
```

---

## color

Set the foreground and background color using ANSI escape codes or the
Windows console API.

> run "color 0A"

```markscript
# Set terminal colors
push("green")       # foreground
push("black")       # background
call("term_color")
# Result: 1 on success
```

---

## cursor_move

Move the terminal cursor to an absolute (row, column) position.

```markscript
# Move cursor to row 10, column 5
push(10)
push(5)
call("term_cursor_move")
# Result: 1 on success
```

---

## cursor_hide

Hide the terminal cursor.

```markscript
# Hide the cursor
call("term_cursor_hide")
# Result: 1 on success
```

---

## cursor_show

Show the terminal cursor.

```markscript
# Show the cursor
call("term_cursor_show")
# Result: 1 on success
```

---

## raw_mode

Enable raw mode on the terminal -- disable line buffering, echo, and
cooked-mode processing. Use for interactive single-key input.

```markscript
# Enable raw terminal mode
call("term_raw_mode")
# Result: 1 on success
# Now read single keypresses, then call cooked_mode to restore
```

---

## cooked_mode

Restore terminal to normal cooked (canonical) mode.

```markscript
# Restore cooked terminal mode
call("term_cooked_mode")
# Result: 1 on success
```

---

## bell

Ring the terminal bell.

> echo "

```markscript
# Ring the bell (ASCII BEL character)
call("term_bell")
# Result: 1 on success
```

---

## title

Set the terminal window title.

> title "My MarkScript App"

```markscript
# Set terminal window title
push("My MarkScript App")
call("term_title")
# Result: 1 on success
```
