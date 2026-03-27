# Discord File Message

This example demonstrates sending files and messages to Discord channels using propact.

## Content

![dashboard.png](dashboard.png)

```json
{
  "content": "📊 Dashboard update via Propact",
  "tts": false
}
```

## Expected Output

The response will include:
- Message ID
- Attachment URLs
- Channel and guild information

## Run Command

```bash
propact README.md \
  --endpoint "https://discord.com/api/v10/channels/$DISCORD_CHANNEL_ID/messages" \
  --header "Authorization: Bot $DISCORD_TOKEN"
```

## Environment Variables

```bash
DISCORD_TOKEN=<YOUR_DISCORD_BOT_TOKEN>
DISCORD_CHANNEL_ID=<YOUR_CHANNEL_ID>
```

## Requirements

- Discord bot created at https://discord.com/developers/applications
- Bot token with message sending permissions
- Channel ID where the bot has permissions
- Image file (dashboard.png) in the same directory
