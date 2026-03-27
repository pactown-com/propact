#!/bin/bash
set -e

echo "🚀 Propact Public APIs Demo (Gdańsk, 2026)"
echo "========================================"

# Detect propact command
if command -v propact &> /dev/null; then
    PROACT_CMD="propact"
elif command -v poetry &> /dev/null; then
    PROACT_CMD="poetry run propact"
else
    PROACT_CMD="python -m propact.cli"
fi

echo "Using: $PROACT_CMD"
echo ""

# Create responses directory
mkdir -p responses

echo "1. 🌤️ Pogoda:"
$PROACT_CMD run 01-weather/README.md --endpoint "https://api.openweathermap.org/data/2.5/weather?lat=54.35&lon=18.65&appid=demo" || echo "   ⚠️  Weather API call failed"
echo "   → 01-weather/README.response.md"
echo ""

echo "2. 💱 PLN → USD:"
$PROACT_CMD run 02-currency/README.md --endpoint "https://api.exchangerate.host/convert?from=PLN&to=USD&amount=1000" || echo "   ⚠️  Currency API call failed"
echo "   → 02-currency/README.response.md"
echo ""

echo "3. 📈 Tesla Stock:"
ALPHA_VANTAGE_KEY=demo $PROACT_CMD run 03-stocks/README.md --endpoint "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA" || echo "   ⚠️  Stock API call failed"
echo "   → 03-stocks/README.response.md"
echo ""

echo "4. 🪙 Bitcoin PLN:"
$PROACT_CMD run 04-crypto/README.md --endpoint "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=pln&include_24hr_change=true" || echo "   ⚠️  Crypto API call failed"
echo "   → 04-crypto/README.response.md"
echo ""

echo "✅ Wszystkie responses w *.response.md !"
echo ""
echo "📊 Podsumowanie:"
ls -1 */README.response.md 2>/dev/null || echo "   Brak responses (sprawdź połączenie)"
echo ""
echo "🎉 Demo zakończone! Sprawdź pliki .response.md"
echo ""
echo "💡 Tip: Skopiuj dowolny README.md i uruchom z własnym endpointem!"
