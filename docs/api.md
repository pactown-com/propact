# API Documentation

## Core Classes

### ToonPact

Main class for executing Protocol Pact documents.

```python
class ToonPact:
    def __init__(self, file_path: Union[str, Path])
    async def load(self) -> None
    async def execute(self, protocol: Optional[ProtocolType] = None) -> Dict[str, Any]
```

### ProtocolBlock

Represents a protocol block in markdown.

```python
@dataclass
class ProtocolBlock:
    protocol: ProtocolType
    content: str
    attachments: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### ProtocolType

Enum for supported protocol types.

```python
class ProtocolType(Enum):
    SHELL = "shell"
    MCP = "mcp"
    REST = "rest"
    WS = "ws"
```

## Parser

### MarkdownParser

Parses markdown documents to extract protocol blocks.

```python
class MarkdownParser:
    async def parse(self, content: str) -> List[ProtocolBlock]
```

## Protocols

### ShellProtocol

Handles shell command execution.

```python
class ShellProtocol:
    async def execute(self, command: str, cwd: Optional[Path] = None, 
                     env: Optional[Dict[str, str]] = None) -> Dict[str, Any]
    async def execute_script(self, script: str, cwd: Optional[Path] = None,
                           env: Optional[Dict[str, str]] = None) -> Dict[str, Any]
```

### MCPProtocol

Handles Model Context Protocol communication.

```python
class MCPProtocol:
    def register_tool(self, name: str, description: str, 
                     input_schema: Dict[str, Any]) -> None
    def register_resource(self, uri: str, name: str, 
                         description: str, mime_type: str = "text/plain") -> None
    async def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]
    async def get_resource(self, uri: str) -> Dict[str, Any]
```

### RESTProtocol

Handles REST API communication.

```python
class RESTProtocol:
    async def execute(self, request: RESTRequest) -> RESTResponse
    async def get(self, url: str, params: Optional[Dict[str, Any]] = None,
                 headers: Optional[Dict[str, str]] = None) -> RESTResponse
    async def post(self, url: str, body: Optional[Union[str, Dict[str, Any]]] = None,
                  headers: Optional[Dict[str, str]] = None) -> RESTResponse
    async def put(self, url: str, body: Optional[Union[str, Dict[str, Any]]] = None,
                 headers: Optional[Dict[str, str]] = None) -> RESTResponse
    async def delete(self, url: str, headers: Optional[Dict[str, str]] = None) -> RESTResponse
```

### WebSocketProtocol

Handles WebSocket communication.

```python
class WebSocketProtocol:
    async def connect(self) -> Dict[str, Any]
    async def disconnect(self) -> Dict[str, Any]
    async def send(self, message: Union[str, Dict[str, Any]]) -> Dict[str, Any]
    async def receive(self) -> Optional[WebSocketMessage]
    def add_message_handler(self, handler: Callable[[WebSocketMessage], None]) -> None
    def remove_message_handler(self, handler: Callable[[WebSocketMessage], None]) -> None
```

## Attachments

### AttachmentHandler

Manages binary attachments in Protocol Pact documents.

```python
class AttachmentHandler:
    async def load_attachment(self, path: Union[str, Path]) -> bytes
    async def save_attachment(self, data: bytes, path: Union[str, Path]) -> None
    def encode_base64(self, data: bytes) -> str
    def decode_base64(self, encoded: str) -> bytes
    def get_mime_type(self, path: Union[str, Path]) -> str
    async def extract_from_markdown(self, content: str, base_path: Optional[Path] = None) -> Dict[str, bytes]
```

## CLI

The `propact` command-line interface provides:

```bash
propact FILE_PATH [OPTIONS]

Options:
  -p, --protocol [shell|mcp|rest|ws]  Execute only blocks of the specified protocol
  -l, --list                          List all protocol blocks without executing
  -v, --verbose                       Show detailed output
```
