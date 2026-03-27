# Propact Examples

This directory contains comprehensive examples demonstrating propact's capabilities across different protocols and use cases.

## Core Examples

### 01-shell-upload
Demonstrates base64 split for shell/CLI endpoints with audio files.
- **Protocol**: Shell/CLI
- **Features**: Audio attachment handling, metadata extraction
- **Run**: `./run.sh` or `propact README.md --endpoint "curl -X POST http://localhost:8080/upload"`

### 02-openapi-rest
Shows schema-aware multipart handling with OpenAPI specifications.
- **Protocol**: REST/HTTP
- **Features**: OpenAPI schema parsing, intelligent content adaptation
- **Run**: `./run.sh` or `propact README.md --endpoint "https://api.vision.ai/v1/analyze" --schema openapi.json`

### 03-mcp-tool
Video processing with MCP (Model Context Protocol).
- **Protocol**: MCP
- **Features**: Binary video data transport, tool parameter integration
- **Run**: `./run.sh` or `propact README.md --endpoint "mcp://localhost:8080/video-tool"`

### 04-ws-chat
WebSocket streaming with configuration files.
- **Protocol**: WebSocket
- **Features**: Real-time communication, YAML configuration
- **Run**: `./run.sh` or `propact README.md --endpoint "ws://localhost:8080/chat"`

### 05-md-server
Markdown as self-updating server.
- **Protocol**: WebSocket (server mode)
- **Features**: Self-modifying markdown, state persistence
- **Run**: `./run.sh` or `propact server.md --mode server --port 8080`

## Extended Examples

### 01-openai-vision
Medical image analysis using OpenAI's Vision API.
- **Protocol**: REST/HTTP with OpenAI API
- **Features**: Image analysis, JSON request formatting, API integration
- **Run**: `./run.sh` or `propact README.md --endpoint "https://api.openai.com/v1/chat/completions" --schema openapi.json`
- **Requirements**: OpenAI API key in `OPENAI_API_KEY` environment variable

### 02-ffmpeg-cli
Audio processing through FFmpeg CLI.
- **Protocol**: Shell/CLI
- **Features**: Audio conversion, metadata handling, CLI automation
- **Run**: `./run.sh` or `propact README.md --endpoint "ffmpeg -i podcast.mp3 -c:a aac -b:a 128k -ar 44100 processed_podcast.aac"`
- **Requirements**: FFmpeg installed on system

### 03-grpc-inference
ML model inference via gRPC.
- **Protocol**: gRPC
- **Features**: Protobuf handling, binary image data, structured responses
- **Run**: `./run.sh` or `propact README.md --endpoint "grpc://localhost:50051/InferenceService/AnalyzeImage"`
- **Requirements**: gRPC dependencies (`pip install propact[grpc]`)

## Legacy Examples

- [Shell to MCP Integration](shell-to-mcp/) - Demonstrates how to pipe shell output into MCP tools
- [REST to WebSocket Proxy](rest-ws-proxy/) - Shows how to create a proxy between REST APIs and WebSocket clients

## Protocol Support Matrix

| Example | REST | Shell | MCP | WebSocket | gRPC | OpenAI | FFmpeg |
|---------|------|-------|-----|-----------|------|--------|--------|
| 01-shell-upload | ✓ | ✓ | | | | | |
| 02-openapi-rest | ✓ | | | | | | |
| 03-mcp-tool | | | ✓ | | | | |
| 04-ws-chat | | | | ✓ | | | |
| 05-md-server | | | | ✓ | | | |
| 01-openai-vision | ✓ | | | | | ✓ | |
| 02-ffmpeg-cli | | ✓ | | | | | ✓ |
| 03-grpc-inference | | | | | ✓ | | |

## Running Examples

Each example includes a `run.sh` script that demonstrates how to use propact with that specific protocol or use case.

```bash
# Navigate to any example directory
cd examples/01-shell-upload

# Make the script executable (if needed)
chmod +x run.sh

# Run the example
./run.sh
```

Or use propact directly:

```bash
# Basic usage
propact README.md --endpoint "https://api.example.com"

# With schema
propact README.md --endpoint "https://api.example.com" --schema schema.json

# Server mode
propact server.md --mode server --port 8080
```

## Creating Your Own Examples

1. Create a new directory in `examples/`
2. Add a `README.md` with markdown content including:
   - Media files: `![filename.ext](filename.ext)`
   - Code blocks: ```json\n{...}\n```
   - Plain text descriptions
3. Add a `run.sh` script for easy execution
4. Optionally add schema files for OpenAPI/Protocol Buffers

## Dependencies

Some examples require additional dependencies:

- gRPC examples: `pip install propact[grpc]`
- GraphQL examples: `pip install propact[graphql]`
- MQTT examples: `pip install propact[mqtt]`
- SOAP examples: `pip install propact[soap]`
- All optional dependencies: `pip install propact[all]`
