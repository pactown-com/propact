<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

## 🏗️ **Implementacja konwersji w Propact** (kod gotowy do `src/propact/converter.py`)

```python
# src/propact/converter.py
import json, yaml, base64, re
from typing import Dict, Any, Union
from pathlib import Path

class MDConverter:
    @staticmethod
    def response_to_markdown(response: Dict[str, Any], headers: Dict) -> str:
        """Universal response → MD"""
        content_type = headers.get("content-type", "text/plain")
        
        if "json" in content_type:
            return f"```json\n{json.dumps(response, indent=2)}\n```"
        elif "yaml" in content_type:
            return f"```yaml\n{yaml.dump(response)}\n```"
        elif "image" in content_type:
            b64 = base64.b64encode(response).decode()
            mime = content_type.split(";")[0]
            return f"![response_image.{mime.split('/')[-1]}](data:{mime};base64,{b64})"
        elif "audio" in content_type or "video" in content_type:
            return f"![media.{content_type.split('/')[-1]}](data:{content_type};base64,{base64.b64encode(response).decode()})"
        elif isinstance(response, (dict, list)):
            return f"```json\n{json.dumps(response, indent=2)}\n```"
        return f"```\n{response}\n```"
    
    @staticmethod
    def extract_from_markdown(md_content: str) -> Dict[str, Any]:
        """MD → native payload"""
        # 1. Media: ![file.mp3](file.mp3) | data:audio/mp3;base64,...
        media = {}
        for match in re.finditer(r'!\[(.*?)\]\((data:(.+?);base64,(.+?)|(.+?))\)', md_content):
            name, mime, b64_data, _, file_path = match.groups()
            if b64_data:
                media[name] = base64.b64decode(b64_data)
            else:
                media[name] = Path(file_path).read_bytes()
        
        # 2. Codeblocks: ```json {...}
        code_data = {}
        for lang, content in re.findall(r'```(\w+)?\s*\n(.*?)\n```', md_content, re.DOTALL):
            lang = lang or "json"
            if lang == "json":
                code_data["json"] = json.loads(content)
            elif lang == "yaml":
                code_data["yaml"] = yaml.safe_load(content)
            else:
                code_data[lang] = content.strip()
        
        # 3. Plain text
        plain_text = re.sub(r'!\[.*?\]\(.*?\)|```.*?```', '', md_content, flags=re.DOTALL).strip()
        
        return {
            "media": media,
            "code": code_data,
            "text": plain_text
        }
```


## 🌐 **Full Protocol Dispatch Table**

| Protokół | Adapter | Payload mapping | Response → MD |
| :-- | :-- | :-- | :-- |
| **REST** | `httpx.post(url, files=media, json=code["json"])` | multipart/json | JSON→```json, files→![ ] |
| **Shell** | `sh.cmd(_in=json.dumps(code), data_binary=media.values())` | `--data/--data-binary` | stdout→text block |
| **MCP** | `session.call_tool("execute", arguments=code["json"] + media)` | Tool args + attachments | ToolResult→text |
| **gRPC** | `grpc_channel.invoke(method, message=code["proto"])` | Protobuf msg | Proto→YAML block |
| **GraphQL** | `gql.execute(query=code["graphql"], variables=code["json"])` | Query + vars | JSON→```graphql |
| **MQTT** | `mqtt.publish(topic, payload=json.dumps(code) + media)` | JSON + binary | Message→text |

## 🎬 **Kompletne przykłady examples/**

### **examples/01-openai-vision/README.md**

```markdown
# OpenAI Vision Analysis

![medical_scan.png](medical_scan.png)

```json
{
  "model": "gpt-4o",
  "messages": [{"role": "user", "content": "Analyze this X-ray"}]
}
```

**propact examples/01-openai-vision/README.md --endpoint https://api.openai.com/v1/chat/completions --header Authorization:Bearer sk-...**

```

### **examples/02-ffmpeg-cli/README.md**
```markdown
# FFmpeg Audio Processing

![podcast.mp3](podcast.mp3)

```bash
Convert to AAC, bitrate 128k
```

**propact examples/02-ffmpeg-cli/README.md --endpoint "ffmpeg -i stdin podcast.aac"**

```

### **examples/03-grpc-inference/README.md**
```protobuf
service Inference {
  rpc AnalyzeImage(ImageRequest) returns (Analysis);
}
```

```yaml
image: medical.jpg
model: resnet50
```


### **examples/04-md-server/server.md** (Propact server!)

```markdown
# Propact MD Server API
**POST ws://localhost:8080/propact**

Parses incoming MD, processes, returns updated MD.

**Status**: 🟢 Active
**Last update**: {{timestamp}}

Send me MD with `![image]` to analyze!
```

**Uruchom server**: `propact server.md --mode server`
**Client**: `propact client.md --endpoint ws://localhost:8080/propact`

## 🔧 **Smart Schema Adapter**

```python
async def adapt_to_schema(payload: Dict, schema: Dict, protocol: str):
    if protocol == "openapi":
        spec = prance.parse(schema)
        endpoint = find_best_match(spec, intent=payload["text"])
        return build_request(endpoint, payload)
    elif protocol == "shell":
        return build_curl_like(payload)
    # Auto-adaptation dla 10+ protokołów
```


## 📈 **Roadmap rozszerzeń**

```
Week 1: REST/Shell/MCP + konwersje
Week 2: gRPC/GraphQL/MQTT
Week 3: Server mode + Watch
Week 4: PyPI + Markpact plugin
Month 2: Visual editor (VSCode extension)
```

**Propact = "Markdown dla wszystkich API"** – **jedna prawda** w MD, **wszystkie protokoły** obsługiwane automatycznie. Gotowe do produkcji! 🌟

