"""Query Generator with LiteLLM integration for intent-to-MD conversion."""

from typing import Optional, Dict, Any
from propact.llm_proxy import LiteLLMProxy


class QueryGenerator:
    """Generate Propact MD templates from natural language queries using LLM."""
    
    def __init__(self, provider: str = "cloud"):
        """Initialize query generator.
        
        Args:
            provider: LLM provider for generation (cloud, groq, local, etc.)
        """
        self.llm = LiteLLMProxy(provider)
    
    async def generate_md(self, query: str, **kwargs) -> str:
        """Generate Propact MD template from natural language query.
        
        Args:
            query: Natural language query (e.g., "pogoda w Gdańsku")
            **kwargs: Additional context (endpoint hints, schema, etc.)
            
        Returns:
            Generated Markdown template
        """
        system_prompt = """You are a Propact MD template generator. 
Convert natural language queries into structured Markdown templates with embedded JSON queries.

Rules:
1. Create a clear title in the target language
2. Include a JSON block describing the intent
3. Keep it simple and copy-paste ready
4. Use the format shown in examples"""

        intent_prompt = f"""Query: "{query}"

Generate a Propact Markdown template for this query.

The template should include:
- A descriptive title
- A brief description  
- A JSON code block with the query parameters
- Optional usage hints

Respond with only the Markdown content, no explanations."""

        return await self.llm.generate(intent_prompt, system=system_prompt)
    
    async def generate_from_spec(
        self, 
        query: str, 
        openapi_spec: dict,
        provider: str = "groq"
    ) -> str:
        """Generate MD template matching OpenAPI spec.
        
        Args:
            query: User query
            openapi_spec: OpenAPI specification dict
            provider: Fast provider for quick matching
            
        Returns:
            Generated MD template
        """
        llm = LiteLLMProxy(provider)
        
        prompt = f"""Given this OpenAPI spec and user query, generate a Propact MD template.

User Query: "{query}"

Available Endpoints:
{list(openapi_spec.get('paths', {}).keys())[:10]}

Generate a markdown file that:
1. Has a clear title matching the intent
2. Includes relevant JSON query structure
3. References the appropriate endpoint

Respond with only the Markdown content."""

        return await llm.generate(prompt)
    
    async def suggest_endpoint(
        self, 
        query: str, 
        available_endpoints: list,
        provider: str = "groq"
    ) -> str:
        """Suggest best endpoint for query.
        
        Args:
            query: User query
            available_endpoints: List of available endpoint paths
            provider: Fast provider for matching
            
        Returns:
            Suggested endpoint path
        """
        llm = LiteLLMProxy(provider)
        
        prompt = f"""Select the best API endpoint for this query.

Query: "{query}"

Available Endpoints:
{chr(10).join(f"- {ep}" for ep in available_endpoints)}

Respond with only the endpoint path, nothing else."""

        response = await llm.generate(prompt, temperature=0.1)
        return response.strip()
    
    async def enhance_template(
        self, 
        template: str, 
        context: Optional[Dict] = None,
        provider: str = "anthropic"
    ) -> str:
        """Enhance existing template with better formatting/examples.
        
        Args:
            template: Existing MD template
            context: Additional context for enhancement
            provider: Accurate provider for quality improvements
            
        Returns:
            Enhanced template
        """
        llm = LiteLLMProxy(provider)
        
        system_prompt = """Enhance this Propact template by:
1. Adding clear examples
2. Improving formatting
3. Adding response format documentation
4. Making it more user-friendly"""

        prompt = f"""Enhance this template:

{template}

Context: {context or 'None'}

Respond with the enhanced Markdown template only."""

        return await llm.generate(prompt, system=system_prompt)
    
    def _render_template(self, intent: str, **params) -> str:
        """Render final MD template from intent.
        
        Args:
            intent: Parsed intent string
            **params: Template parameters
            
        Returns:
            Rendered template
        """
        # Basic template rendering - can be extended
        return f"""# {intent.title()}

Generated from query: {params.get('query', 'N/A')}

```json
{params.get('json_block', '{}')}
```

**Endpoint**: {params.get('endpoint', 'TBD')}
"""


# Convenience async functions
async def query_to_md(query: str, provider: str = "groq") -> str:
    """Quick conversion from query to MD template.
    
    Args:
        query: Natural language query
        provider: LLM provider to use
        
    Returns:
        Generated Markdown template
    """
    generator = QueryGenerator(provider)
    return await generator.generate_md(query)


async def batch_generate(queries: list, provider: str = "cloud") -> list:
    """Generate multiple templates in parallel.
    
    Args:
        queries: List of queries
        provider: LLM provider
        
    Returns:
        List of generated templates
    """
    import asyncio
    generator = QueryGenerator(provider)
    
    tasks = [generator.generate_md(q) for q in queries]
    return await asyncio.gather(*tasks)
