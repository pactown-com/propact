# PLN → USD/EUR

Ile dostanę za 1000 PLN dzisiaj?

```json
{
  "from": "PLN",
  "to": "USD,EUR",
  "amount": 1000
}
```

**Free NO KEY**: https://api.exchangerate.host/convert

## Usage

```bash
propact run examples/public-apis/02-currency/README.md --endpoint "https://api.exchangerate.host/convert"
```

## Expected Output

Output will be saved to `README.response.md`:

```markdown
# Kursy walut

**1000 PLN** = **$254.32 USD** | **€234.56 EUR**
*Rate z 2026-03-27*
```
