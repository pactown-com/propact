# Markdown Server Example

This example demonstrates how to use propact in server mode to create a self-updating markdown document.

## Content

```markdown
# Propact Server Demo

This is a self-updating markdown document served by propact.

## Current Status

The server is running and serving this document via WebSocket.

## Features

- Real-time updates
- WebSocket communication
- Markdown rendering
- State persistence

## Configuration

```yaml
server:
  host: localhost
  port: 8080
  mode: websocket
  
features:
  - live_updates
  - state_persistence
  - markdown_rendering
```

## Usage

Connect to the WebSocket server to receive updates:

```javascript
const ws = new WebSocket('ws://localhost:8080');
ws.onmessage = (event) => {
  console.log('Received update:', event.data);
};
```

## Run Command

```bash
propact server.md --mode server --port 8080
```

## Expected Behavior

1. Server starts on localhost:8080
2. Clients can connect via WebSocket
3. Document updates are pushed to all connected clients
4. State is persisted between sessions

## Testing

Use the included client script or any WebSocket client to test:

```bash
# Simple test with curl (for HTTP mode)
curl http://localhost:8080

# WebSocket test with wscat
wscat -c ws://localhost:8080
```
