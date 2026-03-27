# Tesla Stock (TSLA)

Ostatnia cena + 5-day change.

![tsla_chart.png](tsla_chart.png)

```json
{
  "symbol": "TSLA",
  "function": "TIME_SERIES_DAILY",
  "query": "Latest price + 5-day change"
}
```

## Usage

```bash
ALPHA_VANTAGE_KEY=demo propact examples/public-apis/03-stocks/README.md \
  --endpoint "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA"
```

## Expected Output

Output will be saved to `README.response.md` with current stock price and changes.
