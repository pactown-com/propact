# Response from Propact

**Status:** 200

## JSON Response

```json

{
  "args": {
    "bash": "# Free tier (bez klucza dla demo)\npropact examples/public-apis/01-weather/README.md --endpoint \"https://api.openweathermap.org/data/2.5/weather?lat=54.35&lon=18.65&appid=demo\"\n\n# Real (z kluczem)\nOPENWEATHER_API_KEY=abc123 propact examples/public-apis/01-weather/README.md --endpoint \"https://api.openweathermap.org/data/2.5/onecall\"",
    "json": "{\"query\": \"Current weather + 5-day forecast\", \"location\": \"Gda\\u0144sk, PL\"}",
    "markdown": "# Pogoda Gda\u0144sk\n\n**Temp**: 8\u00b0C, **Wilgotno\u015b\u0107**: 82%\n**Prognoza**:\n| Godzina | Temp | Opady |\n|---------|------|-------|\n| 20:00  | 7\u00b0C | 0.2mm|",
    "text": "# Pogoda w Gda\u0144sku\n\nSprawd\u017a aktualn\u0105 pogod\u0119 i prognoz\u0119 dla lat 54.35, lon 18.65.\n\n\n\n**Free API**: https://api.openweathermap.org/data/2.5/weather\n\n## Usage\n\n### Demo CLI (zero key dla basic):\n\n\n## Expected Output\n\nOutput will be saved to `README.response.md`:"
  },
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "httpbin.org",
    "User-Agent": "python-httpx/0.27.2",
    "X-Amzn-Trace-Id": "Root=1-69c6e781-7c99b3033803b7721ea2a6bc"
  },
  "origin": "83.20.192.207",
  "url": "https://httpbin.org/get?text=%23 Pogoda w Gda\u0144sku\n\nSprawd\u017a aktualn\u0105 pogod\u0119 i prognoz\u0119 dla lat 54.35%2C lon 18.65.\n\n\n\n**Free API**%3A https%3A%2F%2Fapi.openweathermap.org%2Fdata%2F2.5%2Fweather\n\n%23%23 Usage\n\n%23%23%23 Demo CLI (zero key dla basic)%3A\n\n\n%23%23 Expected Output\n\nOutput will be saved to `README.response.md`%3A&json={\"query\"%3A \"Current weather %2B 5-day forecast\"%2C \"location\"%3A \"Gda\\u0144sk%2C PL\"}&bash=%23 Free tier (bez klucza dla demo)\npropact examples%2Fpublic-apis%2F01-weather%2FREADME.md --endpoint \"https%3A%2F%2Fapi.openweathermap.org%2Fdata%2F2.5%2Fweather%3Flat%3D54.35%26lon%3D18.65%26appid%3Ddemo\"\n\n%23 Real (z kluczem)\nOPENWEATHER_API_KEY%3Dabc123 propact examples%2Fpublic-apis%2F01-weather%2FREADME.md --endpoint \"https%3A%2F%2Fapi.openweathermap.org%2Fdata%2F2.5%2Fonecall\"&markdown=%23 Pogoda Gda\u0144sk\n\n**Temp**%3A 8\u00b0C%2C **Wilgotno\u015b\u0107**%3A 82%25\n**Prognoza**%3A\n| Godzina | Temp | Opady |\n|---------|------|-------|\n| 20%3A00  | 7\u00b0C | 0.2mm|"
}

```

## Raw Response

```

{
  "args": {
    "bash": "# Free tier (bez klucza dla demo)\npropact examples/public-apis/01-weather/README.md --endpoint \"https://api.openweathermap.org/data/2.5/weather?lat=54.35&lon=18.65&appid=demo\"\n\n# Real (z kluczem)\nOPENWEATHER_API_KEY=abc123 propact examples/public-apis/01-weather/README.md --endpoint \"https://api.openweathermap.org/data/2.5/onecall\"", 
    "json": "{\"query\": \"Current weather + 5-day forecast\", \"location\": \"Gda\\u0144sk, PL\"}", 
    "markdown": "# Pogoda Gda\u0144sk\n\n**Temp**: 8\u00b0C, **Wilgotno\u015b\u0107**: 82%\n**Prognoza**:\n| Godzina | Temp | Opady |\n|---------|------|-------|\n| 20:00  | 7\u00b0C | 0.2mm|", 
    "text": "# Pogoda w Gda\u0144sku\n\nSprawd\u017a aktualn\u0105 pogod\u0119 i prognoz\u0119 dla lat 54.35, lon 18.65.\n\n\n\n**Free API**: https://api.openweathermap.org/data/2.5/weather\n\n## Usage\n\n### Demo CLI (zero key dla basic):\n\n\n## Expected Output\n\nOutput will be saved to `README.response.md`:"
  }, 
  "headers"...

```
