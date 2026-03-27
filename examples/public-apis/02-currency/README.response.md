# Response from Propact

**Status:** 200

## JSON Response

```json

{
  "args": {
    "bash": "propact run examples/public-apis/02-currency/README.md --endpoint \"https://api.exchangerate.host/convert\"",
    "json": "{\"from\": \"PLN\", \"to\": \"USD,EUR\", \"amount\": 1000}",
    "markdown": "# Kursy walut\n\n**1000 PLN** = **$254.32 USD** | **\u20ac234.56 EUR**\n*Rate z 2026-03-27*",
    "text": "# PLN \u2192 USD/EUR\n\nIle dostan\u0119 za 1000 PLN dzisiaj?\n\n\n\n**Free NO KEY**: https://api.exchangerate.host/convert\n\n## Usage\n\n\n\n## Expected Output\n\nOutput will be saved to `README.response.md`:"
  },
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "httpbin.org",
    "User-Agent": "python-httpx/0.27.2",
    "X-Amzn-Trace-Id": "Root=1-69c6e8ed-1f7115362efb92ee2af2d535"
  },
  "origin": "83.20.192.207",
  "url": "https://httpbin.org/get?text=%23 PLN \u2192 USD%2FEUR\n\nIle dostan\u0119 za 1000 PLN dzisiaj%3F\n\n\n\n**Free NO KEY**%3A https%3A%2F%2Fapi.exchangerate.host%2Fconvert\n\n%23%23 Usage\n\n\n\n%23%23 Expected Output\n\nOutput will be saved to `README.response.md`%3A&json={\"from\"%3A \"PLN\"%2C \"to\"%3A \"USD%2CEUR\"%2C \"amount\"%3A 1000}&bash=propact run examples%2Fpublic-apis%2F02-currency%2FREADME.md --endpoint \"https%3A%2F%2Fapi.exchangerate.host%2Fconvert\"&markdown=%23 Kursy walut\n\n**1000 PLN** %3D **%24254.32 USD** | **\u20ac234.56 EUR**\n*Rate z 2026-03-27*"
}

```

## Raw Response

```

{
  "args": {
    "bash": "propact run examples/public-apis/02-currency/README.md --endpoint \"https://api.exchangerate.host/convert\"", 
    "json": "{\"from\": \"PLN\", \"to\": \"USD,EUR\", \"amount\": 1000}", 
    "markdown": "# Kursy walut\n\n**1000 PLN** = **$254.32 USD** | **\u20ac234.56 EUR**\n*Rate z 2026-03-27*", 
    "text": "# PLN \u2192 USD/EUR\n\nIle dostan\u0119 za 1000 PLN dzisiaj?\n\n\n\n**Free NO KEY**: https://api.exchangerate.host/convert\n\n## Usage\n\n\n\n## Expected Output\n\nOutput will be saved to `README.response.md`:"
  }, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "httpbin.org", 
    "User-Agent": "python-httpx/0.27.2", 
    "X-Amzn-Trace-Id": "Root=1-69c6e8ed-1f7115362efb92ee2af2d535"
  }, 
  "origin": "83.20.192.207", 
  "url": "https://httpbin.org/get?text=%23 PLN \u2192 USD%2FEUR\n\nIle dostan\u0119 za 1000 PLN dzisiaj%3F\n\n\n\n**Free NO KEY**%3A https%3A%2F%2Fapi.exchangerate.host%2Fconvert\n\n%23%23 Usage...

```
