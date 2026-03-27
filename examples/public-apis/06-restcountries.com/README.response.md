# Response from Propact

**Status:** 200

## JSON Response

```json

{
  "args": {
    "bash": "propact 06-restcountries.com/README.md --endpoint \"https://restcountries.com/v3.1/name/Poland?fullText=true\"",
    "json": "{\"country\": \"Poland\", \"fields\": [\"name\", \"capital\", \"population\", \"currency\", \"languages\", \"flag\"]}",
    "markdown": "# Poland - Country Information\n\n\ud83c\uddf5\ud83c\uddf1 **Flaga**: ![Flag](https://flagcdn.com/w320/pl.png)\n\n**Stolica**: Warszawa  \n**Populacja**: 37,950,000  \n**Waluta**: Polish z\u0142oty (PLN)  \n\n**J\u0119zyki**:\n- Polski (oficjalny)\n\n**Region**: Europa  \n**Subregion**: Wschodnia Europa  \n\n**Kody**:\n- ISO2: PL\n- ISO3: POL",
    "text": "# Dane o Polsce\n\nPobierz podstawowe informacje o Polsce z REST Countries API.\n\n\n\n**Free NO KEY**: https://restcountries.com/v3.1/name/Poland\n\n## Usage\n\n\n\n## Expected Output\n\nOutput will be saved to `README.response.md`:"
  },
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "httpbin.org",
    "User-Agent": "python-httpx/0.27.2",
    "X-Amzn-Trace-Id": "Root=1-69c6e787-448f01bc73de56a46333a019"
  },
  "origin": "83.20.192.207",
  "url": "https://httpbin.org/get?text=%23 Dane o Polsce\n\nPobierz podstawowe informacje o Polsce z REST Countries API.\n\n\n\n**Free NO KEY**%3A https%3A%2F%2Frestcountries.com%2Fv3.1%2Fname%2FPoland\n\n%23%23 Usage\n\n\n\n%23%23 Expected Output\n\nOutput will be saved to `README.response.md`%3A&json={\"country\"%3A \"Poland\"%2C \"fields\"%3A [\"name\"%2C \"capital\"%2C \"population\"%2C \"currency\"%2C \"languages\"%2C \"flag\"]}&bash=propact 06-restcountries.com%2FREADME.md --endpoint \"https%3A%2F%2Frestcountries.com%2Fv3.1%2Fname%2FPoland%3FfullText%3Dtrue\"&markdown=%23 Poland - Country Information\n\n\ud83c\uddf5\ud83c\uddf1 **Flaga**%3A ![Flag](https%3A%2F%2Fflagcdn.com%2Fw320%2Fpl.png)\n\n**Stolica**%3A Warszawa  \n**Populacja**%3A 37%2C950%2C000  \n**Waluta**%3A Polish z\u0142oty (PLN)  \n\n**J\u0119zyki**%3A\n- Polski (oficjalny)\n\n**Region**%3A Europa  \n**Subregion**%3A Wschodnia Europa  \n\n**Kody**%3A\n- ISO2%3A PL\n- ISO3%3A POL"
}

```

## Raw Response

```

{
  "args": {
    "bash": "propact 06-restcountries.com/README.md --endpoint \"https://restcountries.com/v3.1/name/Poland?fullText=true\"", 
    "json": "{\"country\": \"Poland\", \"fields\": [\"name\", \"capital\", \"population\", \"currency\", \"languages\", \"flag\"]}", 
    "markdown": "# Poland - Country Information\n\n\ud83c\uddf5\ud83c\uddf1 **Flaga**: ![Flag](https://flagcdn.com/w320/pl.png)\n\n**Stolica**: Warszawa  \n**Populacja**: 37,950,000  \n**Waluta**: Polish z\u0142oty (PLN)  \n\n**J\u0119zyki**:\n- Polski (oficjalny)\n\n**Region**: Europa  \n**Subregion**: Wschodnia Europa  \n\n**Kody**:\n- ISO2: PL\n- ISO3: POL", 
    "text": "# Dane o Polsce\n\nPobierz podstawowe informacje o Polsce z REST Countries API.\n\n\n\n**Free NO KEY**: https://restcountries.com/v3.1/name/Poland\n\n## Usage\n\n\n\n## Expected Output\n\nOutput will be saved to `README.response.md`:"
  }, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Host": "httpbin.org", 
...

```
