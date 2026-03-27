# Pogoda w Gdańsku

Sprawdź aktualną pogodę i prognozę dla lat 54.35, lon 18.65.

```json
{
  "query": "Current weather + 5-day forecast",
  "location": "Gdańsk, PL"
}
```

**Free API**: https://api.openweathermap.org/data/2.5/weather

## Usage

### Demo CLI (zero key dla basic):
```bash
# Free tier (bez klucza dla demo)
propact run examples/public-apis/01-weather/README.md --endpoint "https://api.openweathermap.org/data/2.5/weather?lat=54.35&lon=18.65&appid=demo"

# Real (z kluczem)
OPENWEATHER_API_KEY=abc123 propact run examples/public-apis/01-weather/README.md --endpoint "https://api.openweathermap.org/data/2.5/onecall"
```

## Expected Output

Output will be saved to `README.response.md`:

```markdown
# Pogoda Gdańsk

**Temp**: 8°C, **Wilgotność**: 82%
**Prognoza**:
| Godzina | Temp | Opady |
|---------|------|-------|
| 20:00  | 7°C | 0.2mm|
```
