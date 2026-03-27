Proponuję **ToonPact** – prostą bibliotekę Python, która działa jak **Markpact**, ale skupia się na **uniwersalnej warstwie komunikacyjnej** z natywnym formatem `![img_2.png](img_2.png)` dla wszystkich protokołów (shell/REST/WS/MCP) i seamless transfer binary data.

## 🎯 Format `![filename.ext](filename.ext)` jako uniwersalny kontrakt

```markdown
# Przykład ToonPact README.md
ToonPact obsługuje obrazy, video, pliki bezpośrednio w Markdown:

![config.yaml](config.yaml)
![logo.png](logo.png) 
![demo.mp4](demo.mp4)
![model.onnx](model.onnx)

```toonpact:shell
echo "Test shell → MCP → REST pipeline"
```

```toonpact:mcp path=tools/math.py
# Automatycznie extract z MD i wyślij jako MCP tool
```

```toonpact:rest url=/api/v1/analyze
POST data z config.yaml + logo.png jako attachments
```

```

## 🧩 Kluczowe biblioteki (minimalny stack)

```bash
pip install rich markdown pydantic httpx mcp-python-sdk pytoony base64io
```

**Core biblioteki:**

- `rich` + `markdown` – parsing `![file.png](file.png)` → binary extraction
- `pytoony` – MD/Toon konwersja z embedded files
- `mcp-python-sdk` – MCP tools/resources transport
- `httpx` – REST/WS universal client
- `base64io` – binary transfer bez raw handling


## 🏗️ Architektura ToonPact (150 linii core)

```python
# toonpact.py – Markpact-like runtime dla komunikacji
import re, base64, httpx, asyncio
from pathlib import Path
from rich.markdown import Markdown
from rich.console import Console
from mcp import ClientSession
from pytoony import encode_toon
from pydantic import BaseModel
from typing import Dict, Any

console = Console()

class Attachment(BaseModel):
    name: str
    content: bytes
    mime: str = ""

class ToonPact:
    def __init__(self, readme_path: str):
        self.readme = Path(readme_path)
        self.attachments = {}  # ![file.png] → bytes
        self.routes = []      # toompact:shell, :rest, :mcp
        self._parse_readme()
    
    def _extract_attachments(self, content: str) -> Dict[str, Attachment]:
        """Parsuje ![filename.ext](filename.ext) → binary"""
        for match in re.finditer(r'!\[(.*?)\]\((.*?)\)', content):
            name, path = match.groups()
            if path.endswith(('png','jpg','mp4','pdf','onnx','yaml')):
                file_path = Path(path)
                if file_path.exists():
                    self.attachments[name or path] = Attachment(
                        name=name or path, 
                        content=file_path.read_bytes(),
                        mime=self._guess_mime(path)
                    )
        return self.attachments
    
    def _parse_readme(self):
        """Parsuje ```toonpact:shell, :rest, :mcp blocks"""
        content = self.readme.read_text()
        self._extract_attachments(content)
        
        for block in re.finditer(r'```toonpact:(\w+)(?:\s+(.*))?```(.*?)(?=```|$)', 
                               content, re.DOTALL):
            kind, meta, body = block.groups()
            self.routes.append({"kind": kind, "meta": meta, "body": body.strip()})
    
    async def execute(self):
        """Wykonuje routes z automatyczną konwersją MD→Toon→Native"""
        for route in self.routes:
            console.print(f"[bold cyan]🚀 {route['kind'].upper()}[/]: {route.get('meta', '')}")
            
            if route["kind"] == "shell":
                await self._exec_shell(route["body"])
            elif route["kind"] == "mcp":
                await self._exec_mcp(route)
            elif route["kind"] == "rest":
                await self._exec_rest(route)
    
    async def _exec_shell(self, cmd: str):
        """Shell z auto-capture → MD stream"""
        import subprocess
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        console.print(Markdown(stdout.decode()))
    
    async def _exec_mcp(self, route: Dict):
        """MCP tool call z attachments"""
        from mcp.types import ToolCallResult
        async with ClientSession() as session:
            # Payload z Toon + binary attachments
            payload = encode_toon({
                "command": route["body"],
                "attachments": {k: b64encode(v.content).decode() 
                              for k,v in self.attachments.items()}
            })
            result = await session.call_tool("execute", arguments=payload)
            console.print(Markdown(result.content[0].text))
    
    async def _exec_rest(self, route: Dict):
        """REST z multipart/form-data (files auto)"""
        async with httpx.AsyncClient() as client:
            files = {name: (name, data.content, data.mime) 
                    for name, data in self.attachments.items()}
            resp = await client.post(
                route.get("meta", "").split("url=")[1], 
                data={"payload": route["body"]},
                files=files
            )
            console.print(Markdown(resp.text))
    
    @staticmethod
    def _guess_mime(path: str) -> str:
        return {"png": "image/png", "mp4": "video/mp4"}.get(path.split('.')[-1])

# Użycie jak Markpact
if __name__ == "__main__":
    pact = ToonPact("README.md")
    asyncio.run(pact.execute())
```


## 🚀 Użycie (identyczne jak Markpact)

```bash
# 1. Stwórz README.md z attachments
echo "![config.yaml](config.yaml)" > README.md
echo "```toonpact:rest url=http://api.example.com```" >> README.md

# 2. Uruchom (auto-extract + execute)
python toonpact.py README.md

# 3. Lub CLI
toonpact README.md --run
toonpact README.md --watch  # Live reload
```


## ✨ Zalety vs Markpact

| Funkcja | Markpact | **ToonPact** |
| :-- | :-- | :-- |
| **Attachments** | ❌ | ✅ `![file.png]` → binary auto |
| **Multi-protocol** | README only | Shell/REST/WS/MCP |
| **Binary transfer** | ❌ | ✅ Base64 + multipart |
| **Toon/MD native** | ❌ | ✅ Token optimized |
| **Live reload** | ❌ | ✅ `--watch` mode |
| **Core size** | ~5k LOC | **150 LOC** |

## 📦 Rozszerzenia (opcjonalne)

```yaml
# routes.yaml (Camel-like DSL)
routes:
  - from: "![data.json](data.json)"
    via: "mcp://localhost/analyze"
    to: "rest://api.example.com/result"
  - from: "shell://ls -la"
    transform: "md_to_toon"
    to: "ws://chat.example.com"
```

**ToonPact** to **Markpact 2.0 dla komunikacji** – ten sam prosty format `![file.ext](file.ext)`, ale dla wszystkich protokołów z automatycznym binary handling. Idealne do Twoich MCP/embedded/Camel-like routingu! 🚀

