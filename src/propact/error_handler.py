"""Error handling and recovery system for Propact."""

import time
import random
import json
import re
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass
from enum import Enum

# Optional LLM integration
try:
    import ollama
    HAS_OLLAMA = True
except ImportError:
    HAS_OLLAMA = False
    ollama = None

# LiteLLM integration for multi-provider support
try:
    from .llm_proxy import LiteLLMProxy, self_correct
    HAS_LITELLM = True
except ImportError:
    HAS_LITELLM = False
    LiteLLMProxy = None
    self_correct = None

from rich.console import Console

console = Console()


class ErrorMode(Enum):
    """Error handling modes."""
    STRICT = "strict"      # Fail fast, no recovery
    RECOVER = "recover"    # Auto-recover with LLM and fallbacks
    DEBUG = "debug"        # Verbose error debugging
    INTERACTIVE = "interactive"  # Human-in-loop for fixes


@dataclass
class MatchError:
    """Error information for recovery strategies."""
    type: str  # "no_match", "validation", "http_400", "http_5xx", "timeout"
    confidence: float
    error_msg: str
    candidates: List[Dict[str, Any]]
    endpoint: Optional[str] = None
    retry_count: int = 0


class PropactErrorHandler:
    """Multi-layer error recovery system for Propact."""
    
    def __init__(self, mode: ErrorMode = ErrorMode.RECOVER, max_retries: int = 3, 
                 llm_model: str = "llama3.2", llm_provider: str = "anthropic"):
        self.mode = mode
        self.max_retries = max_retries
        self.llm_model = llm_model
        self.llm_provider = llm_provider
        self.retry_counts = {}
        self.fallback_keywords = ["upload", "create", "post", "send", "add", "new"]
        
        # Initialize LiteLLM proxy if available
        self.llm_proxy = None
        if HAS_LITELLM:
            try:
                self.llm_proxy = LiteLLMProxy(llm_provider)
            except Exception as e:
                console.print(f"[yellow]Warning: Could not initialize LLM provider {llm_provider}: {e}[/yellow]")
    
    async def handle_match_failure(self, error: MatchError, md_content: str, 
                                   spec: dict) -> Optional[str]:
        """Multi-strategy error recovery."""
        
        if self.mode == ErrorMode.STRICT:
            console.print(f"[red]Error in strict mode: {error.error_msg}[/red]")
            return None
        
        if self.mode == ErrorMode.DEBUG:
            console.print(f"[yellow]Debug: Error type={error.type}, confidence={error.confidence}[/yellow]")
            console.print(f"[yellow]Debug: Error message: {error.error_msg}[/yellow]")
        
        # Route to appropriate recovery strategy
        if error.type == "no_match":
            return await self._fallback_search(error, spec)
        elif error.type == "validation":
            return await self._llm_self_correct(error, md_content)
        elif error.type.startswith("http_4"):
            return await self._fix_client_error(error, md_content)
        elif error.type.startswith("http_5") or error.type == "http_429":
            return await self._retry_with_backoff(error)
        elif error.type == "timeout":
            return await self._simplify_and_retry(error, md_content)
        else:
            return await self._generic_fallback(error, spec)
    
    async def _llm_self_correct(self, error: MatchError, md_content: str) -> Optional[str]:
        """LLM analyzes error and proposes fix using LiteLLM (Claude) for best reasoning."""
        # Prefer LiteLLM for multi-provider support
        if HAS_LITELLM and self.llm_proxy:
            return await self._llm_self_correct_litellm(error, md_content)
        
        # Fallback to Ollama if available
        if HAS_OLLAMA:
            return await self._llm_self_correct_ollama(error, md_content)
        
        console.print("[yellow]LLM self-correction not available (no LLM providers configured)[/yellow]")
        return await self._fallback_search(error, {})
    
    async def _llm_self_correct_litellm(self, error: MatchError, md_content: str) -> Optional[str]:
        """Use LiteLLM for self-correction (default: anthropic for reasoning)."""
        try:
            context = {
                "intent": self._extract_intent(md_content),
                "error_msg": error.error_msg,
                "candidates": error.candidates[:3],
                "error_type": error.type
            }
            
            result = await self_correct(error, context, provider=self.llm_provider)
            
            if isinstance(result, dict) and "endpoint" in result:
                if self.mode == ErrorMode.DEBUG:
                    console.print(f"[blue]🤖 LLM ({self.llm_provider}) fix: {result.get('reason', 'No reason')}[/blue]")
                
                if self.mode == ErrorMode.INTERACTIVE:
                    console.print(f"[cyan]LLM suggests: {result['endpoint']}[/cyan]")
                    if not self._confirm_fix():
                        return None
                
                return result.get("endpoint")
            
            return None
        except Exception as e:
            console.print(f"[red]LLM self-correction failed: {e}[/red]")
            return await self._fallback_search(error, {})
    
    async def _llm_self_correct_ollama(self, error: MatchError, md_content: str) -> Optional[str]:
        """Legacy Ollama self-correction."""
        intent = self._extract_intent(md_content)
        
        prompt = f"""
MD Intent: {intent}

Schema error: {error.error_msg}

Candidates (low confidence):
{json.dumps(error.candidates[:3], indent=2)}

You are Propact's error recovery AI. Propose a fix.
Response format JSON:
{{"endpoint": "POST /path", "reason": "explanation", "confidence": 0.8}}
"""
        try:
            response = ollama.generate(model=self.llm_model, prompt=prompt)
            fix = json.loads(response['response'])
            
            if self.mode == ErrorMode.DEBUG:
                console.print(f"[blue]🤖 LLM fix: {fix['reason']}[/blue]")
            
            if self.mode == ErrorMode.INTERACTIVE:
                console.print(f"[cyan]LLM suggests: {fix['endpoint']} (confidence: {fix.get('confidence', 0.5)})[/cyan]")
                console.print(f"[cyan]Reason: {fix['reason']}[/cyan]")
                if not self._confirm_fix():
                    return None
            
            return fix.get('endpoint')
        except Exception as e:
            console.print(f"[red]LLM self-correction failed: {e}[/red]")
            return await self._fallback_search(error, {})
    
    async def _fallback_search(self, error: MatchError, spec: dict) -> Optional[str]:
        """Search for similar endpoints using keywords and Levenshtein."""
        if not spec or "paths" not in spec:
            return None
        
        # Extract keywords from error message
        keywords = self._extract_keywords(error.error_msg.lower())
        
        # Search by keywords
        for path, methods in spec["paths"].items():
            for method, operation in methods.items():
                if method.upper() in ["POST", "PUT", "PATCH"]:
                    # Check if keywords match path or operation
                    path_lower = path.lower()
                    op_summary = operation.get("summary", "").lower()
                    op_desc = operation.get("description", "").lower()
                    
                    for keyword in keywords:
                        if (keyword in path_lower or 
                            keyword in op_summary or 
                            keyword in op_desc):
                            endpoint = f"{method.upper()} {path}"
                            if self.mode == ErrorMode.DEBUG:
                                console.print(f"[blue]🔍 Keyword fallback: {endpoint}[/blue]")
                            return endpoint
        
        # Fallback to first POST endpoint
        for path, methods in spec["paths"].items():
            if "post" in methods:
                endpoint = f"POST {path}"
                if self.mode == ErrorMode.DEBUG:
                    console.print(f"[yellow]⚠️ Default fallback: {endpoint}[/yellow]")
                return endpoint
        
        return None
    
    async def _fix_client_error(self, error: MatchError, md_content: str) -> Optional[str]:
        """Fix 4xx errors via LLM parameter correction."""
        # Prefer LiteLLM for multi-provider support
        if HAS_LITELLM and self.llm_proxy:
            return await self._fix_client_error_litellm(error, md_content)
        
        # Fallback to Ollama
        if HAS_OLLAMA:
            return await self._fix_client_error_ollama(error, md_content)
        
        console.print("[yellow]Cannot fix 4xx error without LLM[/yellow]")
        return error.endpoint
    
    async def _fix_client_error_litellm(self, error: MatchError, md_content: str) -> Optional[str]:
        """Fix 4xx errors using LiteLLM (anthropic for reasoning)."""
        try:
            prompt = f"""API Error 4xx: {error.error_msg}
Endpoint: {error.endpoint}
MD content: {md_content[:1000]}

Analyze the error and suggest parameter fixes.
Response format JSON:
{{"fixed_params": {{"param": "value"}}, "reason": "why this fixes the error"}}"""
            
            response = await self.llm_proxy.generate(prompt, temperature=0.0)
            fix = json.loads(response)
            
            if self.mode == ErrorMode.DEBUG:
                console.print(f"[blue]🔧 Parameter fix ({self.llm_provider}): {fix.get('reason', 'No reason')}[/blue]")
            
            # In a real implementation, we would apply the parameter fixes
            # For now, we'll retry the same endpoint
            return error.endpoint
        except Exception as e:
            console.print(f"[red]Parameter fix failed: {e}[/red]")
            return None
    
    async def _fix_client_error_ollama(self, error: MatchError, md_content: str) -> Optional[str]:
        """Legacy Ollama 4xx error fixing."""
        prompt = f"""
API Error 4xx: {error.error_msg}
Endpoint: {error.endpoint}
MD content: {md_content[:1000]}

Analyze the error and suggest parameter fixes.
Response format JSON:
{{"fixed_params": {{"param": "value"}}, "reason": "why this fixes the error"}}
"""
        try:
            response = ollama.generate(model=self.llm_model, prompt=prompt)
            fix = json.loads(response['response'])
            
            if self.mode == ErrorMode.DEBUG:
                console.print(f"[blue]🔧 Parameter fix: {fix['reason']}[/blue]")
            
            # In a real implementation, we would apply the parameter fixes
            # For now, we'll retry the same endpoint
            return error.endpoint
        except Exception as e:
            console.print(f"[red]Parameter fix failed: {e}[/red]")
            return None
    
    async def _retry_with_backoff(self, error: MatchError) -> Optional[str]:
        """Exponential backoff for 5xx and rate limit errors."""
        if not error.endpoint:
            return None
        
        retry_count = self.retry_counts.get(error.endpoint, 0)
        
        if retry_count >= self.max_retries:
            console.print("[red]❌ Max retries reached. Human review needed.[/red]")
            return None
        
        # Calculate delay with exponential backoff and jitter
        delay = min(2 ** retry_count, 60)
        jitter = random.uniform(0, 1)
        time.sleep(delay + jitter)
        
        self.retry_counts[error.endpoint] = retry_count + 1
        
        if self.mode == ErrorMode.DEBUG:
            console.print(f"[blue]🔄 Retry {retry_count + 1}/{self.max_retries} after {delay:.1f}s[/blue]")
        
        return error.endpoint
    
    async def _simplify_and_retry(self, error: MatchError, md_content: str) -> Optional[str]:
        """Simplify payload for timeout errors."""
        if self.mode == ErrorMode.DEBUG:
            console.print("[blue]📦 Simplifying payload for timeout[/blue]")
        
        # In a real implementation, we would extract only essential data
        # For now, just retry the same endpoint
        return error.endpoint
    
    async def _generic_fallback(self, error: MatchError, spec: dict) -> Optional[str]:
        """Final fallback strategy."""
        if self.mode == ErrorMode.INTERACTIVE:
            console.print(f"[red]❌ Could not recover from error: {error.error_msg}[/red]")
            console.print("[cyan]Options: [r]etry, [s]kip, [e]dit endpoint, [q]uit[/cyan]")
            choice = input("Choose option: ").lower()
            
            if choice == 'r' and error.endpoint:
                return error.endpoint
            elif choice == 'e':
                new_endpoint = input("Enter endpoint (e.g., POST /api/v1/users): ")
                return new_endpoint
            elif choice == 's':
                return None
            else:
                return None
        
        console.print("[red]❌ Error recovery failed[/red]")
        return None
    
    def _extract_intent(self, md_content: str) -> str:
        """Extract intent from markdown content."""
        # Remove images and code blocks
        text = re.sub(r'!\[.*?\]\(.*?\)|```.*?```', '', md_content, flags=re.DOTALL)
        
        # Extract headers
        headers = re.findall(r'^#+\s*(.*?)$', text, re.MULTILINE)
        
        # Keep first paragraph
        first_para = re.split(r'\n\n', text.strip())[0] if text.strip() else ""
        
        intent = " ".join(headers[:3] + [first_para[:200]])
        return intent[:500]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text."""
        keywords = []
        
        # Add fallback keywords if they appear in text
        for kw in self.fallback_keywords:
            if kw in text:
                keywords.append(kw)
        
        # Extract words that might be API-related
        api_words = re.findall(r'\b(user|file|image|data|message|email|post|comment|task|project)\b', text)
        keywords.extend(api_words)
        
        return list(set(keywords))
    
    def _confirm_fix(self) -> bool:
        """Confirm LLM fix in interactive mode."""
        while True:
            choice = input("Accept this fix? [y/n]: ").lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("Please enter y or n")
