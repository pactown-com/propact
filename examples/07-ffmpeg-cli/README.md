# FFmpeg Audio Processing Example

This example demonstrates propact's ability to process audio files through FFmpeg CLI with markdown-based configuration.

## Audio File to Process

![podcast.mp3](podcast.mp3)

```bash
# FFmpeg processing command
Convert to AAC format with 128k bitrate
Add metadata: title, artist, album
Normalize audio levels
```

Additional processing instructions:
- Target format: AAC (Advanced Audio Coding)
- Bitrate: 128 kbps
- Sample rate: 44.1 kHz
- Output filename: processed_podcast.aac
- Metadata to include:
  - Title: "Tech Talk Episode 42"
  - Artist: "Tech Podcast Network"
  - Album: "Tech Talks 2024"
  - Year: 2024

## Expected Behavior

Propact will:
1. Extract the audio file and processing instructions
2. Build FFmpeg command with appropriate parameters
3. Execute the conversion
4. Return processing results and file information

## Run Command

```bash
propact README.md --endpoint "ffmpeg -i podcast.mp3 -c:a aac -b:a 128k -ar 44100 processed_podcast.aac"
```

## Shell Schema

FFmpeg CLI expects:
- Input file specified with -i flag
- Output codec with -c:a flag
- Bitrate with -b:a flag
- Sample rate with -ar flag
- Output filename as last argument
