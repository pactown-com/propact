# Shell Upload Example

This example demonstrates how propact intelligently splits markdown content with audio attachments for shell/CLI endpoints.

## Content to Upload

![audio.mp3](audio.mp3)

```bash
# Upload metadata
title: "My Podcast Episode"
description: "An interesting discussion about technology"
duration: "45 minutes"
author: "John Doe"
```

Additional context: This is episode 5 of our tech podcast series, focusing on AI and machine learning trends.

## Expected Behavior

When run with propact, this markdown will be:
1. Parsed to extract the audio.mp3 file
2. Split into binary data (audio) and text metadata
3. Sent to shell endpoint with appropriate flags
4. Response converted back to markdown

## Run Command

```bash
propact README.md --endpoint "curl -X POST http://localhost:8080/upload"
```

## Schema

The shell endpoint expects:
- `--data-binary` for the audio file
- `--data` for JSON metadata
- Plain text as additional context
