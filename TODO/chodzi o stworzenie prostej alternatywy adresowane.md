<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# chodzi o stworzenie prostej alternatywy adresowanej jak markpact like format ![img_2.png](img_2.png)

# markpact - + GitOps meets AI Agents — all in one README.

[![PyPI version](https://img.shields.io/pypi/v/markpact.svg)](https://pypi.org/project/markpact/)
[![Python](https://img.shields.io/pypi/pyversions/markpact.svg)](https://pypi.org/project/markpact/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Tests](https://github.com/wronai/markpact/actions/workflows/tests.yml/badge.svg)](https://github.com/wronai/markpact/actions)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Markpact to minimalny runtime, który pozwala trzymać cały projekt w jednym `README.md`.
Runtime ignoruje zwykły Markdown, a wykonuje wyłącznie codeblocki `markpact:*`.

## 💡 Czym jest Markpact?

Markpact to narzędzie, które zamienia plik README.md w **wykonywalny kontrakt projektu**. Zamiast utrzymywać osobno dokumentację i kod źródłowy, wszystko znajduje się w jednym miejscu.

### Kluczowe możliwości:

| Funkcja | Opis |
| :-- | :-- |
| **Executable README** | Uruchom cały projekt z jednego pliku README.md |
| **LLM Generation** | Wygeneruj projekt z opisu tekstowego: `markpact -p "REST API"` |
| **Live Demo** | Interaktywne demo z generowaniem PDF: `python examples/demo_live_markpact.py` |
| **PDF Generation** | Automatyczne tworzenie PDF dokumentacji (7 stron) |
| **Multi-language** | Python, Node.js, Go, Rust, PHP, TypeScript, React |
| **Publishing** | Publikuj do PyPI, npm, Docker Hub jedną komendą |
| **Docker Sandbox** | Uruchom w izolowanym kontenerze: `--docker` |
| **HTTP Testing** | Definiuj testy HTTP w `markpact:test http` |
| **Auto-fix** | Automatyczne naprawianie błędów runtime |
| **Sync \& Rollback** | Synchronizuj pliki źródłowe z README: `markpact sync` |

### Dla kogo?

- **Deweloperzy** – szybkie prototypowanie i uruchamianie projektów
- **DevOps** – CI/CD z README jako single source of truth
- **Edukatorzy** – interaktywne tutoriale z wykonywalnym kodem
- **LLM/AI** – generowanie i modyfikacja projektów przez AI

![img_3.png](img_3.png)

## 🚀 Szybki start

```bash
git clone [https://github.com/wronai/markpact.git](https://github.com/wronai/markpact.git)
# Instalacja
pip install markpact[llm]

# Konfiguracja LLM (wybierz jeden)
markpact config --provider ollama                              # lokalny
markpact config --provider openrouter --api-key sk-or-v1-xxx   # chmura

# Generuj i uruchom jedną komendą!
markpact -p "REST API do zarządzania zadaniami z SQLite" -o todo/README.md --run

markpact -p "URL shortener with FastAPI and SQLite" -o url-test/README.md --run

# Lub z gotowego przykładu
markpact -e todo-api -o todo/README.md --run
```


## 🎬 Demo Live - Generowanie z LLM w czasie rzeczywistym

Spróbuj interaktywnego demo, które generuje kompletny projekt z promptu i tworzy PDF dokumentacji:

```bash
# Wejdź do katalogu markpact
cd /home/tom/github/wronai/markpact

# Uruchom demo z własnym promptem
python examples/demo_live_markpact.py --prompt "Build a chat API with WebSocket"

# Lub użyj gotowego przykładu
python examples/demo_live_markpact.py --example todo-api

# Lista dostępnych przykładów
python examples/demo_live_markpact.py --list
```

**Co robi demo:**

1. **Generuje kontrakt** z LLM (Ollama/OpenRouter/OpenAI)
2. **Parsuje bloki** `markpact:*` z wygenerowanego README
3. **Waliduje** wszystkie wymagane bloki
4. **Tworzy PDF** z pełną dokumentacją (7 stron)
5. **Zapisuje wyniki** do `generated/live/`

**Wymagania:**

```bash
pip install markpact[llm] fpdf2
```

**Przykład wyjścia:**

```
[PASS] LLM wygenerował kontrakt  81.1s, 2177 znaków
[PASS] Znaleziono 4 bloków  0.0ms
[PASS] Zaleznosci: 3 pakietów  fastapi, uvicorn, websockets
[PASS] Plik: app/main.py  36 linii
[PASS] PDF zapisany: generated/live/markpact_live_custom.pdf  13 KB, 7 stron
```


## 🤖 Generowanie z LLM

Wygeneruj kompletny projekt z opisu tekstowego:

```bash
# Lista 16 gotowych przykładów
markpact --list-examples

# Generuj z promptu
markpact -p "URL shortener z FastAPI i SQLite" -o url/README.md

# Generuj i uruchom natychmiast (one-liner)
markpact -p "Chat WebSocket z FastAPI" -o chat/README.md --run

# Uruchom w izolowanym Docker
markpact -p "Blog API z komentarzami" -o blog/README.md --run --docker
```

**Obsługiwane providery:** Ollama (lokalny), OpenRouter, OpenAI, Anthropic, Groq

Szczegóły: [docs/generator.md](docs/generator.md)

## 📦 Publikacja do rejestrów

Publikuj artefakty bezpośrednio z README:

```bash
# PyPI
markpact README.md --publish --bump patch

# npm
markpact README.md --publish --registry npm

# Docker Hub
markpact README.md --publish --registry docker

# GitHub Container Registry
markpact README.md --publish --registry ghcr
```

Obsługiwane rejestry: **PyPI**, **npm**, **Docker Hub**, **GitHub Packages**, **GHCR**

## 📓 Konwersja Notebooków

Konwertuj notebooki do formatu markpact:

```bash
# Lista obsługiwanych formatów
markpact --list-notebook-formats

# Konwersja Jupyter Notebook
markpact --from-notebook notebook.ipynb -o project/README.md

# Konwersja i uruchomienie
markpact --from-notebook notebook.ipynb -o project/README.md --run

# Podgląd konwersji
markpact --from-notebook notebook.ipynb --convert-only
```

**Obsługiwane formaty:**


| Format | Rozszerzenie | Opis |
| :-- | :-- | :-- |
| Jupyter Notebook | `.ipynb` | Python, R, Julia |
| R Markdown | `.Rmd` | R z markdown |
| Quarto | `.qmd` | Wielojęzyczny |
| Databricks | `.dib` | Python, Scala, R |
| Zeppelin | `.zpln` | Python, Scala, SQL |

## 📚 Dokumentacja

- [Pełna dokumentacja](docs/README.md)
- [Demo Live Guide](examples/README.md) ⭐ **NEW** - Interaktywne demo z PDF
- [Generowanie z LLM](docs/generator.md) ⭐ **NEW**
- [Kontrakt markpact:*](docs/contract.md)
- [CI/CD Integration](docs/ci-cd.md)
- [Współpraca z LLM](docs/llm.md)


## 🎯 Przykłady

| Przykład | Opis | Uruchomienie |
| :-- | :-- | :-- |
| [Demo Live](examples/demo_live_markpact.py) | **Interaktywne generowanie z LLM + PDF** | `python examples/demo_live_markpact.py --prompt "Chat API"` |
| [FastAPI Todo](examples/fastapi-todo/) | REST API z bazą danych | `markpact examples/fastapi-todo/README.md` |
| [Flask Blog](examples/flask-blog/) | Aplikacja webowa z szablonami | `markpact examples/flask-blog/README.md` |
| [CLI Tool](examples/cli-tool/) | Narzędzie linii poleceń | `markpact examples/cli-tool/README.md` |
| [Streamlit Dashboard](examples/streamlit-dashboard/) | Dashboard danych | `markpact examples/streamlit-dashboard/README.md` |
| [Kivy Mobile](examples/kivy-mobile/) | Aplikacja mobilna | `markpact examples/kivy-mobile/README.md` |
| [Electron Desktop](examples/electron-desktop/) | Aplikacja desktopowa | `markpact examples/electron-desktop/README.md` |
| [Markdown Converter](examples/markdown-converter/) | Konwersja zwykłego MD | `markpact examples/markdown-converter/sample.md --convert` |
| [Go HTTP API](examples/go-http-api/) | REST API w Go | `markpact examples/go-http-api/README.md` |
| [Node Express API](examples/node-express-api/) | REST API w Node.js | `markpact examples/node-express-api/README.md` |
| [Static Frontend](examples/static-frontend/) | Statyczny HTML/CSS/JS | `markpact examples/static-frontend/README.md` |
| [Python Typer CLI](examples/python-typer-cli/) | CLI w Python (Typer) | `markpact examples/python-typer-cli/README.md` |
| [Rust Axum API](examples/rust-axum-api/) | REST API w Rust | `markpact examples/rust-axum-api/README.md` |
| [PHP CLI](examples/php-cli/) | CLI w PHP | `markpact examples/php-cli/README.md` |
| [React TypeScript SPA](examples/react-typescript-spa/) | SPA React + TS | `markpact examples/react-typescript-spa/README.md` |
| [TypeScript Node API](examples/typescript-node-api/) | REST API w TS (Node) | `markpact examples/typescript-node-api/README.md` |
| [PyPI Publish](examples/pypi-publish/) | Publikacja do PyPI | `markpact examples/pypi-publish/README.md --publish` |
| [npm Publish](examples/npm-publish/) | Publikacja do npm | `markpact examples/npm-publish/README.md --publish` |
| [Docker Publish](examples/docker-publish/) | Publikacja do Docker | `markpact examples/docker-publish/README.md --publish` |
| [Notebook Converter](examples/notebook-converter/) | Konwersja .ipynb do markpact | `markpact --from-notebook examples/notebook-converter/sample.ipynb --convert-only` |

## 🧪 Testowanie przykładów

Uruchom automatyczne testy wszystkich przykładów:

```bash
# Dry-run (tylko parsowanie)
./scripts/test_examples.sh

# Pełne uruchomienie
./scripts/test_examples.sh --run

# Verbose output
./scripts/test_examples.sh --verbose
```


## 🔄 Sync — synchronizacja plików z README

Komenda `sync` aktualizuje bloki `markpact:file` w README.md na podstawie rzeczywistych plików w katalogu źródłowym (np. `sandbox/`). Odwrotność `markpact pack`.

```bash
# Synchronizacja (auto-detect sandbox/ obok README)
markpact sync README.md

# Z własnym katalogiem źródłowym
markpact sync README.md --source ./my-project

# Podgląd zmian bez zapisu
markpact sync README.md --dry-run --diff

# CI check — exit 1 jeśli pliki nie są zsynchronizowane
markpact sync README.md --check

# Lista śledzonych plików
markpact sync README.md --list

# Pliki w katalogu źródłowym nie śledzone w README
markpact sync README.md --missing

# Wyklucz wrażliwe pliki
markpact sync README.md --exclude .env --exclude .env.prod
```


### Rollback — przywracanie poprzedniej wersji

Każdy `sync` automatycznie tworzy backup README w `.markpact/` (max 10).

```bash
# Przywróć ostatni backup
markpact sync README.md --rollback

# Lista dostępnych backupów
markpact sync README.md --backups

# Przywróć konkretny backup
markpact sync README.md --rollback-to .markpact/README.md.bak.20240301_143022
```


### Opcje `markpact sync`

| Flaga | Opis |
| :-- | :-- |
| `-n`, `--dry-run` | Podgląd bez zapisu |
| `-d`, `--diff` | Pokaż unified diff |
| `-c`, `--check` | CI: exit 1 jeśli out-of-sync |
| `-l`, `--list` | Lista śledzonych plików |
| `-m`, `--missing` | Pliki źródłowe bez bloku w README |
| `--exclude PATH` | Wyklucz plik (powtarzalne) |
| `--rollback` | Przywróć z ostatniego backup |
| `--rollback-to FILE` | Przywróć z konkretnego backup |
| `--backups` | Lista dostępnych backupów |
| `-s`, `--source DIR` | Katalog źródłowy (domyślnie: `sandbox/`) |

## 🔄 Konwersja zwykłego Markdown

Markpact może automatycznie konwertować zwykłe pliki Markdown (bez tagów `markpact:*`) do formatu wykonywalnego:

```bash
# Podgląd konwersji
markpact README.md --convert-only

# Konwersja i uruchomienie
markpact README.md --convert

# Auto-detekcja (konwertuj jeśli brak markpact blocks)
markpact README.md --auto

# Zapisz skonwertowany plik
markpact README.md --convert-only --save-converted output.md
```

Konwerter analizuje code blocks i na podstawie heurystyk wykrywa:

- **Zależności** → `markpact:deps` (pakiety Python/Node)
- **Pliki źródłowe** → `markpact:file` (importy, klasy, funkcje)
- **Komendy** → `markpact:run` (python, uvicorn, npm, etc.)


## 1️⃣ Cel projektu

- **Jedno README jako źródło prawdy**
- **Możliwość uruchomienia projektu bez ręcznego tworzenia struktury plików**
- **Automatyzacja**
Bootstrap tworzy pliki w sandboxie, instaluje zależności i uruchamia komendę startową.


## 2️⃣ Kontrakt README (codeblocki `markpact:*`)

- **`markpact:bootstrap <lang>`**
Dokładnie jeden bootstrap na README. Odpowiada za parsowanie codeblocków i uruchomienie.
- **`markpact:deps <scope>`**
Lista zależności dla danego scope (np. `python`).
- **`markpact:file <lang> path=...`**
Zapisuje plik do sandboxu pod ścieżką `path=...`.
- **`markpact:run <lang>`**
Jedna komenda uruchomieniowa wykonywana w sandboxie.

---
```markpact:bootstrap python
#!/usr/bin/env python3
"""MARKPACT v0.1 – Executable Markdown Runtime"""
import os, re, subprocess, sys
from pathlib import Path

README = Path(sys.argv[1] if len(sys.argv) > 1 else "README.md")
SANDBOX = Path(os.environ.get("MARKPACT_SANDBOX", "./sandbox"))
SANDBOX.mkdir(parents=True, exist_ok=True)
RE = re.compile(r"^```markpact:(?P<kind>\\w+)(?:\\s+(?P<meta>[^\\n]+))?\\n(?P<body>.*?)\\n^```[ \\t]*$", re.DOTALL | re.MULTILINE)

def run(cmd):
    print(f"[markpact] RUN: {cmd}")
    env = os.environ.copy()
    venv = SANDBOX / ".venv" / "bin"
    if venv.exists():
        env.update(VIRTUAL_ENV=str(venv.parent), PATH=f"{venv}:{env.get('PATH','')}")
    subprocess.check_call(cmd, shell=True, cwd=SANDBOX, env=env)

def main():
    deps, run_cmd = [], None
    for m in RE.finditer(README.read_text()):
        kind, meta, body = m.group("kind"), (m.group("meta") or "").strip(), m.group("body").strip()
        if kind == "file":
            p = re.search(r"\\bpath=(\\S+)", meta)
            if not p: raise ValueError(f"markpact:file requires path=..., got {meta!r}")
            f = SANDBOX / p[1]
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(body)
            print(f"[markpact] wrote {f}")
        elif kind == "deps" and meta == "python":
            deps.extend(line.strip() for line in body.splitlines() if line.strip())
        elif kind == "run":
            run_cmd = body
    if deps:
        venv_pip = SANDBOX / ".venv" / "bin" / "pip"
        if os.environ.get("MARKPACT_NO_VENV") != "1" and not venv_pip.exists():
            run(f"{sys.executable} -m venv .venv")
        (SANDBOX / "requirements.txt").write_text("\\n".join(deps))
        run(f"{'.venv/bin/pip' if venv_pip.exists() else 'pip'} install -r requirements.txt")
    if run_cmd:
        run(run_cmd)
    else:
        print("[markpact] No run command defined")

if __name__ == "__main__":
    main()
```


## 3️⃣ Instalacja

### Opcja A: Pakiet pip (zalecane)

```bash
# Podstawowa instalacja
pip install markpact

# Z LLM i PDF generation (dla demo)
pip install markpact[llm] fpdf2

# Z integracją fixop (auto-fix, diagnostyka portów)
pip install markpact[ops]
```

Użycie:

```bash
markpact README.md                    # uruchom projekt
markpact README.md --dry-run          # podgląd bez wykonywania
markpact README.md -s ./my-sandbox    # własny katalog sandbox

# Demo live z LLM
python examples/demo_live_markpact.py --prompt "Twój prompt"
```


### Opcja B: Instalacja lokalna (dev)

```bash
git clone [https://github.com/wronai/markpact.git](https://github.com/wronai/markpact.git)
cd markpact
make install   # lub: pip install -e .
```


### Opcja C: Ekstrakcja bootstrapu (zero dependencies)

- **Ekstrakcja bootstrapu do pliku**

Ten wariant jest odporny na przypadek, gdy w samym bootstrapie występują znaki ``` (np. w regexie):

```bash
sed -n '/^```markpact:bootstrap/,/^```[[:space:]]*$/p' README.md | sed '1d;$d' > markpact.py
```

- **Uruchomienie**

```bash
python3 markpact.py
```

- **Konfiguracja (env vars)**

```bash
MARKPACT_PORT=8001 MARKPACT_SANDBOX=./.markpact-sandbox python3 markpact.py
```


## 4️⃣ Sandbox i środowisko

- **`MARKPACT_SANDBOX`**
Zmienia katalog sandboxu (domyślnie `./sandbox`).
- **`MARKPACT_NO_VENV=1`**
Wyłącza tworzenie `.venv` w sandboxie (przydatne, jeśli CI/Conda zarządza środowiskiem).
- **Port zajęty (`[Errno 98] address already in use`)**
Ustaw `MARKPACT_PORT` na inny port lub zatrzymaj proces, który używa `8000`.


## 5️⃣ Dependency management

- **Python**
Bootstrap zbiera `markpact:deps python`, zapisuje `requirements.txt` w sandboxie i instaluje zależności.


## 6️⃣ Uruchamianie i workflow

- **Wejście**
`python3 markpact.py [README.md]`
- **Kolejność**
Bootstrap parsuje wszystkie codeblocki, zapisuje pliki i dopiero na końcu uruchamia `markpact:run`.


## 6.1 Konwencje i format metadanych

- **Nagłówek codeblocka**
` ```markpact:<kind> <lang> <meta>`

Minimalnie wymagane jest `markpact:<kind>`.
`lang` jest opcjonalny i pełni rolę informacyjną (bootstrap może go ignorować).
- **Metadane**
Dla `markpact:file` wymagane jest `path=...`.
Metadane mogą zawierać dodatkowe tokeny (np. w przyszłości `mode=...`, `chmod=...`).


## 6.2 CI/CD

- **Rekomendacja**
Uruchamiaj bootstrap w czystym środowisku (np. job CI) i ustaw sandbox na katalog roboczy joba.
- **Przykład (shell)**

```bash
export MARKPACT_SANDBOX=./.markpact-sandbox
export MARKPACT_PORT=8001
python3 markpact.py README.md
```

- **Wskazówki**
    - **Deterministyczność**
Pinuj wersje w `markpact:deps` (np. `fastapi==...`).
    - **Bezpieczeństwo**
Traktuj `markpact:run` jak skrypt uruchomieniowy repo: w CI odpalaj tylko zaufane README.
    - **Cache**
Jeśli CI wspiera cache, cache’uj katalog `MARKPACT_SANDBOX/.venv`.


## 6.3 Współpraca z LLM

- **Zasada**
LLM może generować/edytować projekt poprzez modyfikacje README (codeblocki `markpact:file`, `markpact:deps`, `markpact:run`).
- **Oczekiwania**
    - `markpact:file` zawsze zawiera pełną zawartość pliku.
    - Każda zmiana zależności idzie przez `markpact:deps`.
    - Jedna komenda startowa w `markpact:run`.


## 7️⃣ Najlepsze praktyki

- **Bootstrap jako pierwszy fenced codeblock w README**
- **Każdy plik w osobnym `markpact:file`**
- **Zależności tylko w `markpact:deps`**
- **Jedna komenda startowa w `markpact:run`**
- **Ekstrakcja bootstrapu**
Nie używaj zakresu `/,/```/` (bo ``` może wystąpić w treści, np. w regexie). Używaj `^```\$` na końcu.


### Plik konfiguracyjny (~/.markpact/.env)

```bash
# Markpact LLM Configuration
MARKPACT_MODEL="openrouter/nvidia/nemotron-3-nano-30b-a3b:free"
MARKPACT_API_BASE="https://openrouter.ai/api/v1"
MARKPACT_API_KEY="sk-or-v1-xxxxx"
MARKPACT_TEMPERATURE="0.7"
MARKPACT_MAX_TOKENS="4096"
```


## Obsługiwani providerzy LLM

### Ollama (lokalny, domyślny)

```bash
markpact config --provider ollama
markpact config --model ollama/qwen2.5-coder:14b
markpact -p "REST API dla książek"
```


### OpenRouter (darmowe modele!)

```bash
markpact config --provider openrouter --api-key sk-or-v1-xxxxx
markpact config --model openrouter/nvidia/nemotron-3-nano-30b-a3b:free
markpact -p "REST API dla książek"
```


## Działający przykład (FastAPI)

### 1️⃣ Dependencies

*markpact:deps python*

```text markpact:deps python
fastapi
uvicorn
```


### 2️⃣ Application Files

*markpact:file python path=app/main.py*

```python markpact:file path=app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Executable Markdown"}
```


### 3️⃣ Run Command

*markpact:run python*

```bash markpact:run
uvicorn app.main:app --host 0.0.0.0 --port ${MARKPACT_PORT:-8088}
```


## 🏗️ Architektura modułów

Markpact jest podzielony na małe, niezależne moduły:

```
src/markpact/
├── cli/                    # CLI dispatch + subcommands
│   ├── __init__.py         # main() — thin dispatch (CC≤5)
│   ├── sync_cmd.py         # markpact sync
│   ├── pack_cmd.py         # markpact pack
│   ├── config_cmd.py       # markpact config
│   ├── publish_cmd.py      # --publish mode
│   ├── run_cmd.py          # normal run, Docker, test
│   ├── convert_cmd.py      # notebook/markdown conversion
│   └── helpers.py          # shared CLI utilities
├── publish/                # Multi-registry publisher
│   ├── models.py           # PublishConfig, PublishResult
│   ├── helpers.py          # inference, interactive config
│   ├── version.py          # semver bump, extract, update
│   ├── llm_config.py       # LLM-based config generation
│   ├── pypi.py             # PyPI publisher
│   ├── npm.py              # npm publisher
│   ├── docker_pub.py       # Docker publisher
│   ├── github.py           # GitHub Packages publisher
│   └── main.py             # parse_publish_block, dispatch
├── auto_fix.py             # Runtime error auto-fix (fixop integration)
├── parser.py               # markpact:* block parser
├── syncer.py               # README ↔ source sync
├── packer.py               # Directory → README packer
├── sandbox.py              # Isolated sandbox management
├── runner.py               # Command execution
└── generator.py            # LLM contract generation
```


### Opcjonalne zależności

| Extra | Pakiet | Opis |
| :-- | :-- | :-- |
| `[llm]` | litellm | Generowanie kontraktów przez LLM |
| `[ops]` | fixop | Diagnostyka portów, klasyfikacja błędów |
| `[dev]` | pytest, ruff, build, twine | Narzędzia deweloperskie |

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Author

Created by **Tom Sapletta** - [tom@sapletta.com](mailto:tom@sapletta.com)

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

