# Twitter/X Media Upload

This example demonstrates uploading media and posting tweets with images using Twitter's API v2.

## Content

![announcement.png](announcement.png)

```json
{
  "text": "Propact: Markdown speaks all APIs! 🚀 Universal transport for 100+ services. #AI #DevOps #API",
  "media": {"media_ids": ["UPLOAD_ID"]}
}
```

## Two-Step Process

### Step 1: Upload Media

```bash
# Upload media first to get media_id
propact README.md \
  --endpoint "https://upload.twitter.com/1.1/media/upload.json" \
  --header "Authorization: Bearer $TWITTER_BEARER"
```

### Step 2: Post Tweet

After getting `media_id` from step 1 response:

```bash
# Update the JSON with actual media_id and post tweet
propact README.md \
  --endpoint "https://api.twitter.com/2/tweets" \
  --header "Authorization: Bearer $TWITTER_BEARER"
```

## Expected Output

The response will include:
- Tweet ID
- Tweet text and creation time
- Media attachment details

## Environment Variables

```bash
TWITTER_BEARER=<YOUR_TWITTER_BEARER_TOKEN>
```

## Requirements

- Twitter Developer account with elevated access
- Bearer token from Twitter Developer Portal
- Image file (announcement.png) in the same directory
