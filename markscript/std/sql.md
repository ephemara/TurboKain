# SQL

SQL database operations: querying, schema management, and migration helpers.

## query

Execute a SELECT query against a database and return rows as list of dicts.

> run "python -c \"import sqlite3; ...\""

```markscript
let db_path = "app.db"

let rows = sql.query(db_path, "SELECT id, name, email FROM users WHERE active = 1")
# rows = [{"id": 1, "name": "Alice", "email": "alice@x.com"}, ...]

> assert rows[0]["name"] "Alice"
```

## insert

Insert a row into a table and return the new row ID.

> run "python -c \"import sqlite3; ... INSERT ...\""

```markscript
let db_path = "app.db"
let new_user = {"name": "Bob", "email": "bob@x.com", "active": 1}

let row_id = sql.insert(db_path, "users", new_user)
> print "Inserted user with ID: " + str(row_id)
```

## update

Update rows matching a condition. Returns count of affected rows.

> run "python -c \"... UPDATE ... SET ... WHERE ...\""

```markscript
let db_path = "app.db"
let changes = {"active": 0}

let affected = sql.update(db_path, "users", changes, "email LIKE '%@old.com'")
> print "Deactivated " + str(affected) + " users"
```

## delete

Delete rows matching a condition. Returns count of deleted rows.

> run "python -c \"... DELETE FROM ... WHERE ...\""

```markscript
let db_path = "app.db"

let removed = sql.delete(db_path, "sessions", "expires_at < datetime('now')")
> print "Cleaned up " + str(removed) + " expired sessions"
```

## create_table

Create a new table with specified columns and types.

> run "python -c \"... CREATE TABLE ...\""

```markscript
let schema = {
  "id": "INTEGER PRIMARY KEY",
  "title": "TEXT NOT NULL",
  "body": "TEXT",
  "created_at": "TEXT DEFAULT CURRENT_TIMESTAMP"
}

sql.create_table(db_path, "posts", schema)
> run "python -c \"import sqlite3; print([c[1] for c in sqlite3.connect('app.db').cursor().execute('PRAGMA table_info(posts)')])\""
```

## migrate

Apply a list of migration SQL strings, tracking applied migrations.

> run "python -c \"... migrations ...\""

```markscript
let migrations = []
migrations[0] = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)"
migrations[1] = "ALTER TABLE users ADD COLUMN email TEXT"
migrations[2] = "CREATE INDEX idx_users_email ON users(email)"

sql.migrate(db_path, migrations)
> print "All migrations applied"
```

## transaction

Execute multiple statements inside a transaction with commit/rollback.

> run "python -c \"... BEGIN ... COMMIT ...\""

```markscript
let ops = []
ops[0] = "INSERT INTO accounts (id, balance) VALUES (1, 1000)"
ops[1] = "INSERT INTO accounts (id, balance) VALUES (2, 500)"
ops[2] = "UPDATE accounts SET balance = balance - 100 WHERE id = 1"
ops[3] = "UPDATE accounts SET balance = balance + 100 WHERE id = 2"

let ok = sql.transaction(db_path, ops)
> assert ok true
> print "Transfer completed"
```

## bulk_insert

Insert many rows efficiently using a single statement with parameter binding.

> run "python -c \"... executemany ...\""

```markscript
let columns = ["product", "price", "qty"]
let data = [
  ["Widget", "9.99", "100"],
  ["Gadget", "24.99", "50"],
  ["Doohickey", "4.99", "200"]
]

let count = sql.bulk_insert(db_path, "inventory", columns, data)
> assert count 3
> print "Inserted " + str(count) + " rows"
```
