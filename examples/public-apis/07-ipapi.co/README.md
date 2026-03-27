# Twoja lokalizacja IP

Sprawdź swoją publiczną adres IP i lokalizację geograficzną.

```json
{
  "query": "My IP location",
  "fields": ["ip", "city", "region", "country", "latitude", "longitude", "isp"]
}
```

**Free NO KEY**: https://ipapi.co/json/

## Usage

```bash
# Automatycznie wykrywa Twoje IP
propact 07-ipapi.co/README.md --endpoint "https://ipapi.co/json/"

# Lub sprawdź konkretne IP
propact 07-ipapi.co/README.md --endpoint "https://ipapi.co/8.8.8.8/json/"
```

## Expected Output

Output will be saved to `README.response.md`:

```markdown
# Twoja lokalizacja IP

🌍 **IP**: 203.0.113.1  
📍 **Lokalizacja**: Gdańsk, pomorskie, Poland  
📊 **Współrzędne**: 54.3520° N, 18.6466° E  

**Szczegóły**:
- **Kraj**: Poland (PL)
- **Region**: Pomeranian Voivodeship
- **Miasto**: Gdańsk
- **ISP**: Example ISP
- **Strefa czasowa**: Europe/Warsaw

🗺️ **Mapa**: [Otwórz w Google Maps](https://www.google.com/maps?q=54.3520,18.6466)
```
