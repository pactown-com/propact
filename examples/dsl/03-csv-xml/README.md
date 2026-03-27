# CSV and XML Conversions

This example demonstrates converting between Markdown tables, CSV, and XML formats.

## 📊 CSV ↔ Markdown Table

### CSV to Markdown

**Input CSV (data.csv):**

```csv
id,name,price,category
1,Laptop,999.99,Electronics
2,Book,19.99,Education
3,Coffee,4.99,Food
```

**Conversion Command:**

```bash
propact convert file data.csv --from csv --to markdown
```

**Output Markdown:**

```markdown
| id | name    | price  | category    |
|----|---------|--------|-------------|
| 1  | Laptop  | 999.99 | Electronics |
| 2  | Book    | 19.99  | Education   |
| 3  | Coffee  | 4.99   | Food        |
```

### Markdown to CSV

**Input Markdown:**

```markdown
| product | stock | location |
|---------|-------|----------|
| Widget A | 100 | Warehouse 1 |
| Widget B | 50 | Warehouse 2 |
| Widget C | 200 | Warehouse 1 |
```

**Conversion Command:**

```bash
propact convert file inventory.md --from markdown --to csv --output inventory.csv
```

**Output CSV:**

```csv
product,stock,location
Widget A,100,Warehouse 1
Widget B,50,Warehouse 2
Widget C,200,Warehouse 1
```

## 📄 XML ↔ Markdown

### XML to Markdown

**Input XML (api_response.xml):**

```xml
<users>
  <user>
    <id>1</id>
    <name>John Doe</name>
    <email>john@example.com</email>
  </user>
  <user>
    <id>2</id>
    <name>Jane Smith</name>
    <email>jane@example.com</email>
  </user>
</users>
```

**Conversion Command:**

```bash
propact convert file api_response.xml --from xml --to markdown
```

**Output Markdown:**

```markdown
```xml
<users>
  <user>
    <id>1</id>
    <name>John Doe</name>
    <email>john@example.com</email>
  </user>
  <user>
    <id>2</id>
    <name>Jane Smith</name>
    <email>jane@example.com</email>
  </user>
</users>
```

**Parsed Structure:**
```yaml
users:
  user:
  - id: '1'
    name: John Doe
    email: john@example.com
  - id: '2'
    name: Jane Smith
    email: jane@example.com
```
```

### Markdown to XML

**Input Markdown:**

```markdown
# Configuration

Database host: localhost
Database port: 5432
Database name: myapp
```

**Conversion Command:**

```bash
propact convert file config.md --from markdown --to xml --root-tag config
```

**Output XML:**

```xml
<config>
  <Database host>localhost</Database host>
  <Database port>5432</Database port>
  <Database name>myapp</Database name>
</config>
```

## 🔄 Chain Conversions

### CSV → XML via Markdown

```bash
# Step 1: CSV to Markdown
propact convert file data.csv --from csv --to markdown --output temp.md

# Step 2: Markdown to XML
propact convert file temp.md --from markdown --to xml --root-tag data --output data.xml
```

### XML → CSV via Markdown

```bash
# Step 1: XML to Markdown
propact convert file data.xml --from xml --to markdown --output temp.md

# Step 2: Extract table and convert to CSV
# (Note: You may need to manually extract the table from the output)
```

## 📋 Use Cases

### CSV Use Cases
1. **Spreadsheet Integration**: Import/export data from Excel, Google Sheets
2. **Data Analysis**: Convert CSV data to readable format for documentation
3. **Configuration**: Manage configuration data in MD tables, export as CSV
4. **Testing**: Generate test data in MD, convert to CSV for test tools

### XML Use Cases
1. **API Responses**: Convert XML API responses to readable documentation
2. **Configuration Files**: Manage XML configs in MD format
3. **Data Exchange**: Convert between XML and other formats
4. **Documentation**: Include XML samples in documentation

## 🔧 Advanced Options

### XML Customization
- **Root tag**: `--root-tag custom_name` (default: root)
- **Pretty printing**: Automatic with proper indentation

### CSV Handling
- **Headers**: Automatically detected from first row
- **Encoding**: UTF-8 by default
- **Quotes**: Properly handled for fields with commas

## ✅ Requirements

Install DSL dependencies:

```bash
pip install propact[dsl]
```

This includes:
- pandas - for CSV processing
- xmltodict - for XML conversion
- PyYAML - for structured data representation
