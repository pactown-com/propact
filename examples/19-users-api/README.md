# Users API Example

This example demonstrates fetching user information from the JSONPlaceholder REST API using propact.

## Overview

JSONPlaceholder provides fake user data for testing. This example shows how to:
- Fetch user profiles using GET requests
- Handle nested JSON structures
- Extract and format user data including address and company info

## API Endpoint

Base URL: `https://jsonplaceholder.typicode.com`

## User Structure

Each user has the following fields:
- `id`: Unique identifier
- `name`: Full name
- `username`: Username
- `email`: Email address
- `address`: Object with street, suite, city, zipcode, and geo coordinates
- `phone`: Phone number
- `website`: Website URL
- `company`: Object with name, catchPhrase, and bs

## Usage

### Quick Run
```bash
./run.sh
```

### Manual Commands

Get a single user:
```bash
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/users/1" \
    --method GET
```

List all users:
```bash
poetry run propact run README.md \
    --endpoint "https://jsonplaceholder.typicode.com/users" \
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
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz",
  "address": {
    "street": "Kulas Light",
    "suite": "Apt. 556",
    "city": "Gwenborough",
    "zipcode": "92998-3874"
  },
  ...
}
```

## Files

- `README.md` - This file with example description
- `run.sh` - Script to run the example
- `README.response.md` - Generated response file (created after running)
