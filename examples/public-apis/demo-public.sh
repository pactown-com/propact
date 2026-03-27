#!/bin/bash
echo "🚀 Propact Public APIs Demo (Gdańsk, 2026)"
echo "========================================"

# Create responses directory
mkdir -p responses

echo "1. 🌤️ Pogoda:"
propact 01-weather/README.md --endpoint "https://api.openweathermap.org/data/2.5/weather?lat=54.35&lon=18.65&appid=demo"
echo "   → 01-weather/README.response.md"

echo "\n2. 💱 PLN → USD:"
propact 02-currency/README.md --endpoint "https://api.exchangerate.host/convert?from=PLN&to=USD&amount=1000"
echo "   → 02-currency/README.response.md"

echo "\n3. 📈 Tesla Stock:"
ALPHA_VANTAGE_KEY=demo propact 03-stocks/README.md --endpoint "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA"
echo "   → 03-stocks/README.response.md"

echo "\n4. 🪙 Bitcoin PLN:"
propact 04-crypto/README.md --endpoint "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=pln&include_24hr_change=true"
echo "   → 04-crypto/README.response.md"

echo "\n✅ Wszystkie responses w *.response.md !"
echo "\n📊 Podsumowanie:"
ls -1 */README.response.md 2>/dev/null || echo "   Brak responses (sprawdź połączenie)"

echo "\n🎉 Demo zakończone! Sprawdź pliki .response.md"
echo "\n💡 Tip: Skopiuj dowolny README.md i uruchom z własnym endpointem!"
