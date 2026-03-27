# REST to WebSocket Proxy Example

This example demonstrates how to create a proxy that forwards REST API requests to WebSocket clients and vice versa.

## Overview

The proxy architecture:
1. Receives REST API requests
2. Forwards them through WebSocket connections
3. Broadcasts responses to subscribed clients
4. Handles bidirectional communication

## Protocol Blocks

### Step 1: Start WebSocket Server
```propact:shell
# Create a simple WebSocket server script
cat > ws_server.py << 'EOF'
import asyncio
import websockets
import json
from typing import Dict, Set

CONNECTED_CLIENTS: Set[websockets.WebSocketServerProtocol] = set()
MESSAGE_HISTORY: list = []

async def handler(websocket, path):
    CONNECTED_CLIENTS.add(websocket)
    print(f"Client connected: {websocket.remote_address}")
    
    try:
        # Send welcome message with history
        await websocket.send(json.dumps({
            "type": "welcome",
            "history": MESSAGE_HISTORY[-10:]  # Last 10 messages
        }))
        
        async for message in websocket:
            data = json.loads(message)
            data["timestamp"] = asyncio.get_event_loop().time()
            MESSAGE_HISTORY.append(data)
            
            # Broadcast to all clients
            for client in CONNECTED_CLIENTS:
                if client != websocket:
                    await client.send(json.dumps(data))
                    
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        CONNECTED_CLIENTS.remove(websocket)
        print(f"Client disconnected: {websocket.remote_address}")

async def main():
    server = await websockets.serve(handler, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
EOF

echo "WebSocket server script created"
```

### Step 2: Start the Server
```propact:shell
# Start WebSocket server in background
python3 ws_server.py &
WS_PID=$!
echo "WebSocket server started with PID: $WS_PID"
sleep 2  # Give server time to start
```

### Step 3: REST API Request
```propact:rest
POST http://localhost:8080/api/proxy
Content-Type: application/json
X-Target-Client: all

{
  "action": "get_users",
  "params": {
    "limit": 10,
    "offset": 0
  }
}
```

### Step 4: Subscribe to Updates
```propact:ws
{
  "type": "subscribe",
  "channels": ["api_responses", "user_updates"],
  "client_id": "client_001"
}
```

### Step 5: Send Data via WebSocket
```propact:ws
{
  "type": "api_request",
  "method": "GET",
  "endpoint": "/api/users",
  "params": {
    "active": true
  },
  "request_id": "req_123"
}
```

### Step 6: Another REST Request
```propact:rest
GET http://localhost:8080/api/proxy/status
Accept: application/json
```

### Step 7: Broadcast Message
```propact:ws
{
  "type": "broadcast",
  "message": "System maintenance in 5 minutes",
  "severity": "warning",
  "target": "all_clients"
}
```

### Step 8: Cleanup
```propact:shell
# Stop WebSocket server
if [ ! -z "$WS_PID" ]; then
    kill $WS_PID
    echo "WebSocket server stopped"
fi

# Clean up files
rm -f ws_server.py
echo "Cleanup completed"
```

## Running the Example

```bash
# Execute the full proxy demo
propact README.md

# Execute only REST requests
propact README.md --protocol rest

# Execute only WebSocket operations
propact README.md --protocol ws

# Execute only server operations
propact README.md --protocol shell
```

## Expected Flow

1. A WebSocket server is started on port 8765
2. REST requests are made to a proxy endpoint
3. WebSocket clients subscribe to channels
4. Messages are exchanged between REST and WebSocket
5. Broadcast messages are sent to all connected clients

## Architecture Diagram

```
REST Client → REST API → Proxy → WebSocket Server → WebSocket Clients
                                    ↑
                                    └── Broadcast Channel
```

## Notes

- This is a demonstration example with simulated REST endpoints
- In production, you would implement actual REST-to-WebSocket proxy logic
- The WebSocket server handles multiple clients and message broadcasting
- Message history is maintained for new client connections
