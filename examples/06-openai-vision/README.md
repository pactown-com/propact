# OpenAI Vision Analysis Example

This example demonstrates propact's ability to send images with analysis requests to OpenAI's Vision API.

## Medical Image for Analysis

![medical_scan.png](medical_scan.png)

```json
{
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Analyze this medical X-ray image. Identify any abnormalities, measure key indicators, and provide a detailed assessment."
        },
        {
          "type": "image_url",
          "image_url": "medical_scan.png"
        }
      ]
    }
  ],
  "max_tokens": 500,
  "temperature": 0.2
}
```

Additional context: This is a chest X-ray of a 45-year-old female patient undergoing routine examination. Please focus on lung health and any signs of pneumonia or other conditions.

## Expected Behavior

Propact will:
1. Extract the medical image and JSON analysis request
2. Convert to OpenAI API multipart format
3. Send to OpenAI Vision API
4. Receive and format the analysis as markdown

## Run Command

```bash
propact README.md --endpoint "https://api.openai.com/v1/chat/completions" --schema openapi.json
```

## OpenAPI Schema

The OpenAI Vision API expects:
- POST /v1/chat/completions
- Content-Type: application/json
- Image data as base64 in message content
- Analysis parameters in JSON format
