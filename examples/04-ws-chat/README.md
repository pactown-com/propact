# WebSocket Chat Example

This example demonstrates propact's WebSocket streaming capabilities with configuration files.

## Chat Configuration

![config.yaml](config.yaml)

```yaml
# Chat message
message: "Hello from Propact!"
user_id: 123
channel: "general"
timestamp: "2024-01-15T10:30:00Z"
```

Additional context: This is a test message to verify WebSocket connectivity and message formatting.

## Expected Behavior

Propact will:
1. Connect to WebSocket endpoint
2. Send configuration file as resource
3. Stream YAML message content
4. Listen for responses
5. Convert received messages to markdown

## Run Command

```bash
propact README.md --endpoint "ws://localhost:8080/chat"
```

## WebSocket Schema

The WebSocket expects:
- Connection with authentication
- Resource uploads for config files
- Message streaming in YAML/JSON format
- Bidirectional communication
