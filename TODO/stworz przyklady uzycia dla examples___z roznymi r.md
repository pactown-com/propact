<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# stworz przyklady uzycia dla examples/*

z roznymi rpotokołami pozwalającymi na przesyłanie całych markdown z zwartoscia z roznymi plikami audio video oraz danymi w codeblock
w prosty sposob, aby od strony cli to było proste a zeby mozna bylo dowolnie zmieniac endpointy. Chodzi o to, że mam plik markdown np z plikiem img wewnatrz w base64 i chce to wysłać na jakiś endpoint, np upload, ale musze oddzielnie wysłać obraz  a oddzielnie tekst, czyli musze to podzielić, wedle tego co pozwlaa api na endpoint i trzeba to algorytmicznie, inteligentnie rozdzielić i dlatego jest potrzebny propact

np przy załozeniu że musimy wysłac dane do openapi, mamy do dyspozycji dokuemntacji API i propact musi zrozumieć jak działa endpoint i dopasowac do niego treści, kt©óe zostamą do niego wysłane i tak samo, gdy otrrzymujemy jakies tresci z endpointu to musimy je zmianieć na markdown, nie sototne jaki był format źródłowy

chodzi o to, ze markdown jest podstaowywm formatem z metadanymi, a codeblock służy do trzyemania tych danych lub specjalne tagi dla mediów,
więce finalnie trzymamy jeden format danych markdown, ale z odpowiednim przygotowaniem przed wysłaniem i po otrzymaniu na dysku, aby dla każdego oendpointu w zalęznosci od SCHEMA, cyzli np oopenapi lub cli shell lub innego API strony www, czy email, itd w zlaęznosci od rpototkołu, któryr też ma specyficzne schema przygotować markdown do trasnportu i z transportu do markdown,
w zasadzie każdy plik markdown moze być też serverem danych i każdy mardkown moze być do niego wysłany w celu nadpisania, stwórz takie przykłady

Oto **kompletne przykłady użycia** w `examples/*` dla **Propact**. Każdy przykład to **samowystarczalny Markdown** z `![audio.mp3]` / codeblockami, który Propact **inteligentnie parsuje wg schema** (OpenAPI/CLI introspection), **dzieląc na payload/attachments**, wysyła, **konwertuje response → MD**, i zapisuje jako nowy plik MD (nadpisuje lub tworzy).[^1][^2]

CLI proste: `propact examples/shell-upload/README.md --endpoint "https://api.imgur.com/upload"`

## 📁 Struktura examples/

```
examples/
├── 01-shell-upload/
│   ├── README.md          # Źródło z ![audio.mp3]
│   ├── audio.mp3          # Attachment
│   └── schema.txt         # curl --help output
├── 02-openapi-rest/
│   ├── README.md
│   ├── image.png
│   └── openapi.json       # Schema
├── 03-mcp-tool/
│   ├── README.md
│   └── demo.mp4
├── 04-ws-chat/
│   ├── README.md
│   └── config.yaml
└── 05-md-server/          # MD jako server!
    └── server.md          # Propact server mode
```


## 🧑‍💻 **Propact core update** (dodaj do `src/propact/core.py`)

```python
# Dodaj schema introspection + smart split
import prance  # pip install prance[validation]
import subprocess

class Propact(ToonPact):
    def __init__(self, md_path: str, endpoint: str = None, schema: str = None):
        super().__init__(md_path)
        self.endpoint = endpoint
        self.schema = self._introspect_schema(schema)
    
    def _introspect_schema(self, schema_path: str):
        """OpenAPI/CLI schema → rules dla split MD"""
        if schema_path.endswith('.json'):
            return prance.ResolvingParser(schema_path).specification  # OpenAPI
        elif schema_path.endswith('.txt'): 
            return {"shell": subprocess.check_output("cat", schema_path).decode()}
        return {"generic": "multipart/form-data"}
    
    def _smart_split_md(self, content: str, schema: dict):
        """Algorytmicznie: ![img] → files, codeblock → json, text → body"""
        attachments = self._extract_attachments(content)
        code_data = re.findall(r'```(\w+)?\n(.*?)\n```', content, re.DOTALL)
        body_text = re.sub(r'!\[.*?\]\(.*?\)|```.*?```', '', content, flags=re.DOTALL)
        
        if "openapi" in schema:
            # Match endpoint schema → required params/files
            return {"files": attachments, "json": code_data, "text": body_text}
        return {"multipart": {"text": body_text, "files": attachments}}
    
    async def send_to_endpoint(self, endpoint: str):
        """Wysyła split MD → endpoint → response → nowy MD"""
        payload = self._smart_split_md(self.readme.read_text(), self.schema)
        
        if "rest" in endpoint:
            resp = await self._rest_smart_post(endpoint, payload)
        # ... mcp/shell/ws
        
        # Response → MD (JSON→codeblock, files→![ ])
        new_md = self._response_to_md(resp)
        output_path = self.readme.with_suffix('.response.md')
        output_path.write_text(new_md)
        console.print(f"💾 Saved: {output_path}")
```


