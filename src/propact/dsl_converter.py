"""DSL Converter for bidirectional format conversions."""

import re
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass
from pathlib import Path
import logging

# Try to import optional dependencies
try:
    import sqlglot
    HAS_SQLGLOT = True
except ImportError:
    HAS_SQLGLOT = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    import xmltodict
    HAS_XMLTODICT = True
except ImportError:
    HAS_XMLTODICT = False

try:
    from markdown_table_generator import table_from_dataframe
    HAS_MD_TABLE_GEN = True
except ImportError:
    HAS_MD_TABLE_GEN = False


@dataclass
class ConversionResult:
    """Result of a conversion operation."""
    success: bool
    content: str
    format: str
    errors: List[str] = None
    warnings: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
        if self.metadata is None:
            self.metadata = {}


class BaseConverter(ABC):
    """Base class for format converters."""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def to_markdown(self, content: str, **kwargs) -> ConversionResult:
        """Convert content to Markdown format."""
        pass
    
    @abstractmethod
    def from_markdown(self, markdown: str, **kwargs) -> ConversionResult:
        """Convert Markdown content to target format."""
        pass
    
    def _parse_md_table(self, markdown: str) -> Tuple[List[str], List[List[str]]]:
        """Parse a markdown table into headers and rows."""
        lines = [line.strip() for line in markdown.strip().split('\n') if line.strip()]
        
        # Find table start
        table_start = -1
        for i, line in enumerate(lines):
            if '|' in line and i + 1 < len(lines) and '-' in lines[i + 1]:
                table_start = i
                break
        
        if table_start == -1:
            raise ValueError("No valid markdown table found")
        
        # Parse header
        header_line = lines[table_start]
        headers = [h.strip() for h in header_line.split('|') if h.strip()]
        
        # Parse rows (skip separator line)
        rows = []
        for line in lines[table_start + 2:]:
            if '|' in line:
                row = [cell.strip() for cell in line.split('|') if cell.strip()]
                if row:
                    rows.append(row)
        
        return headers, rows
    
    def _create_md_table(self, headers: List[str], rows: List[List[str]], 
                        align: str = "left") -> str:
        """Create a markdown table from headers and rows."""
        if not headers:
            return ""
        
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(cell))
        
        # Build table
        lines = []
        
        # Header row
        header_cells = [h.ljust(w) for h, w in zip(headers, col_widths)]
        lines.append(f"| {' | '.join(header_cells)} |")
        
        # Separator row
        if align == "center":
            sep_cells = [':' + '-' * (w - 2) + ':' for w in col_widths]
        elif align == "right":
            sep_cells = ['-' * (w - 1) + ':' for w in col_widths]
        else:  # left
            sep_cells = ['-' * w for w in col_widths]
        lines.append(f"| {' | '.join(sep_cells)} |")
        
        # Data rows
        for row in rows:
            row_cells = []
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    row_cells.append(cell.ljust(col_widths[i]))
                else:
                    row_cells.append(cell)
            lines.append(f"| {' | '.join(row_cells)} |")
        
        return '\n'.join(lines)


