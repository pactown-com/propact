# Usage Guide

## Getting Started

Propact allows you to execute multiple protocols directly from Markdown documents. Simply write protocol blocks in your markdown and run them with the `propact` command.

## Basic Usage

### 1. Create a Markdown Document

Create a file named `pipeline.md`:

```markdown
# My Protocol Pipeline

## Step 1: Setup Environment
```propact:shell
echo "Setting up environment..."
mkdir -p output
```

## Step 2: Fetch Data
```propact:rest
GET https://api.example.com/data
Authorization: Bearer YOUR_TOKEN
```

## Step 3: Process with MCP
```propact:mcp
{
  "method": "tools/call",
  "params": {
    "name": "data_processor",
    "arguments": {
      "input": "output/data.json"
    }
  }
}
```

## Step 4: Real-time Updates
```propact:ws
{
  "type": "subscribe",
  "channel": "updates",
  "filters": ["processed"]
}
```
```

### 2. Run the Pipeline

```bash
# Execute all protocols
propact pipeline.md

# Execute only shell commands
propact pipeline.md --protocol shell

# List all protocol blocks without executing
propact pipeline.md --list

# Show detailed output
propact pipeline.md --verbose
```

## Protocol Blocks

### Shell Protocol

Execute shell commands and scripts:

```propact:shell
# Single command
echo "Hello World"

# Multiple commands
ls -la
grep "pattern" file.txt

# With environment variables
export API_KEY="secret"
curl -H "Authorization: $API_KEY" https://api.example.com
```

### MCP Protocol

Communicate with Model Context Protocol servers:

```propact:mcp
{
  "method": "tools/list",
  "id": 1
}
```

```propact:mcp
{
  "method": "tools/call",
  "id": 2,
  "params": {
    "name": "file_editor",
    "arguments": {
      "file_path": "output.txt",
      "content": "Processed data"
    }
  }
}
```

### REST Protocol

Make HTTP requests:

```propact:rest
GET https://api.example.com/users
Accept: application/json
```

```propact:rest
POST https://api.example.com/data
Content-Type: application/json
Authorization: Bearer TOKEN

{
  "name": "Example",
  "value": 42
}
```

```propact:rest
PUT https://api.example.com/data/123
Content-Type: application/json

{
  "status": "updated"
}
```

### WebSocket Protocol

Handle WebSocket connections:

```propact:ws
{
  "type": "connect",
  "url": "ws://localhost:8080"
}
```

```propact:ws
{
  "type": "message",
  "data": {
    "action": "subscribe",
    "channel": "events"
  }
}
```

## Working with Attachments

Include binary files and images:

```markdown
# Document with attachments

![Diagram](diagram.png)

```propact:shell
# Process the attached image
python process_image.py diagram.png
```
```

## Python API

Use Propact programmatically:

```python
import asyncio
from propact import ToonPact, ProtocolType

async def run_pipeline():
    # Load a document
    pact = ToonPact("pipeline.md")
    
    # Execute all protocols
    results = await pact.execute()
    
    # Check results
    for block_id, result in results.items():
        print(f"{block_id}: {result}")
    
    # Execute only specific protocol
    shell_results = await pact.execute(protocol=ProtocolType.SHELL)
    
    # Access parsed blocks
    await pact.load()
    for block in pact.blocks:
        print(f"Found {block.protocol.value} block")

# Run the pipeline
asyncio.run(run_pipeline())
```

## Advanced Features

### Custom Protocol Handlers

```python
from propact.protocols import ShellProtocol

# Create custom shell protocol with specific environment
shell = ShellProtocol()
result = await shell.execute(
    "echo $CUSTOM_VAR",
    env={"CUSTOM_VAR": "custom_value"}
)
```

### Attachment Handling

```python
from propact.attachments import AttachmentHandler

handler = AttachmentHandler()

# Extract all attachments from markdown
attachments = await handler.extract_from_markdown(
    content,
    base_path=Path("docs")
)

# Process attachments
for path, data in attachments.items():
    print(f"Found attachment: {path} ({len(data)} bytes)")
```

## Best Practices

1. **Organize by Protocol**: Group related protocol blocks together
2. **Use Descriptive Headers**: Add context before each protocol block
3. **Handle Dependencies**: Ensure blocks execute in the correct order
4. **Error Handling**: Check results of each block
5. **Security**: Avoid sensitive data in markdown files

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure shell commands have proper permissions
2. **Network Errors**: Check REST/WS endpoints are accessible
3. **Missing Attachments**: Verify attachment paths are correct
4. **MCP Connection**: Ensure MCP server is running

### Debug Mode

Use verbose output for detailed debugging:

```bash
propact document.md --verbose
```

This will show:
- Full stdout/stderr for shell commands
- HTTP response details for REST
- WebSocket message logs
- MCP communication details
