# Propact 🚀 Protocol Pact via Markdown

[![PyPI](https://img.shields.io/pypi/v/propact.svg)](https://pypi.org/project/propact/)
[![Python](https://img.shields.io/pypi/pyversions/propact.svg)](https://pypi.org/project/propact/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

**Markdown speaks all protocols!** Shell → MCP → REST/WS without conversion.

```bash
pip install propact
propact README.md  # Run this file!
```

## 🚀 Quick Start

```propact:shell
echo "Shell → MCP → REST pipeline works!"
```

## Features

- **Universal Protocol Support**: Execute Shell, MCP, REST, and WebSocket protocols directly from Markdown
- **Attachment Handling**: Manage binary files and images within your protocol documents
- **Async Execution**: Full async/await support for concurrent protocol execution
- **Type Safety**: Full type annotations with Pydantic integration
- **Modern Python**: Built with Python 3.10+ and the latest best practices

## Example Usage

```python
import asyncio
from propact import ToonPact

async def main():
    # Load a Protocol Pact document
    pact = ToonPact("README.md")
    
    # Execute all protocols
    results = await pact.execute()
    print(results)
    
    # Execute only shell protocols
    shell_results = await pact.execute(protocol=ProtocolType.SHELL)
    print(shell_results)

asyncio.run(main())
```

## Protocol Blocks

### Shell Protocol
```propact:shell
echo "Hello from shell!"
ls -la
```

### MCP Protocol
```propact:mcp
{
  "method": "tools/call",
  "params": {
    "name": "example_tool",
    "arguments": {"input": "test"}
  }
}
```

### REST Protocol
```propact:rest
GET https://api.example.com/data
Content-Type: application/json
```

### WebSocket Protocol
```propact:ws
{
  "type": "subscribe",
  "channel": "updates"
}
```

## Installation

```bash
pip install propact
```

Or with Poetry:

```bash
poetry add propact
```

## Development

```bash
# Clone the repository
git clone https://github.com/wronai/propact.git
cd propact

# Install development dependencies
poetry install --with dev

# Run tests
make test

# Run linting
make lint
```

## License

Licensed under Apache-2.0.


Apache-2.0 © Tom Sapletta