class SQLConverter(BaseConverter):
    """Converter for SQL ↔ Markdown tables."""
    
    def __init__(self):
        super().__init__()
        self.supported_dialects = ["postgres", "mysql", "sqlite", "snowflake", "bigquery"]
    
    def to_markdown(self, content: str, **kwargs) -> ConversionResult:
        """Convert SQL query/result to Markdown table."""
        try:
            if not HAS_PANDAS:
                return ConversionResult(
                    success=False,
                    content="",
                    format="markdown",
                    errors=["pandas is required for SQL to Markdown conversion"]
                )
            
            # Check if content is a query or result
            db_connection = kwargs.get('db_connection')
            
            if db_connection:
                # Execute query and get results
                try:
                    df = pd.read_sql(content, db_connection)
                except Exception as e:
                    return ConversionResult(
                        success=False,
                        content="",
                        format="markdown",
                        errors=[f"Failed to execute SQL query: {str(e)}"]
                    )
            else:
                # Parse SQL to generate mock data (for demo)
                df = self._mock_sql_result(content)
            
            # Convert DataFrame to markdown
            if HAS_MD_TABLE_GEN:
                table_md = table_from_dataframe(df, align="center")
                content_md = table_md.to_markdown()
            else:
                # Simple markdown table generation
                content_md = self._create_md_table(
                    df.columns.tolist(),
                    df.values.astype(str).tolist()
                )
            
            return ConversionResult(
                success=True,
                content=content_md,
                format="markdown",
                metadata={"rows": len(df), "columns": len(df.columns)}
            )
            
        except Exception as e:
            self.logger.error(f"SQL to Markdown conversion failed: {e}")
            return ConversionResult(
                success=False,
                content="",
                format="markdown",
                errors=[str(e)]
            )
    
    def from_markdown(self, markdown: str, **kwargs) -> ConversionResult:
        """Convert Markdown table to SQL INSERT/UPDATE statements."""
        try:
            dialect = kwargs.get('dialect', 'postgres')
            table_name = kwargs.get('table_name', 'generated_table')
            operation = kwargs.get('operation', 'INSERT')  # INSERT or UPDATE
            
            if dialect not in self.supported_dialects:
                return ConversionResult(
                    success=False,
                    content="",
                    format="sql",
                    errors=[f"Unsupported SQL dialect: {dialect}"]
                )
            
            # Parse markdown table
            headers, rows = self._parse_md_table(markdown)
            
            if not headers or not rows:
                return ConversionResult(
                    success=False,
                    content="",
                    format="sql",
                    errors=["No data found in markdown table"]
                )
            
            # Generate SQL
            sql_statements = []
            
            # CREATE TABLE statement
            columns_def = ', '.join([f'"{col}" TEXT' for col in headers])
            sql_statements.append(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_def});')
            
            if operation == 'INSERT':
                # INSERT statements
                for row in rows:
                    values = ', '.join(['\'' + val.replace("'", "''") + '\'' for val in row])
                    cols = ', '.join([f'"{col}"' for col in headers])
                    sql_statements.append(f'INSERT INTO "{table_name}" ({cols}) VALUES ({values});')
            
            elif operation == 'UPDATE':
                # UPDATE statements (need a key column)
                key_column = kwargs.get('key_column', headers[0])
                if key_column not in headers:
                    return ConversionResult(
                        success=False,
                        content="",
                        format="sql",
                        errors=[f"Key column '{key_column}' not found in table"]
                    )
                
                key_idx = headers.index(key_column)
                for row in rows:
                    set_clauses = []
                    for i, (col, val) in enumerate(zip(headers, row)):
                        if i != key_idx:
                            set_clauses.append(f'"{col}" = \'{val.replace("\"", "\"\"")}\'')
                    
                    where_val = row[key_idx].replace("'", "''")
                    sql_statements.append(
                        f'UPDATE "{table_name}" SET {", ".join(set_clauses)} WHERE "{key_column}" = \'{where_val}\';'
                    )
            
            # Transpile to target dialect if sqlglot is available
            final_sql = '\n'.join(sql_statements)
            if HAS_SQLGLOT and dialect != 'postgres':
                try:
                    final_sql = sqlglot.transpile(final_sql, read='postgres', write=dialect)[0]
                except Exception as e:
                    self.logger.warning(f"SQL transpilation failed: {e}")
            
            return ConversionResult(
                success=True,
                content=final_sql,
                format="sql",
                metadata={"table": table_name, "rows": len(rows), "columns": len(headers)}
            )
            
        except Exception as e:
            self.logger.error(f"Markdown to SQL conversion failed: {e}")
            return ConversionResult(
                success=False,
                content="",
                format="sql",
                errors=[str(e)]
            )
    
    def _mock_sql_result(self, query: str) -> 'pd.DataFrame':
        """Generate mock data for SQL queries (for demo purposes)."""
        # Simple mock data based on query patterns
        if 'users' in query.lower():
            return pd.DataFrame({
                'id': [1, 2, 3],
                'name': ['Alice', 'Bob', 'Charlie'],
                'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com']
            })
        elif 'products' in query.lower():
            return pd.DataFrame({
                'id': [101, 102],
                'name': ['Product A', 'Product B'],
                'price': [29.99, 49.99]
            })
        else:
            return pd.DataFrame({'result': ['mock_data']})


