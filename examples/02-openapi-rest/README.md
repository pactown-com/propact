# OpenAPI Image Analysis Example

This example demonstrates propact's schema-aware content splitting for REST APIs with OpenAPI specifications.

## Content to Analyze

![medical_scan.png](medical_scan.png)

```json
{
  "prompt": "Analyze this medical image for abnormalities",
  "model": "gpt-4-vision",
  "detail": "high",
  "features": ["anomaly_detection", "measurement", "comparison"]
}
```

Patient information: 45-year-old female, routine check-up. History: No prior conditions.

## Expected Behavior

Propact will:
1. Parse the OpenAPI schema to understand the /analyze endpoint
2. Split content into multipart/form-data with file and JSON fields
3. Send to the API with correct content-type
4. Convert JSON response to markdown with codeblocks

## Run Command

```bash
propact README.md --endpoint "https://api.vision.ai/v1/analyze" --schema openapi.json
```

## OpenAPI Schema

The API expects:
- POST /analyze
- multipart/form-data with:
  - file: Image file
  - json: Analysis parameters
