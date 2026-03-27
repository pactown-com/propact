# 🌟 Propact Public APIs – Zero Config Demo!

## Szybki start (NO KEYS!)

```bash
make public-demo  # Uruchom wszystko
```

## Real-time Gdańsk Weather

![pogoda.png](pogoda.png)  ← Auto-update!

| Service | Endpoint | Response |
| :-- | :-- | :-- |
| Weather | OpenWeather | 8°C ☀️ |
| Currency | ExchangeRate | 1PLN=\$0.25 |
| Crypto | CoinGecko | BTC=₽285k |

**Kliknij "Run All" → patrz magię!**

## 📁 Przykłady do skopiowania

```bash
# Każdy przykład to 1 plik MD + 1 komenda
cp 01-weather/README.md moje-pogoda.md
propact moje-pogoda.md --endpoint "https://..."

# Wynik zawsze w moje-pogoda.response.md
```

## 🌐 Więcej publicznych API (gotowe MD)

```
05-newsapi.org      # Headlines
06-restcountries.com # Countries data
07-ipapi.co         # IP geolocation
08-dadjokeapi.com   # Jokes 😄
09-quotes.rest      # Inspirational quotes
10-cat-fact.herokuapp # Cat facts 🐱
```

## 🎥 Video Demo Flow

1. User kopiuje examples/01-weather/README.md
2. Terminal: propact README.md --endpoint "..."
3. 3s → README.response.md z pogodą + tabelą
4. Copy-paste do Slack/Notion/Discord
5. Magia! 📊

## 🔑 Public API keys (.env.demo)

```bash
# Free tiers (demo only)
OPENWEATHER_APPID=demo
ALPHA_VANTAGE_KEY=demo

# Reszta NO KEY!
```

## 🚀 Szybkie komendy

```bash
# Pogoda Gdańsk
propact 01-weather/README.md --endpoint "https://api.openweathermap.org/data/2.5/weather?lat=54.35&lon=18.65&appid=demo"

# Kursy walut
propact 02-currency/README.md --endpoint "https://api.exchangerate.host/convert?from=PLN&to=USD&amount=1000"

# Bitcoin PLN
propact 04-crypto/README.md --endpoint "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=pln"
```

**Propact Public Demo** = **"Copy MD → Run → Magic MD response"**. **Idealny onboarding** dla userów – **pokazuje prostotę** na otwartych API! 🌤️💱📈
