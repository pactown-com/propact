# Dane o Polsce

Pobierz podstawowe informacje o Polsce z REST Countries API.

```json
{
  "country": "Poland",
  "fields": ["name", "capital", "population", "currency", "languages", "flag"]
}
```

**Free NO KEY**: https://restcountries.com/v3.1/name/Poland

## Usage

```bash
propact 06-restcountries.com/README.md --endpoint "https://restcountries.com/v3.1/name/Poland?fullText=true"
```

## Expected Output

Output will be saved to `README.response.md`:

```markdown
# Poland - Country Information

🇵🇱 **Flaga**: ![Flag](https://flagcdn.com/w320/pl.png)

**Stolica**: Warszawa  
**Populacja**: 37,950,000  
**Waluta**: Polish złoty (PLN)  

**Języki**:
- Polski (oficjalny)

**Region**: Europa  
**Subregion**: Wschodnia Europa  

**Kody**:
- ISO2: PL
- ISO3: POL
```
