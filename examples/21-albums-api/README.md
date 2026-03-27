# Albums API Example

This example demonstrates fetching photo albums from the JSONPlaceholder REST API using propact.

## Overview

JSONPlaceholder provides fake album data for testing. This example shows how to:
- Fetch photo albums using GET requests
- Handle album-to-photos relationships
- Work with nested resources

## API Endpoint

Base URL: `https://jsonplaceholder.typicode.com`

## Album Structure

Each album has the following fields:
- `userId`: The owner user ID
- `id`: Unique album identifier
- `title`: Album title

## Usage

### Quick Run
```bash
./run.sh
```

### Manual Commands

Get a single album:
```bash
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/albums/1" \
    --method GET
```

Get photos in an album:
```bash
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/albums/1/photos?_limit=5" \
    --method GET
```

List all albums:
```bash
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/albums?_limit=5" \
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
  "title": "quidem molestiae enim"
}
```

## Files

- `README.md` - This file with example description
- `run.sh` - Script to run the example
- `README.response.md` - Generated response file (created after running)
