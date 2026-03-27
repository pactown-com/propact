# Posts API Example

This example demonstrates fetching blog posts from the JSONPlaceholder REST API using propact.

## Overview

JSONPlaceholder provides fake blog post data for testing. This example shows how to:
- Fetch blog posts using GET requests
- Handle post comments
- Work with nested resources

## API Endpoint

Base URL: `https://jsonplaceholder.typicode.com`

## Post Structure

Each post has the following fields:
- `userId`: The author user ID
- `id`: Unique post identifier
- `title`: Post title
- `body`: Post content

## Usage

### Quick Run
```bash
./run.sh
```

### Manual Commands

Get a single post:
```bash
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/posts/1" \
    --method GET
```

Get comments for a post:
```bash
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/posts/1/comments" \
    --method GET
```

List all posts:
```bash
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/posts?_limit=5" \
    --method GET
```

## Expected Response Format

Response is saved to `README.response.md` with markdown formatting:

```markdown
# Response from Propact

**Status:** 200

## JSON Response

```json
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat...",
  "body": "quia et suscipit..."
}
```

## Files

- `README.md` - This file with example description
- `run.sh` - Script to run the example
- `README.response.md` - Generated response file (created after running)
