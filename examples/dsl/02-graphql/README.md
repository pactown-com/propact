# GraphQL from Markdown

This example demonstrates converting structured Markdown to GraphQL queries.

## 📄 Input Markdown

```markdown
# GitHub Issues Query

User: alice
Status: OPEN
Limit: 10
```

## 🔄 Conversion Commands

### Convert to GitHub GraphQL Query

```bash
propact convert file README.md --from markdown --to graphql --api-type github
```

**Output:**

```graphql
query {
  user(login: "alice") {
    issues(states: [OPEN], first: 10) {
      nodes {
        title
        body
        state
        createdAt
      }
    }
  }
}
```

### Convert to Stripe GraphQL Query

```markdown
# Stripe Charges Query

Limit: 20
Status: succeeded
```

```bash
propact convert file README.md --from markdown --to graphql --api-type stripe
```

**Output:**

```graphql
query {
  charges(first: 20) {
    edges {
      node {
        id
        amount
        currency
        status
        created
      }
    }
  }
}
```

### Generic GraphQL Query

```markdown
# User Profile

User: viewer
Fields: id, name, email
```

```bash
propact convert file README.md --from markdown --to graphql --api-type generic
```

**Output:**

```graphql
query {
  viewer {
    id
    name
  }
}
```

## 🔄 Reverse Conversion

### GraphQL to Markdown

```bash
propact convert string "query { user(login: \"alice\") { issues(first: 10) { nodes { title } } } }" --from graphql --to markdown
```

**Output:**

```markdown
```graphql
query {
  user(login: "alice") {
    issues(first: 10) {
      nodes {
        title
        body
        state
        createdAt
      }
    }
  }
}
```
```

## 📋 Use Cases

1. **API Documentation**: Document GraphQL queries in readable Markdown
2. **Query Building**: Build complex queries through simple key-value pairs
3. **Code Generation**: Generate query templates from documentation
4. **Testing**: Create test queries in MD format for easy review

## 🔧 Supported API Types

- **github**: GitHub GraphQL API v4
- **stripe**: Stripe GraphQL API
- **generic**: Basic GraphQL structure

## 📝 Custom API Templates

You can extend the GraphQL converter to support custom APIs by modifying the `_generate_*_query` methods in `GraphQLConverter`.

## ✅ Requirements

Install DSL dependencies:

```bash
pip install propact[dsl]
```