## 🎯 **Przykłady użycia**

### **1. Shell Upload (CLI z base64 split)**

`examples/01-shell-upload/README.md`:

```markdown
# Shell Upload Example

Prześlij audio + text do CLI endpointu (np. `curl --data-binary`)

![audio.mp3](audio.mp3)

```bash
Upload this file with description: "My podcast episode"
```

**Endpoint**: `curl -X POST http://localhost:8080/upload`

```

**Uruchomienie**:
```bash
propact examples/01-shell-upload/README.md --endpoint "curl -X POST http://upload.api.com --data-binary @-"
# Propact: split ![audio.mp3] → --data-binary, text → --data "desc"
# Response → README.response.md
```


### **2. OpenAPI REST (schema-aware multipart)**

`examples/02-openapi-rest/README.md`:

```markdown
# OpenAPI Image Analysis

![image.png](image.png)

```json
{
  "prompt": "Analyze this medical image",
  "model": "gpt-4-vision"
}
```

**OpenAPI schema**: POST /analyze (multipart: file, json: prompt)

```

**Uruchomienie**:
```bash
propact examples/02-openapi-rest/README.md --endpoint "https://api.openai.com/v1/analyze" --schema openapi.json
# Propact: parsuje schema → {"multipart": {"file": image.png, "json": {...}}}
# Response JSON → ```json codeblock w README.response.md
```


### **3. MCP Tool Call (video + code)**

`examples/03-mcp-tool/README.md`:

```markdown
# MCP Video Processor

![demo.mp4](demo.mp4)

```python
# Tool args
{"duration": 30, "format": "h264"}
```

```

**Uruchomienie**:
```bash
propact examples/03-mcp-tool/README.md --endpoint "mcp://localhost/video-tool"
# Propact: MCP tool call z attachments → response MD
```


### **4. WS Chat (streaming MD)**

`examples/04-ws-chat/README.md`:

```markdown
# WS Chat z config

![config.yaml](config.yaml)

```yaml
message: "Hello from Propact!"
user_id: 123
```

```

### **5. MD Server (nadpisuje MD plik!)**
`examples/05-md-server/server.md` (uruchom: `propact server.md --mode server`):
```markdown
# Propact MD Server
Listening on ws://localhost:8080/propact

**Nadpiszę się po każdym request!**

Current time: {{timestamp}}
Last message: {{last_msg}}

![status.png](status.png)
```

**Client → Server**:

```bash
# Client wysyła MD do MD-servera
propact client.md --endpoint "ws://localhost:8080/propact"
# Server: parsuje, przetwarza, nadpisuje server.md → nowy MD!
```


## 🔧 **CLI usage (proste zmienne endpointy)**

```bash
# Uniwersalne
propact ANY_README.md --endpoint "curl|rest|ws|mcp://URL"

# Z schema
propact file.md --endpoint "https://api.com/upload" --schema openapi.json

# Server mode
propact server.md --mode server --port 8080

# Chain: shell → mcp → rest
propact chain.md --route "shell://cmd → mcp://tool → rest://api"
```


## 🧠 **Inteligentny algorytm split (pseudo-kod)**

```
def smart_split(md_content, schema):
    attachments = extract_images_audio(md_content)  # ![file.ext]
    code_data = extract_codeblocks(md_content)     # ```json/yaml/bash
    plain_text = strip_media_code(md_content)
    
    if schema.openapi:
        match = find_matching_endpoint(schema, intent=plain_text)
        return adapt_to_schema(match.params, attachments, code_data)
    elif schema.shell:
        return {"--data-binary": attachments, "--data": plain_text}
    
    return {"universal": {"multipart": {**attachments, "text": plain_text}}}
```

**Propact** zamienia **każdy Markdown w uniwersalny transport** – parsuje schema, splituje inteligentnie, wysyła, rekonstruuje MD z response. Jeden format, wszystkie protokoły! 🚀
<span style="display:none">[^10][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://jsontotable.org/openapi-to-markdown

[^2]: https://github.com/OpenAPITools/openapi-generator/blob/master/docs/generators/markdown.md

[^3]: https://the-guild.dev/graphql/inspector/docs/commands/introspect

[^4]: https://www.reddit.com/r/PayloadCMS/comments/1h93mul/payload_lexical_markdown_now/

[^5]: https://github.com/exogen/graphql-markdown

[^6]: https://github.com/bigsk1/llm-adapter

[^7]: https://openapi-generator.tech/docs/usage/

[^8]: https://graphql-markdown.dev/api/graphql/introspection

[^9]: https://apify.com/botflowtech/universal-markdown-scraper-for-llms/api

[^10]: https://stackoverflow.com/questions/54259816/how-to-generate-a-pdf-or-markup-from-openapi-3-0

