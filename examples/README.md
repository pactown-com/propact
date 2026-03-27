# Propact Examples

This directory contains comprehensive examples demonstrating propact's capabilities across different protocols and use cases, including semantic matching, error recovery, and openapi-llm integration.

## 📁 Structure

Examples follow two structures:
- **Flat structure**: `examples/{name}.{md,sh,env}` for simple examples
- **Directory structure**: `examples/{name}/` for complex examples with multiple files

## 🧠 Semantic Matching & AI Features

### smart-test/
Basic semantic matching using sentence-transformers embeddings.
- **Features**: Embeddings-based endpoint matching, top-k results
- **Protocol**: REST/HTTP
- **Run**: `cd smart-test && PYTHONPATH=../../src python3 -m propact.cli README.md --openapi openapi.json --base-url "https://api.example.com"`

### openapi-llm-demo/
Integration with openapi-llm browser extension for zero-config API access.
- **Features**: LLM-enhanced descriptions, 96% accuracy
- **Protocol**: REST/HTTP
- **Run**: `cd openapi-llm-demo && PYTHONPATH=../../src python3 -m propact.cli README.md --openapi notion-openapi.json --base-url "https://api.notion.com/v1"`

### error-demo/
Multi-layer error recovery strategies demonstration.
- **Features**: Fallback search, retry logic, LLM self-correction
- **Protocol**: REST/HTTP
- **Run**: `cd error-demo && PYTHONPATH=../../src python3 -m propact.cli README.md --openapi ecommerce-api.json --base-url "https://api.example.com" --error-mode debug`

## Core Examples (01-08)

### 01-shell-upload.md
Demonstrates base64 split for shell/CLI endpoints with audio files.
- **Protocol**: Shell/CLI
- **Features**: Audio attachment handling, metadata extraction
- **Run**: `./01-shell-upload.sh`
- **Env**: Not required

### 02-openapi-rest.md
Shows schema-aware multipart handling with OpenAPI specifications.
- **Protocol**: REST/HTTP
- **Features**: OpenAPI schema parsing, intelligent content adaptation
- **Run**: `./02-openapi-rest.sh`
- **Env**: Not required

### 03-mcp-tool.md
Video processing with MCP (Model Context Protocol).
- **Protocol**: MCP
- **Features**: Binary video data transport, tool parameter integration
- **Run**: `./03-mcp-tool.sh`
- **Env**: Not required

### 04-ws-chat.md
WebSocket streaming with configuration files.
- **Protocol**: WebSocket
- **Features**: Real-time communication, YAML configuration
- **Run**: `./04-ws-chat.sh`
- **Env**: Not required

### 05-md-server.md
Markdown as self-updating server.
- **Protocol**: WebSocket (server mode)
- **Features**: Self-modifying markdown, state persistence
- **Run**: `./05-md-server.sh`
- **Env**: Not required

### 06-openai-vision.md
Medical image analysis using OpenAI's Vision API.
- **Protocol**: REST/HTTP with OpenAI API
- **Features**: Image analysis, JSON request formatting, API integration
- **Run**: `./06-openai-vision.sh`
- **Env**: `06-openai-vision.env`

### 07-ffmpeg-cli.md
Audio processing through FFmpeg CLI.
- **Protocol**: Shell/CLI
- **Features**: Audio conversion, metadata handling, CLI automation
- **Run**: `./07-ffmpeg-cli.sh`
- **Env**: Not required

### 08-grpc-inference.md
ML model inference via gRPC.
- **Protocol**: gRPC
- **Features**: Protobuf handling, binary image data, structured responses
- **Run**: `./08-grpc-inference.sh`
- **Env**: Not required

## Popular Services Integration (09-17)

### File Upload Services

#### 09-imgur.md
Image upload to Imgur hosting service.
- **Protocol**: REST/HTTP
- **Features**: Image hosting, URL generation
- **Run**: `./09-imgur.sh`
- **Env**: `09-imgur.env`

#### 10-slack.md
File upload to Slack channels.
- **Protocol**: REST/HTTP
- **Features**: Team collaboration, file sharing
- **Run**: `./10-slack.sh`
- **Env**: `10-slack.env`

#### 11-discord.md
File and message posting to Discord.
- **Protocol**: REST/HTTP
- **Features**: Community platform, media attachments
- **Run**: `./11-discord.sh`
- **Env**: `11-discord.env`

