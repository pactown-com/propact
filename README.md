# Propact 🚀 Protocol Pact via Markdown

[![PyPI](https://img.shields.io/pypi/v/propact.svg)](https://pypi.org/project/propact/)
[![Python](https://img.shields.io/pypi/pyversions/propact.svg)](https://pypi.org/project/propact/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

**Markdown speaks all protocols!** Shell → MCP → REST/WS without conversion.


propact pozwala na wymiane danych markdown z roznymi rpotokołami pozwalającymi na przesyłanie całych markdown z zwartoscia z roznymi plikami audio video embedded oraz danymi w codeblock w prosty sposob, aby od strony cli to było proste a zeby mozna bylo dowolnie zmieniac endpointy. Chodzi o to, że mam plik markdown np z plikiem img wewnatrz w base64 i chce to wysłać na jakiś endpoint, np upload, ale musze oddzielnie wysłać obraz  a oddzielnie tekst, czyli musze to podzielić, wedle tego co pozwlaa api na endpoint i trzeba to algorytmicznie, inteligentnie rozdzielić i dlatego jest potrzebny propact

np przy załozeniu że musimy wysłac dane do openapi, mamy do dyspozycji dokuemntacji API i propact musi zrozumieć jak działa endpoint i dopasowac do niego treści, kt©óe zostamą do niego wysłane i tak samo, gdy otrrzymujemy jakies tresci z endpointu to musimy je zmianieć na markdown, nie sototne jaki był format źródłowy

chodzi o to, ze markdown jest podstaowywm formatem z metadanymi, a codeblock służy do trzyemania tych danych lub specjalne tagi dla mediów, 
więce finalnie trzymamy jeden format danych markdown, ale z odpowiednim przygotowaniem przed wysłaniem i po otrzymaniu na dysku, aby dla każdego oendpointu w zalęznosci od SCHEMA, cyzli np oopenapi lub cli shell lub innego API strony www, czy email, itd w zlaęznosci od rpototkołu, któryr też ma specyficzne schema przygotować markdown do trasnportu i z transportu do markdown,
 w zasadzie każdy plik markdown moze być też serverem danych i każdy mardkown moze być do niego wysłany w celu nadpisania, stwórz takie przykłady


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
- **Schema-Aware Processing**: Intelligently parse OpenAPI, CLI, and MCP schemas to adapt content
- **Smart Content Splitting**: Automatically separate attachments, code blocks, and text based on endpoint requirements
- **Attachment Handling**: Manage binary files, images, audio, and video within your protocol documents
- **Async Execution**: Full async/await support for concurrent protocol execution
- **Type Safety**: Full type annotations with Pydantic integration
- **Modern Python**: Built with Python 3.10+ and the latest best practices
- **MD-as-Server**: Markdown files can act as servers that update themselves

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


Licensed under Apache-2.0.


Licensed under Apache-2.0.


Licensed under Apache-2.0.


Apache-2.0 © Tom Sapletta
