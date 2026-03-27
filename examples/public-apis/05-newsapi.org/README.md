# Najnowerski - Tech News

Sprawdź najnowerski artykuły o technologii z ostatnimi Trending.

```json
{
  "query": "Latest technology headlines",
  "category": "technology",
  "country": "us",
  "pageSize": 10
}
```

**Free API**: https://newsapi.org/v2/top-headlines

## Usage

```bash
# Demo (bez klucza - ogranicche API)
NEWS_API_KEY=demo propact 05-newsapi.org/README.md --endpoint "https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=demo"

# Real (z免费 API key)
NEWS_API_KEY=your_key propact 05-NewsAPI.org/README.md --endpoint "https://newsapi.org/v2/top-headlines?country=pl&category=technology"
```

## Expected Output

Output will be saved to `README.response.md`:

```markdown
# Tech News - Top Headlines

1. **AI Revolution Continues** - TechCrunch
   New breakthrough in LLM technology announced...
   
2. **Quantum Computing Milestone** - MIT News
   Researchers achieve 1000-qubit processor...

| Source | Title | Time |
|--------|-------|------|
| TechCrunch | AI Breakthrough | 2h ago |
| Wired | Quantum Leap | 4h ago |
```
