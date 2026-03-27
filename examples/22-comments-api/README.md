# Comments API Example

This example demonstrates fetching comments from the JSONPlaceholder REST API using propact.

## Overview

JSONPlaceholder provides fake comment data for testing. This example shows how to:
- Fetch comments using GET requests
- Filter comments by post
- Work with email and name fields

## API Endpoint

Base URL: `https://jsonplaceholder.typicode.com`

## Comment Structure

Each comment has the following fields:
- `postId`: The parent post ID
- `id`: Unique comment identifier
- `name`: Commenter name
- `email`: Commenter email
- `body`: Comment content

## Usage

### Quick Run
```bash
./run.sh
```

### Manual Commands

Get a single comment:
```bash
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/comments/1" \
    --method GET
```

Get comments for a post:
```bash
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/posts/1/comments" \
    --method GET
```

Filter comments by email:
```bash
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/comments?email=Jayne_Kuhic@sydney.com" \
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
  "postId": 1,
  "id": 1,
  "name": "id labore ex et quam laborum",
  "email": "Eliseo@gardner.biz",
  "body": "laudantium enim quasi est..."
}
```

## Files

- `README.md` - This file with example description
- `run.sh` - Script to run the example
- `README.response.md` - Generated response file (created after running)