#### 12-openai-vision.md
Medical image analysis with GPT-4o Vision API.
- **Protocol**: REST/HTTP
- **Features**: AI analysis, confidence scores
- **Run**: `./12-openai-vision.sh`
- **Env**: `12-openai-vision.env`

### API Services

#### 13-github-gist.md
Multi-file Gist creation.
- **Protocol**: REST/HTTP
- **Features**: Code sharing, version control
- **Run**: `./13-github-gist.sh`
- **Env**: `13-github-gist.env`

#### 14-stripe.md
Payment intent creation with Stripe.
- **Protocol**: REST/HTTP
- **Features**: Payment processing, checkout
- **Run**: `./14-stripe.sh`
- **Env**: `14-stripe.env`

#### 15-youtube.md
Video metadata management.
- **Protocol**: REST/HTTP
- **Features**: Video platform, content management
- **Run**: `./15-youtube.sh`
- **Env**: `15-youtube.env`

#### 16-notion.md
Rich page creation with blocks and attachments.
- **Protocol**: REST/HTTP
- **Features**: Documentation, knowledge base
- **Run**: `./16-notion.sh`
- **Env**: `16-notion.env`

### Social Media

#### 17-twitter.md
Social media posting with media.
- **Protocol**: REST/HTTP
- **Features**: Two-step upload, social engagement
- **Run**: `./17-twitter.sh`
- **Env**: `17-twitter.env`

## Running Examples

### Individual Examples

Each example can be run directly:

```bash
# Make executable
chmod +x 01-shell-upload.sh

# Run example
./01-shell-upload.sh
```

### With Environment Variables

For examples that require API keys:

```bash
# Copy env template
cp 09-imgur.env 09-imgur.local.env

# Edit with your API keys
nano 09-imgur.local.env

# Load and run
source 09-imgur.local.env && ./09-imgur.sh
```

### Batch Testing

Run all examples with a simple script:

```bash
#!/bin/bash
# Run all examples
for file in *.sh; do
    echo "Running $file..."
    ./"$file"
done
```

## Protocol Support Matrix

| Example | REST | Shell | MCP | WebSocket | gRPC | OpenAI | FFmpeg |
|---------|------|-------|-----|-----------|------|--------|--------|
| 01-shell-upload | ✓ | ✓ | | | | | |
| 02-openapi-rest | ✓ | | | | | | |
| 03-mcp-tool | | | ✓ | | | | |
| 04-ws-chat | | | | ✓ | | | |
| 05-md-server | | | | ✓ | | | |
| 06-openai-vision | ✓ | | | | | ✓ | |
| 07-ffmpeg-cli | | ✓ | | | | | ✓ |
| 08-grpc-inference | | | | | ✓ | | |
| 09-imgur | ✓ | | | | | | |
| 10-slack | ✓ | | | | | | |
| 11-discord | ✓ | | | | | | |
| 12-openai-vision | ✓ | | | | | ✓ | |
| 13-github-gist | ✓ | | | | | | |
| 14-stripe | ✓ | | | | | | |
| 15-youtube | ✓ | | | | | | |
| 16-notion | ✓ | | | | | | |
| 17-twitter | ✓ | | | | | | |

## Legacy Examples

- [Shell to MCP Integration](shell-to-mcp/) - Demonstrates how to pipe shell output into MCP tools
- [REST to WebSocket Proxy](rest-ws-proxy/) - Shows how to create a proxy between REST APIs and WebSocket clients

## Testing Helper

The `propact.testing` module provides utilities for creating and testing examples:

```python
from propact.testing import ExampleHelper

# Create sample files
helper = ExampleHelper()
audio_file = helper.create_sample_file('audio.mp3')

# Run example with proper environment
result = helper.run_example(Path.cwd(), endpoint='https://api.example.com')

# Cleanup
helper.cleanup_files(audio_file)
```

## Creating Your Own Examples

1. Create a new example file: `my-example.md`
2. Add markdown content with:
   - Media files: `![filename.ext](filename.ext)`
   - Code blocks: ```json\n{...}\n```
   - Plain text descriptions
3. Create a runner script: `my-example.sh`
4. Optionally add env template: `my-example.env`
5. Make script executable: `chmod +x my-example.sh`

## Dependencies

Some examples require additional dependencies:

- gRPC examples: `pip install propact[grpc]`
- GraphQL examples: `pip install propact[graphql]`
- MQTT examples: `pip install propact[mqtt]`
- SOAP examples: `pip install propact[soap]`
- All optional dependencies: `pip install propact[all]`
