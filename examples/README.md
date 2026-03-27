# Propact Examples

This directory contains example Protocol Pact documents demonstrating various use cases.

## Examples

- [Shell to MCP Integration](shell-to-mcp/) - Demonstrates how to pipe shell output into MCP tools
- [REST to WebSocket Proxy](rest-ws-proxy/) - Shows how to create a proxy between REST APIs and WebSocket clients

## Running Examples

Each example can be run with the `propact` command:

```bash
# Run shell-to-mcp example
propact shell-to-mcp/README.md

# Run rest-ws-proxy example
propact rest-ws-proxy/README.md

# List protocol blocks without executing
propact shell-to-mcp/README.md --list
```
