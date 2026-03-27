# Response from Propact

**Status:** 200

## JSON Response

```json

{
  "args": {
    "bash": "ALPHA_VANTAGE_KEY=demo propact examples/public-apis/03-stocks/README.md \\\n  --endpoint \"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA\"",
    "json": "{\"symbol\": \"TSLA\", \"function\": \"TIME_SERIES_DAILY\", \"query\": \"Latest price + 5-day change\"}",
    "text": "# Tesla Stock (TSLA)\n\nOstatnia cena + 5-day change.\n\n\n\n\n\n## Usage\n\n\n\n## Expected Output\n\nOutput will be saved to `README.response.md` with current stock price and changes."
  },
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "httpbin.org",
    "User-Agent": "python-httpx/0.27.2",
    "X-Amzn-Trace-Id": "Root=1-69c6e783-30b0502b317cb2c94a12db1a"
  },
  "origin": "83.20.192.207",
  "url": "https://httpbin.org/get?text=%23 Tesla Stock (TSLA)\n\nOstatnia cena %2B 5-day change.\n\n\n\n\n\n%23%23 Usage\n\n\n\n%23%23 Expected Output\n\nOutput will be saved to `README.response.md` with current stock price and changes.&json={\"symbol\"%3A \"TSLA\"%2C \"function\"%3A \"TIME_SERIES_DAILY\"%2C \"query\"%3A \"Latest price %2B 5-day change\"}&bash=ALPHA_VANTAGE_KEY%3Ddemo propact examples%2Fpublic-apis%2F03-stocks%2FREADME.md \\\n  --endpoint \"https%3A%2F%2Fwww.alphavantage.co%2Fquery%3Ffunction%3DTIME_SERIES_DAILY%26symbol%3DTSLA\""
}

```

## Raw Response

```

{
  "args": {
    "bash": "ALPHA_VANTAGE_KEY=demo propact examples/public-apis/03-stocks/README.md \\\n  --endpoint \"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA\"", 
    "json": "{\"symbol\": \"TSLA\", \"function\": \"TIME_SERIES_DAILY\", \"query\": \"Latest price + 5-day change\"}", 
    "text": "# Tesla Stock (TSLA)\n\nOstatnia cena + 5-day change.\n\n\n\n\n\n## Usage\n\n\n\n## Expected Output\n\nOutput will be saved to `README.response.md` with current stock price and changes."
  }, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "httpbin.org", 
    "User-Agent": "python-httpx/0.27.2", 
    "X-Amzn-Trace-Id": "Root=1-69c6e783-30b0502b317cb2c94a12db1a"
  }, 
  "origin": "83.20.192.207", 
  "url": "https://httpbin.org/get?text=%23 Tesla Stock (TSLA)\n\nOstatnia cena %2B 5-day change.\n\n\n\n\n\n%23%23 Usage\n\n\n\n%23%23 Expected Output\n\nOutput will be saved to `README.response.md` with current stock price and ...

```