class GraphQLConverter(BaseConverter):
    """Converter for GraphQL ↔ Markdown."""
    
    def to_markdown(self, content: str, **kwargs) -> ConversionResult:
        """Convert GraphQL query/schema to Markdown."""
        try:
            # Format GraphQL as code block
            formatted = f"```graphql\n{content}\n```"
            
            return ConversionResult(
                success=True,
                content=formatted,
                format="markdown"
            )
        except Exception as e:
            return ConversionResult(
                success=False,
                content="",
                format="markdown",
                errors=[str(e)]
            )
    
    def from_markdown(self, markdown: str, **kwargs) -> ConversionResult:
        """Convert Markdown to GraphQL query."""
        try:
            api_type = kwargs.get('api_type', 'generic')
            
            # Extract structured data from markdown
            structured_data = self._extract_structured_data(markdown)
            
            # Generate GraphQL query based on API type
            if api_type == 'github':
                query = self._generate_github_query(structured_data)
            elif api_type == 'stripe':
                query = self._generate_stripe_query(structured_data)
            else:
                query = self._generate_generic_query(structured_data)
            
            return ConversionResult(
                success=True,
                content=query,
                format="graphql",
                metadata={"api_type": api_type}
            )
        except Exception as e:
            return ConversionResult(
                success=False,
                content="",
                format="graphql",
                errors=[str(e)]
            )
    
    def _extract_structured_data(self, markdown: str) -> Dict[str, Any]:
        """Extract structured key-value data from markdown."""
        data = {}
        
        # Look for key: value patterns
        for line in markdown.split('\n'):
            if ':' in line and not line.strip().startswith('#') and not line.strip().startswith('```'):
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
        
        return data
    
    def _generate_github_query(self, data: Dict[str, Any]) -> str:
        """Generate GitHub GraphQL query."""
        user = data.get('User', data.get('user', 'viewer'))
        status = data.get('Status', 'OPEN')
        limit = data.get('Limit', data.get('limit', '10'))
        
        query = f"""query {{
  user(login: "{user}") {{
    issues(states: [{status}], first: {limit}) {{
      nodes {{
        title
        body
        state
        createdAt
      }}
    }}
  }}
}}"""
        return query
    
    def _generate_stripe_query(self, data: Dict[str, Any]) -> str:
        """Generate Stripe GraphQL query."""
        query = """query {
  charges(first: 10) {
    edges {
      node {
        id
        amount
        currency
        status
        created
      }
    }
  }
}"""
        return query
    
    def _generate_generic_query(self, data: Dict[str, Any]) -> str:
        """Generate generic GraphQL query."""
        return """query {
  viewer {
    id
    name
  }
}"""


class YAMLConverter(BaseConverter):
    """Converter for YAML ↔ Markdown."""
    
    def to_markdown(self, content: str, **kwargs) -> ConversionResult:
        """Convert YAML to Markdown."""
        try:
            if not HAS_YAML:
                return ConversionResult(
                    success=False,
                    content="",
                    format="markdown",
                    errors=["PyYAML is required for YAML conversion"]
                )
            
            # Parse YAML
            data = yaml.safe_load(content)
            
            # Convert to markdown
            if isinstance(data, dict):
                md_content = self._dict_to_markdown(data)
            elif isinstance(data, list):
                md_content = self._list_to_markdown(data)
            else:
                md_content = f"```\n{content}\n```"
            
            return ConversionResult(
                success=True,
                content=md_content,
                format="markdown"
            )
        except Exception as e:
            return ConversionResult(
                success=False,
                content="",
                format="markdown",
                errors=[str(e)]
            )
    
    def from_markdown(self, markdown: str, **kwargs) -> ConversionResult:
        """Convert Markdown to YAML."""
        try:
            if not HAS_YAML:
                return ConversionResult(
                    success=False,
                    content="",
                    format="yaml",
                    errors=["PyYAML is required for YAML conversion"]
                )
            
            # Extract code blocks or convert structured content
            yaml_blocks = re.findall(r'```yaml\n(.*?)\n```', markdown, re.DOTALL)
            
            if yaml_blocks:
                # Return first YAML block
                yaml_content = yaml_blocks[0]
            else:
                # Convert structured markdown to YAML
                data = self._markdown_to_dict(markdown)
                yaml_content = yaml.dump(data, indent=2)
            
            return ConversionResult(
                success=True,
                content=yaml_content,
                format="yaml"
            )
        except Exception as e:
            return ConversionResult(
                success=False,
                content="",
                format="yaml",
                errors=[str(e)]
            )
    
    def _dict_to_markdown(self, data: Dict[str, Any], level: int = 0) -> str:
        """Convert dictionary to markdown."""
        lines = []
        indent = "  " * level
        
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{indent}- **{key}:**")
                lines.append(self._dict_to_markdown(value, level + 1))
            elif isinstance(value, list):
                lines.append(f"{indent}- **{key}:**")
                for item in value:
                    lines.append(f"{indent}  - {item}")
            else:
                lines.append(f"{indent}- **{key}:** {value}")
        
        return '\n'.join(lines)
    
    def _list_to_markdown(self, data: List[Any]) -> str:
        """Convert list to markdown."""
        lines = []
        for item in data:
            if isinstance(item, dict):
                lines.append("- " + self._dict_to_markdown(item, 1))
            else:
                lines.append(f"- {item}")
        return '\n'.join(lines)
    
    def _markdown_to_dict(self, markdown: str) -> Dict[str, Any]:
        """Convert structured markdown to dictionary."""
        data = {}
        
        for line in markdown.split('\n'):
            if ':' in line and not line.strip().startswith('#') and not line.strip().startswith('```'):
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
        
        return data


