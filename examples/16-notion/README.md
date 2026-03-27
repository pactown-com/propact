# Notion Page Creation

This example demonstrates creating Notion pages with rich content blocks and file attachments using propact.

## Content

![cover.jpg](cover.jpg)

```json
{
  "parent": {"database_id": "DATABASE_ID"},
  "properties": {
    "Name": {
      "title": [{"text": {"content": "Propact Integration Demo"}}]
    },
    "Status": {
      "select": {"name": "In Progress"}
    },
    "Priority": {
      "select": {"name": "High"}
    }
  },
  "children": [
    {
      "object": "block",
      "type": "paragraph",
      "paragraph": {
        "rich_text": [
          {"type": "text", "text": {"content": "Propact enables "}},
          {"type": "text", "text": {"content": "universal markdown transport", "annotations": {"bold": true}}},
          {"type": "text", "text": {"content": " for 100+ APIs without custom code."}}
        ]
      }
    },
    {
      "object": "block",
      "type": "heading_2",
      "heading_2": {
        "rich_text": [{"type": "text", "text": {"content": "Key Features"}}]
      }
    },
    {
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{"type": "text", "text": {"content": "Schema-aware content splitting"}}]
      }
    },
    {
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{"type": "text", "text": {"content": "Automatic file attachment handling"}}]
      }
    },
    {
      "object": "block",
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{"type": "text", "text": {"content": "Response conversion to markdown"}}]
      }
    }
  ]
}
```

## Expected Output

The response will include:
- Page ID and URL
- Created and last edited timestamps
- Properties and block structure

## Run Command

```bash
# Replace DATABASE_ID with your actual database ID
propact README.md \
  --endpoint "https://api.notion.com/v1/pages" \
  --header "Authorization: Bearer $NOTION_TOKEN" \
  --header "Notion-Version: 2022-06-28"
```

## Environment Variables

```bash
NOTION_TOKEN=<YOUR_NOTION_TOKEN>
```

## Requirements

- Notion integration created at https://www.notion.so/my-integrations
- Database ID from Notion page URL
- Integration with page creation permissions

## Getting Database ID

1. Open your Notion database
2. Copy the ID from the URL (after `/` and before `?`)
3. Example: `https://notion.so/DATABASE_ID?v=...`
