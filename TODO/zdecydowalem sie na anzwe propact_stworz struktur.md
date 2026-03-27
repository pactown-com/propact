<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# zdecydowalem sie na anzwe  propact

stworz strukture projektu i plan jego utworzenia

**Propact** (Protocol Pact) to doskonała nazwa – krótka, chwytliwa, opisuje **pakt protokołów** via Markdown. Poniżej pełna struktura projektu i **krok-po-kroku plan utworzenia** (nowoczesny Python 2026 stack: pyproject.toml, Poetry, Ruff, GitHub Actions).[^1][^2]

## 📁 Struktura projektu Propact

```
propact/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Testy + lint + build
│       ├── release.yml         # PyPI auto-release
│       └── docs.yml            # Docs deploy
├── docs/
│   ├── api.md                  # Auto-generated API docs
│   └── usage.md                # Przykłady Markdown contracts
├── examples/
│   ├── README.md               # ![logo.png] + ```propact:shell```
│   ├── shell-to-mcp/
│   └── rest-ws-proxy/
├── src/
│   └── propact/
│       ├── __init__.py         # __version__ = "0.1.0"
│       ├── core.py             # ToonPact class (150 LOC)
│       ├── parser.py           # ![file.png] + ```propact:*``` 
│       ├── protocols/
│       │   ├── __init__.py
│       │   ├── shell.py
│       │   ├── mcp.py
│       │   ├── rest.py
│       │   └── ws.py
│       └── attachments.py      # Binary handling
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_protocols.py
│   └── fixtures/               # Test README.md files
├── .gitignore
├── LICENSE                     # Apache-2.0 (jak Markpact)
├── README.md                   # ![logo.png] demo + badges
├── pyproject.toml              # Poetry + tools config
├── poetry.lock
└── Makefile                    # make test lint dev
```


## 📋 **Plan utworzenia (15 min → MVP)**

### **Krok 1: Init repo (2 min)**

```bash
mkdir propact && cd propact
git init
git switch -c main
```


### **Krok 2: pyproject.toml (3 min)**

```toml
[tool.poetry]
name = "propact"
version = "0.1.0"
description = "Protocol Pact: Universal Markdown for Shell/MCP/REST/WS"
authors = ["Tom Sapletta <tom@sapletta.com>"]
license = "Apache-2.0"
readme = "README.md"
repository = "https://github.com/wronai/propact"

[tool.poetry.dependencies]
python = "^3.10"
rich = "^13.7"
markdown = "^3.6"
pydantic = {extras = ["email"], version = "^2.8"}
httpx = "^0.27"
mcp-python-sdk = "^1.0"  # MCP
pytoony = "^0.1"          # Toon

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "B", "Q", "I", "N", "S", "T20"]
ignore = ["B008"]  # No eval

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
```


### **Krok 3: Core biblioteka (5 min)**

Skopiuj `ToonPact` class z poprzedniej odpowiedzi do `src/propact/core.py`.

### **Krok 4: README.md z demo (3 min)**

```markdown
# Propact 🚀 Protocol Pact via Markdown

[![PyPI](https://img.shields.io/pypi/v/propact.svg)](https://pypi.org/project/propact/)
[![Python](https://img.shields.io/pypi/pyversions/propact.svg)](https://pypi.org/project/propact/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

**Markdown mówi wszystkimi protokołami!** Shell → MCP → REST/WS bez konwersji.

![demo.png](demo.png)  <!-- Auto-transfer -->

```bash
pip install propact
propact README.md  # Uruchom ten plik!
```


## 🚀 Szybki start

```propact:shell
echo "Shell → MCP → REST pipeline works!"
```

```

### **Krok 5: GitHub Actions (2 min)**
`.github/workflows/ci.yml`:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with: {python-version: "3.12"}
    - run: make install test lint
```


### **Krok 6: Makefile (1 min)**

```makefile
.PHONY: install dev test lint clean

install:
	poetry install

dev:
	poetry install --with dev

test:
	poetry run pytest -vv

lint:
	poetry run ruff check src/ tests/
	poetry run ruff format src/ tests/

publish:
	poetry publish --build
```


### **Krok 7: Init i push (1 min)**

```bash
poetry install
make dev
make test lint
git add .
git commit -m "feat: initial Propact MVP"
git push origin main
gh repo create wronai/propact --public --push
```


## 🎯 **Następne kroki (Day 2)**

1. **Tests**: `test_core.py` z fixture README.md
2. **Examples**: Folder z `shell-to-mcp/README.md`
3. **Docs**: MkDocs + `make docs`
4. **PyPI**: `poetry publish` po tag v0.1.0
5. **Markpact integration**: `propact --markpact README.md`

## 📦 **Badges gotowe**

```
PyPI: propact | Python 3.10+ | Ruff | Tests | Apache-2.0
```

**MVP ready w 15 min!** 🚀 Potem dodaj WS, advanced attachments. Pasuje idealnie do twojego Markpact ecosystem.[^1]
<span style="display:none">[^10][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://github.com/habedi/template-python-library

[^2]: https://realpython.com/python-pyproject-toml/

[^3]: https://towardsdatascience.com/how-to-spin-up-a-project-structure-with-cookiecutter/

[^4]: https://pycon.switowski.com/03-project-structure-2-parts/cookiecutter/

[^5]: https://github.com/matthewfeickert/Python-library-template

[^6]: https://inventivehq.com/blog/pyproject-toml-complete-guide

[^7]: https://aeturrell.com/blog/posts/ultra-modern-python-cookiecutters/

[^8]: https://github.com/Python-templates

[^9]: https://dev.to/ldrscke/hypermodernize-your-python-package-3d9m

[^10]: https://www.reddit.com/r/Python/comments/1lcz532/a_modern_python_project_cookiecutter_template/