class CSVConverter(BaseConverter):
    """Converter for CSV ↔ Markdown tables."""
    
    def to_markdown(self, content: str, **kwargs) -> ConversionResult:
        """Convert CSV to Markdown table."""
        try:
            if not HAS_PANDAS:
                return ConversionResult(
                    success=False,
                    content="",
                    format="markdown",
                    errors=["pandas is required for CSV conversion"]
                )
            
            # Parse CSV
            from io import StringIO
            df = pd.read_csv(StringIO(content))
            
            # Convert to markdown table
            if HAS_MD_TABLE_GEN:
                table_md = table_from_dataframe(df, align="center")
                content_md = table_md.to_markdown()
            else:
                content_md = self._create_md_table(
                    df.columns.tolist(),
                    df.values.astype(str).tolist()
                )
            
            return ConversionResult(
                success=True,
                content=content_md,
                format="markdown",
                metadata={"rows": len(df), "columns": len(df.columns)}
            )
        except Exception as e:
            return ConversionResult(
                success=False,
                content="",
                format="markdown",
                errors=[str(e)]
            )
    
    def from_markdown(self, markdown: str, **kwargs) -> ConversionResult:
        """Convert Markdown table to CSV."""
        try:
            # Parse markdown table
            headers, rows = self._parse_md_table(markdown)
            
            # Generate CSV
            import csv
            from io import StringIO
            
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(headers)
            writer.writerows(rows)
            
            csv_content = output.getvalue()
            
            return ConversionResult(
                success=True,
                content=csv_content,
                format="csv",
                metadata={"rows": len(rows), "columns": len(headers)}
            )
        except Exception as e:
            return ConversionResult(
                success=False,
                content="",
                format="csv",
                errors=[str(e)]
            )


