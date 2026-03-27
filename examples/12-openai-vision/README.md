# OpenAI Vision Analysis

This example demonstrates how to use propact with OpenAI's Vision API to analyze images using GPT-4o.

## Content

![xray.png](xray.png)

```json
{
  "model": "gpt-4o",
  "messages": [{
    "role": "user", 
    "content": [
      {"type": "text", "text": "Analyze this X-ray for abnormalities. Provide a detailed medical assessment."},
      {"type": "image_url", "image_url": {"url": "data:image/png;base64,BASE64"}}
    ]
  }],
  "max_tokens": 500,
  "temperature": 0.2
}
```

Patient: 45-year-old female, routine check-up. History: No prior conditions.

## Expected Output

The response will include:
- Medical analysis of the X-ray
- Confidence score for findings
- Recommendations for follow-up if needed

## Run Command

```bash
propact README.md \
  --endpoint "https://api.openai.com/v1/chat/completions" \
  --header "Authorization: Bearer $OPENAI_API_KEY"
```

## Environment Variables

```bash
OPENAI_API_KEY=sk-...
```

## Requirements

- OpenAI API key with access to GPT-4o vision model
- Valid image file (xray.png) in the same directory
