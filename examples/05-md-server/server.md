# Propact MD Server

This markdown file acts as a server that updates itself with each request.

## Server Status

![status.png](status.png)

Current server status: **Running**
Listening on: ws://localhost:8080/propact

## Dynamic Content

Last update: {{timestamp}}
Last message: {{last_msg}}
Request count: {{request_count}}

## Message Log

```json
{
  "messages": [],
  "uptime": "0s",
  "clients_connected": 0
}
```

## Server Mode

When run in server mode, this file will:
1. Listen for incoming propact requests
2. Parse incoming markdown content
3. Update this file with new data
4. Maintain state between requests

## Run Command

```bash
# Start server mode
propact server.md --mode server --port 8080

# Send data to server
propact client.md --endpoint "ws://localhost:8080/propact"
```