class XMLConverter(BaseConverter):
    """Converter for XML ↔ Markdown."""
    
    def to_markdown(self, content: str, **kwargs) -> ConversionResult:
        """Convert XML to Markdown."""
        try:
            if not HAS_XMLTODICT:
                return ConversionResult(
                    success=False,
                    content="",
                    format="markdown",
                    errors=["xmltodict is required for XML conversion"]
                )
            
            # Parse XML
            data = xmltodict.parse(content)
            
            # Convert to YAML for readability, then wrap in code block
            if HAS_YAML:
                yaml_content = yaml.dump(data, indent=2)
                md_content = f"```xml\n{content}\n```\n\n**Parsed Structure:**\n```yaml\n{yaml_content}\n```"
            else:
                md_content = f"```xml\n{content}\n```"
            
            return ConversionResult(
                success=True,
                content=md_content,
                format="markdown"
            )
        except Exception as e:
            return ConversionResult(
                success=False,
                content="",
                format="markdown",
                errors=[str(e)]
            )
    
    def from_markdown(self, markdown: str, **kwargs) -> ConversionResult:
        """Convert Markdown to XML."""
        try:
            if not HAS_XMLTODICT:
                return ConversionResult(
                    success=False,
                    content="",
                    format="xml",
                    errors=["xmltodict is required for XML conversion"]
                )
            
            # Extract XML from code blocks
            xml_blocks = re.findall(r'```xml\n(.*?)\n```', markdown, re.DOTALL)
            
            if xml_blocks:
                return ConversionResult(
                    success=True,
                    content=xml_blocks[0],
                    format="xml"
                )
            
            # Convert structured data to XML
            root_tag = kwargs.get('root_tag', 'root')
            data = self._markdown_to_dict(markdown)
            
            xml_content = xmltodict.unparse({root_tag: data}, pretty=True)
            
            return ConversionResult(
                success=True,
                content=xml_content,
                format="xml"
            )
        except Exception as e:
            return ConversionResult(
                success=False,
                content="",
                format="xml",
                errors=[str(e)]
            )
    
    def _markdown_to_dict(self, markdown: str) -> Dict[str, Any]:
        """Convert structured markdown to dictionary."""
        data = {}
        
        for line in markdown.split('\n'):
            if ':' in line and not line.strip().startswith('#') and not line.strip().startswith('```'):
                key, value = line.split(':', 1)
                data[key.strip()] = value.strip()
        
        return data


class DSLConverter:
    """Main DSL converter using strategy pattern."""
    
    def __init__(self):
        """Initialize DSL converter with all format converters."""
        self.converters: Dict[str, BaseConverter] = {
            'sql': SQLConverter(),
            'graphql': GraphQLConverter(),
            'yaml': YAMLConverter(),
            'yml': YAMLConverter(),
            'csv': CSVConverter(),
            'xml': XMLConverter(),
        }
        self.logger = logging.getLogger(__name__)
    
    def convert(self, content: str, from_format: str, to_format: str, **kwargs) -> ConversionResult:
        """Convert content from one format to another.
        
        Args:
            content: Input content
            from_format: Source format (sql, graphql, yaml, csv, xml, markdown)
            to_format: Target format
            **kwargs: Additional options for conversion
            
        Returns:
            ConversionResult with converted content or errors
        """
        try:
            # Normalize formats
            from_format = from_format.lower()
            to_format = to_format.lower()
            
            # Direct conversion
            if from_format == 'markdown':
                # Markdown to target format
                if to_format not in self.converters:
                    return ConversionResult(
                        success=False,
                        content="",
                        format=to_format,
                        errors=[f"Unsupported target format: {to_format}"]
                    )
                
                converter = self.converters[to_format]
                return converter.from_markdown(content, **kwargs)
            
            elif to_format == 'markdown':
                # Source format to Markdown
                if from_format not in self.converters:
                    return ConversionResult(
                        success=False,
                        content="",
                        format="markdown",
                        errors=[f"Unsupported source format: {from_format}"]
                    )
                
                converter = self.converters[from_format]
                return converter.to_markdown(content, **kwargs)
            
            else:
                # Convert via Markdown as intermediate format
                # First convert to Markdown
                if from_format not in self.converters:
                    return ConversionResult(
                        success=False,
                        content="",
                        format=to_format,
                        errors=[f"Unsupported source format: {from_format}"]
                    )
                
                converter = self.converters[from_format]
                md_result = converter.to_markdown(content, **kwargs)
                
                if not md_result.success:
                    return md_result
                
                # Then convert Markdown to target
                if to_format not in self.converters:
                    return ConversionResult(
                        success=False,
                        content="",
                        format=to_format,
                        errors=[f"Unsupported target format: {to_format}"]
                    )
                
                target_converter = self.converters[to_format]
                return target_converter.from_markdown(md_result.content, **kwargs)
        
        except Exception as e:
            self.logger.error(f"Conversion failed: {e}")
            return ConversionResult(
                success=False,
                content="",
                format=to_format,
                errors=[str(e)]
            )
    
    def list_formats(self) -> List[str]:
        """List all supported formats."""
        return list(self.converters.keys()) + ['markdown']
    
    def register_converter(self, format_name: str, converter: BaseConverter):
        """Register a custom converter."""
        self.converters[format_name.lower()] = converter


# Default converter instance
default_converter = DSLConverter()
