# SQL Insert from Markdown Table

This example demonstrates converting a Markdown table to SQL INSERT statements.

## 📄 Input Markdown

```markdown
# Users Table

| id | name    | email             | active |
|----|---------|-------------------|--------|
| 1  | Alice   | alice@example.com | true   |
| 2  | Bob     | bob@example.com   | false  |
| 3  | Charlie | charlie@example.com | true |
```

## 🔄 Conversion Commands

### Convert to SQL (PostgreSQL)

```bash
propact convert file README.md --from markdown --to sql --dialect postgres --table-name users
```

**Output:**

```sql
CREATE TABLE IF NOT EXISTS "users" ("id" TEXT, "name" TEXT, "email" TEXT, "active" TEXT);
INSERT INTO "users" ("id", "name", "email", "active") VALUES ('1', 'Alice', 'alice@example.com', 'true');
INSERT INTO "users" ("id", "name", "email", "active") VALUES ('2', 'Bob', 'bob@example.com', 'false');
INSERT INTO "users" ("id", "name", "email", "active") VALUES ('3', 'Charlie', 'charlie@example.com', 'true');
```

### Convert to SQL (MySQL)

```bash
propact convert file README.md --from markdown --to sql --dialect mysql --table-name users
```

### Generate UPDATE Statements

```bash
propact convert file README.md --from markdown --to sql --operation UPDATE --key-column id --table-name users
```

**Output:**

```sql
CREATE TABLE IF NOT EXISTS "users" ("id" TEXT, "name" TEXT, "email" TEXT, "active" TEXT);
UPDATE "users" SET "name" = 'Alice', "email" = 'alice@example.com', "active" = 'true' WHERE "id" = '1';
UPDATE "users" SET "name" = 'Bob', "email" = 'bob@example.com', "active" = 'false' WHERE "id" = '2';
UPDATE "users" SET "name" = 'Charlie', "email" = 'charlie@example.com', "active" = 'true' WHERE "id" = '3';
```

## 🔄 Reverse Conversion

### SQL Query to Markdown Table

```bash
propact convert string "SELECT * FROM users WHERE active = true" --from sql --to markdown
```

**Output:**

```markdown
| id | name    | email             |
|----|---------|-------------------|
| 1  | Alice   | alice@example.com |
| 3  | Charlie | charlie@example.com |
```

## 📋 Use Cases

1. **Data Migration**: Convert spreadsheet data (saved as MD tables) to SQL
2. **Documentation**: Include SQL samples in documentation as MD tables
3. **Testing**: Generate test data as MD tables, convert to SQL for setup
4. **Code Reviews**: Review data changes in MD format before applying to database

## 🔧 Advanced Options

- **Custom table name**: `--table-name custom_table`
- **SQL dialects**: postgres, mysql, sqlite, snowflake, bigquery
- **Operation types**: INSERT (default), UPDATE
- **Key column**: Required for UPDATE operations

## ✅ Requirements

Install DSL dependencies:

```bash
pip install propact[dsl]
```

This will install: sqlglot, pandas, PyYAML, xmltodict, markdown-table-generator
