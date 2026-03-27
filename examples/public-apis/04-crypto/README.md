# Bitcoin Price

Aktualna cena BTC w PLN + 24h change.

```json
{
  "ids": "bitcoin",
  "vs_currencies": "pln",
  "include_24hr_change": "true"
}
```

**Free NO KEY**: https://api.coingecko.com/api/v3/simple/price

## Usage

```bash
propact run examples/public-apis/04-crypto/README.md --endpoint "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=pln&include_24hr_change=true"
```

## Expected Output

Output will be saved to `README.response.md`:

```markdown
# Bitcoin Price

**1 BTC** = **₽285,000 PLN** 
**24h change**: +2.34% 📈
```
