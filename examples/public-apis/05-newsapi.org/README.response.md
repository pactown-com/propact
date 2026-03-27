# Response from Propact

**Status:** 200

## JSON Response

```json

{
  "args": {
    "bash": "# Demo (bez klucza - ogranicche API)\nNEWS_API_KEY=demo propact 05-newsapi.org/README.md --endpoint \"https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=demo\"\n\n# Real (z\u514d\u8d39 API key)\nNEWS_API_KEY=your_key propact 05-NewsAPI.org/README.md --endpoint \"https://newsapi.org/v2/top-headlines?country=pl&category=technology\"",
    "json": "{\"query\": \"Latest technology headlines\", \"category\": \"technology\", \"country\": \"us\", \"pageSize\": 10}",
    "markdown": "# Tech News - Top Headlines\n\n1. **AI Revolution Continues** - TechCrunch\n   New breakthrough in LLM technology announced...\n   \n2. **Quantum Computing Milestone** - MIT News\n   Researchers achieve 1000-qubit processor...\n\n| Source | Title | Time |\n|--------|-------|------|\n| TechCrunch | AI Breakthrough | 2h ago |\n| Wired | Quantum Leap | 4h ago |",
    "text": "# Najnowerski - Tech News\n\nSprawd\u017a najnowerski artyku\u0142y o technologii z ostatnimi Trending.\n\n\n\n**Free API**: https://newsapi.org/v2/top-headlines\n\n## Usage\n\n\n\n## Expected Output\n\nOutput will be saved to `README.response.md`:"
  },
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "httpbin.org",
    "User-Agent": "python-httpx/0.27.2",
    "X-Amzn-Trace-Id": "Root=1-69c6e785-62a1d10f051802fa2d0162b5"
  },
  "origin": "83.20.192.207",
  "url": "https://httpbin.org/get?text=%23 Najnowerski - Tech News\n\nSprawd\u017a najnowerski artyku\u0142y o technologii z ostatnimi Trending.\n\n\n\n**Free API**%3A https%3A%2F%2Fnewsapi.org%2Fv2%2Ftop-headlines\n\n%23%23 Usage\n\n\n\n%23%23 Expected Output\n\nOutput will be saved to `README.response.md`%3A&json={\"query\"%3A \"Latest technology headlines\"%2C \"category\"%3A \"technology\"%2C \"country\"%3A \"us\"%2C \"pageSize\"%3A 10}&bash=%23 Demo (bez klucza - ogranicche API)\nNEWS_API_KEY%3Ddemo propact 05-newsapi.org%2FREADME.md --endpoint \"https%3A%2F%2Fnewsapi.org%2Fv2%2Ftop-headlines%3Fcountry%3Dus%26category%3Dtechnology%26apiKey%3Ddemo\"\n\n%23 Real (z\u514d\u8d39 API key)\nNEWS_API_KEY%3Dyour_key propact 05-NewsAPI.org%2FREADME.md --endpoint \"https%3A%2F%2Fnewsapi.org%2Fv2%2Ftop-headlines%3Fcountry%3Dpl%26category%3Dtechnology\"&markdown=%23 Tech News - Top Headlines\n\n1. **AI Revolution Continues** - TechCrunch\n   New breakthrough in LLM technology announced...\n   \n2. **Quantum Computing Milestone** - MIT News\n   Researchers achieve 1000-qubit processor...\n\n| Source | Title | Time |\n|--------|-------|------|\n| TechCrunch | AI Breakthrough | 2h ago |\n| Wired | Quantum Leap | 4h ago |"
}

```

## Raw Response

```

{
  "args": {
    "bash": "# Demo (bez klucza - ogranicche API)\nNEWS_API_KEY=demo propact 05-newsapi.org/README.md --endpoint \"https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey=demo\"\n\n# Real (z\u514d\u8d39 API key)\nNEWS_API_KEY=your_key propact 05-NewsAPI.org/README.md --endpoint \"https://newsapi.org/v2/top-headlines?country=pl&category=technology\"", 
    "json": "{\"query\": \"Latest technology headlines\", \"category\": \"technology\", \"country\": \"us\", \"pageSize\": 10}", 
    "markdown": "# Tech News - Top Headlines\n\n1. **AI Revolution Continues** - TechCrunch\n   New breakthrough in LLM technology announced...\n   \n2. **Quantum Computing Milestone** - MIT News\n   Researchers achieve 1000-qubit processor...\n\n| Source | Title | Time |\n|--------|-------|------|\n| TechCrunch | AI Breakthrough | 2h ago |\n| Wired | Quantum Leap | 4h ago |", 
    "text": "# Najnowerski - Tech News\n\nSprawd\u017a najnowerski artyku\u0142y o technologii z ostat...

```
