<!-- code2docs:start --># propact

![version](https://img.shields.io/badge/version-0.1.0-blue) ![python](https://img.shields.io/badge/python-%3E%3D3.9-blue) ![coverage](https://img.shields.io/badge/coverage-unknown-lightgrey) ![functions](https://img.shields.io/badge/functions-44-green)
> **44** functions | **15** classes | **11** files | CC̄ = 2.1

> Auto-generated project documentation from source code analysis.

**Author:** Tom Softreck <tom@sapletta.com>  
**License:** MIT[(LICENSE)](./LICENSE)  
**Repository:** [https://github.com/pactown-com/propact](https://github.com/pactown-com/propact)

## Installation

### From PyPI

```bash
pip install propact
```

### From Source

```bash
git clone https://github.com/pactown-com/propact
cd propact
pip install -e .
```


## Quick Start

### CLI Usage

```bash
# Generate full documentation for your project
propact ./my-project

# Only regenerate README
propact ./my-project --readme-only

# Preview what would be generated (no file writes)
propact ./my-project --dry-run

# Check documentation health
propact check ./my-project

# Sync — regenerate only changed modules
propact sync ./my-project
```

### Python API

```python
from propact import generate_readme, generate_docs, Code2DocsConfig

# Quick: generate README
generate_readme("./my-project")

# Full: generate all documentation
config = Code2DocsConfig(project_name="mylib", verbose=True)
docs = generate_docs("./my-project", config=config)
```

## Generated Output

When you run `propact`, the following files are produced:

```
<project>/
├── README.md                 # Main project README (auto-generated sections)
├── docs/
│   ├── api.md               # Consolidated API reference
│   ├── modules.md           # Module documentation with metrics
│   ├── architecture.md      # Architecture overview with diagrams
│   ├── dependency-graph.md  # Module dependency graphs
│   ├── coverage.md          # Docstring coverage report
│   ├── getting-started.md   # Getting started guide
│   ├── configuration.md    # Configuration reference
│   └── api-changelog.md    # API change tracking
├── examples/
│   ├── quickstart.py       # Basic usage examples
│   └── advanced_usage.py   # Advanced usage examples
├── CONTRIBUTING.md         # Contribution guidelines
└── mkdocs.yml             # MkDocs site configuration
```

## Configuration

Create `propact.yaml` in your project root (or run `propact init`):

```yaml
project:
  name: my-project
  source: ./
  output: ./docs/

readme:
  sections:
    - overview
    - install
    - quickstart
    - api
    - structure
  badges:
    - version
    - python
    - coverage
  sync_markers: true

docs:
  api_reference: true
  module_docs: true
  architecture: true
  changelog: true

examples:
  auto_generate: true
  from_entry_points: true

sync:
  strategy: markers    # markers | full | git-diff
  watch: false
  ignore:
    - "tests/"
    - "__pycache__"
```

## Sync Markers

propact can update only specific sections of an existing README using HTML comment markers:

```markdown
<!-- propact:start -->
# Project Title
... auto-generated content ...
<!-- propact:end -->
```

Content outside the markers is preserved when regenerating. Enable this with `sync_markers: true` in your configuration.

## Architecture

```
propact/
    ├── propact/        ├── parser        ├── cli        ├── attachments        ├── protocols/            ├── shell            ├── mcp├── project        ├── core            ├── ws            ├── rest```

## API Overview

### Classes

- **`MarkdownParser`** — Parser for extracting protocol blocks from markdown documents.
- **`AttachmentHandler`** — Handles binary attachments in Protocol Pact documents.
- **`ShellProtocol`** — Handles shell command execution within Protocol Pact.
- **`MCPMessage`** — MCP message structure.
- **`MCPProtocol`** — Handles MCP (Model Context Protocol) communication within Protocol Pact.
- **`ProtocolType`** — Supported protocol types.
- **`ProtocolBlock`** — Represents a protocol block in markdown.
- **`ToonPact`** — Main class for executing Protocol Pact documents.
- **`WebSocketState`** — WebSocket connection states.
- **`WebSocketMessage`** — WebSocket message structure.
- **`WebSocketProtocol`** — Handles WebSocket communication within Protocol Pact.
- **`HTTPMethod`** — HTTP methods supported by REST protocol.
- **`RESTRequest`** — REST request structure.
- **`RESTResponse`** — REST response structure.
- **`RESTProtocol`** — Handles REST API communication within Protocol Pact.

### Functions

- `main(file_path, protocol, list, verbose)` — Execute Protocol Pact documents.
- `list_blocks(pact)` — List all protocol blocks in the document.
- `display_results(results, verbose)` — Display execution results.


## Project Structure

📄 `project`
📦 `src.propact`
📄 `src.propact.attachments` (7 functions, 1 classes)
📄 `src.propact.cli` (3 functions)
📄 `src.propact.core` (7 functions, 3 classes)
📄 `src.propact.parser` (4 functions, 1 classes)
📦 `src.propact.protocols`
📄 `src.propact.protocols.mcp` (7 functions, 2 classes)
📄 `src.propact.protocols.rest` (6 functions, 4 classes)
📄 `src.propact.protocols.shell` (3 functions, 1 classes)
📄 `src.propact.protocols.ws` (7 functions, 3 classes)

## Requirements



## Contributing

**Contributors:**
- Tom Softreck <tom@sapletta.com>
- Tom Sapletta <tom-sapletta-com@users.noreply.github.com>

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/pactown-com/propact
cd propact

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Documentation

- 📖 [Full Documentation](https://github.com/pactown-com/propact/tree/main/docs) — API reference, module docs, architecture
- 🚀 [Getting Started](https://github.com/pactown-com/propact/blob/main/docs/getting-started.md) — Quick start guide
- 📚 [API Reference](https://github.com/pactown-com/propact/blob/main/docs/api.md) — Complete API documentation
- 🔧 [Configuration](https://github.com/pactown-com/propact/blob/main/docs/configuration.md) — Configuration options
- 💡 [Examples](./examples) — Usage examples and code samples

### Generated Files

| Output | Description | Link |
|--------|-------------|------|
| `README.md` | Project overview (this file) | — |
| `docs/api.md` | Consolidated API reference | [View](./docs/api.md) |
| `docs/modules.md` | Module reference with metrics | [View](./docs/modules.md) |
| `docs/architecture.md` | Architecture with diagrams | [View](./docs/architecture.md) |
| `docs/dependency-graph.md` | Dependency graphs | [View](./docs/dependency-graph.md) |
| `docs/coverage.md` | Docstring coverage report | [View](./docs/coverage.md) |
| `docs/getting-started.md` | Getting started guide | [View](./docs/getting-started.md) |
| `docs/configuration.md` | Configuration reference | [View](./docs/configuration.md) |
| `docs/api-changelog.md` | API change tracking | [View](./docs/api-changelog.md) |
| `CONTRIBUTING.md` | Contribution guidelines | [View](./CONTRIBUTING.md) |
| `examples/` | Usage examples | [Browse](./examples) |
| `mkdocs.yml` | MkDocs configuration | — |

<!-- code2docs:end -->