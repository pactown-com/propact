# MCP Video Processing Example

This example shows how propact handles MCP (Model Context Protocol) tool calls with video attachments.

## Video Content

![demo.mp4](demo.mp4)

```python
# Video processing parameters
{
  "duration": 30,
  "format": "h264",
  "resolution": "1920x1080",
  "quality": "high",
  "effects": ["noise_reduction", "color_correction"]
}
```

Processing instructions: Extract the first 30 seconds, apply noise reduction and color correction, output in H.264 format.

## Expected Behavior

Propact will:
1. Register the video as an MCP resource
2. Call the video processor tool with specified parameters
3. Handle binary video data through MCP transport
4. Return processing results as markdown

## Run Command

```bash
propact README.md --endpoint "mcp://localhost:8080/video-tool"
```

## MCP Schema

The MCP tool provides:
- Resource: video file (binary)
- Tool: video_processor with parameters
- Response: Processing status and output file reference
