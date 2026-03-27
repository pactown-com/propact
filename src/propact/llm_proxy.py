"""LiteLLM Proxy for multi-provider LLM support."""

import os
from typing import Optional, Dict, Any, AsyncGenerator
from dataclasses import dataclass

try:
    from litellm import completion, acompletion
except ImportError:
    completion = None
    acompletion = None


@dataclass
class LLMConfig:
    """Configuration for an LLM provider."""
    model: str
    api_base: Optional[str] = None
    api_key: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None


class LiteLLMProxy:
    """Unified interface for 100+ LLM providers via LiteLLM."""
    
    # Predefined provider configurations
    DEFAULT_CONFIGS = {
        "local": LLMConfig(
            model="ollama/llama3.2",
            api_base="http://localhost:11434",
            api_key="no-key-needed"
        ),
        "cloud": LLMConfig(
            model="openai/gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY")
        ),
        "groq": LLMConfig(
            model="groq/llama3-70b-8192",
            api_key=os.getenv("GROQ_API_KEY")
        ),
        "anthropic": LLMConfig(
            model="anthropic/claude-3.5-sonnet",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        ),
        "openrouter": LLMConfig(
            model="openrouter/openai/gpt-4o-mini",
            api_key=os.getenv("OPENROUTER_API_KEY")
        ),
        "bedrock": LLMConfig(
            model="bedrock/claude-3-haiku",
            api_key=os.getenv("AWS_ACCESS_KEY_ID")
        )
    }
    
    def __init__(self, provider: str = "local", custom_config: Optional[Dict] = None):
        """Initialize LiteLLM proxy.
        
        Args:
            provider: Predefined provider name or "custom"
            custom_config: Custom configuration dict for non-standard providers
        """
        if completion is None:
            raise ImportError(
                "litellm is required. Install with: pip install litellm"
            )
        
        self.provider = provider
        self.config = self._load_config(provider, custom_config)
    
    def _load_config(self, provider: str, custom_config: Optional[Dict]) -> LLMConfig:
        """Load configuration for provider."""
        if custom_config:
            return LLMConfig(**custom_config)
        
        if provider in self.DEFAULT_CONFIGS:
            return self.DEFAULT_CONFIGS[provider]
        
        # Try to parse as direct model string (e.g., "ollama/llama3.2")
        if "/" in provider:
            return LLMConfig(model=provider, api_key=os.getenv("LITELLM_MASTER_KEY", "sk-no-key"))
        
        # Default fallback
        return self.DEFAULT_CONFIGS["local"]
    
    async def generate(
        self, 
        prompt: str, 
        system: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Generate text using unified LLM call.
        
        Args:
            prompt: User prompt
            system: Optional system message
            temperature: Override temperature
            max_tokens: Override max tokens
            **kwargs: Additional parameters for litellm
            
        Returns:
            Generated text response
        """
        messages = [{"role": "user", "content": prompt}]
        if system:
            messages.insert(0, {"role": "system", "content": system})
        
        params = {
            "model": self.config.model,
            "messages": messages,
            "temperature": temperature or self.config.temperature,
        }
        
        if self.config.api_key:
            params["api_key"] = self.config.api_key
        if self.config.api_base:
            params["api_base"] = self.config.api_base
        if max_tokens or self.config.max_tokens:
            params["max_tokens"] = max_tokens or self.config.max_tokens
        
        params.update(kwargs)
        
        response = await acompletion(**params)
        return response.choices[0].message.content
    
    async def astream(
        self, 
        prompt: str, 
        system: Optional[str] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Stream text generation.
        
        Args:
            prompt: User prompt
            system: Optional system message
            **kwargs: Additional parameters
            
        Yields:
            Text chunks as they arrive
        """
        messages = [{"role": "user", "content": prompt}]
        if system:
            messages.insert(0, {"role": "system", "content": system})
        
        params = {
            "model": self.config.model,
            "messages": messages,
            "stream": True,
        }
        
        if self.config.api_key:
            params["api_key"] = self.config.api_key
        if self.config.api_base:
            params["api_base"] = self.config.api_base
        
        params.update(kwargs)
        
        stream = await acompletion(**params)
        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    
    def generate_sync(
        self, 
        prompt: str, 
        system: Optional[str] = None,
        **kwargs
    ) -> str:
        """Synchronous text generation.
        
        Args:
            prompt: User prompt
            system: Optional system message
            **kwargs: Additional parameters
            
        Returns:
            Generated text response
        """
        import asyncio
        return asyncio.run(self.generate(prompt, system, **kwargs))
    
    @classmethod
    def list_providers(cls) -> list:
        """List available predefined providers."""
        return list(cls.DEFAULT_CONFIGS.keys())
    
    @classmethod
    def from_env(cls, prefix: str = "PROPELLM_") -> "LiteLLMProxy":
        """Create proxy from environment variables.
        
        Args:
            prefix: Environment variable prefix
            
        Returns:
            Configured LiteLLMProxy instance
        """
        model = os.getenv(f"{prefix}MODEL", "ollama/llama3.2")
        api_base = os.getenv(f"{prefix}API_BASE")
        api_key = os.getenv(f"{prefix}API_KEY")
        
        config = LLMConfig(model=model, api_base=api_base, api_key=api_key)
        return cls("custom", custom_config=config.__dict__)


# Convenience functions for common use cases
async def quick_generate(prompt: str, provider: str = "local", **kwargs) -> str:
    """Quick one-off generation without instantiating class.
    
    Args:
        prompt: User prompt
        provider: Provider name
        **kwargs: Additional parameters
        
    Returns:
        Generated text
    """
    proxy = LiteLLMProxy(provider)
    return await proxy.generate(prompt, **kwargs)


async def match_intent(query: str, candidates: list, provider: str = "groq") -> str:
    """Use LLM to select best match from candidates.
    
    Args:
        query: User query/intent
        candidates: List of candidate options
        provider: Fast provider for matching (default: groq)
        
    Returns:
        Selected candidate
    """
    prompt = f"""Select the best match for the following query.

Query: "{query}"

Candidates:
{chr(10).join(f"- {c}" for c in candidates)}

Respond with only the selected candidate name, nothing else."""
    
    proxy = LiteLLMProxy(provider)
    response = await proxy.generate(prompt, temperature=0.1)
    return response.strip()


async def self_correct(error: Exception, context: dict, provider: str = "anthropic") -> dict:
    """Use LLM to self-correct from error.
    
    Args:
        error: The error that occurred
        context: Context information (endpoint, parameters, etc.)
        provider: Accurate provider for reasoning (default: anthropic)
        
    Returns:
        Corrected parameters as dict
    """
    prompt = f"""The following error occurred in an API call:

Error: {type(error).__name__}: {str(error)}

Context:
{chr(10).join(f"{k}: {v}" for k, v in context.items())}

Suggest corrected parameters to fix this error.
Respond in JSON format with the corrected values."""
    
    proxy = LiteLLMProxy(provider)
    response = await proxy.generate(prompt, temperature=0.0)
    
    import json
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"suggestion": response.strip()}
