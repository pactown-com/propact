# YouTube Video Metadata

This example demonstrates setting metadata for YouTube video uploads using propact.

## Content

```json
{
  "snippet": {
    "title": "Propact Demo 2026: Universal Markdown Transport",
    "description": "Propact enables universal markdown transport for 100+ APIs including OpenAI, Slack, Discord, GitHub, and more. No custom code needed - just write markdown with embedded media and JSON!",
    "tags": ["propact", "markdown", "api", "transport", "universal", "integration"],
    "categoryId": "28"
  },
  "status": {
    "privacyStatus": "private",
    "embeddable": true,
    "license": "youtube"
  },
  "contentDetails": {
    "caption": "false",
    "definition": "hd",
    "projection": "rectangular"
  }
}
```

## Expected Output

The response will include:
- Video ID
- Upload status
- Metadata confirmation

## Run Command

```bash
propact README.md \
  --endpoint "https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails" \
  --header "Authorization: Bearer $YOUTUBE_ACCESS_TOKEN" \
  --header "Content-Type: application/json"
```

## Environment Variables

```bash
YOUTUBE_ACCESS_TOKEN=ya29.your-youtube-access-token
```

## Requirements

- Google Cloud project with YouTube Data API enabled
- OAuth 2.0 credentials for YouTube
- Access token with appropriate scopes

## Note

This example only sets metadata. Actual video upload requires resumable upload protocol which is more complex. Use YouTube Studio for initial upload, then update metadata with propact.
