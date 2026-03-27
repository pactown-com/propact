#!/bin/bash

# Helper script for FFmpeg CLI example
echo "=== FFmpeg Audio Processing Example ==="
echo ""

# Create sample audio file (placeholder)
echo "Creating sample audio file..."
echo "FAKE PODCAST MP3 AUDIO DATA" > podcast.mp3

echo ""
echo "Running propact with FFmpeg CLI..."
echo "Note: This requires FFmpeg to be installed on your system"
echo ""

# Check for FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "Warning: FFmpeg not found. Install with: brew install ffmpeg (macOS) or apt install ffmpeg (Ubuntu)"
    echo ""
fi

# Run propact
python -m propact.cli README.md --endpoint "ffmpeg -i podcast.mp3 -c:a aac -b:a 128k -ar 44100 processed_podcast.aac"

echo ""
echo "✓ Example completed!"
echo "Check README.response.md for processing results"
echo ""

# Cleanup
echo "Cleaning up..."
rm -f podcast.mp3 processed_podcast.aac README.response.md
