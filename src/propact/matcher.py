"""Semantic endpoint matcher for Propact using embeddings."""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import json

# Optional dependencies for semantic matching
try:
    import numpy as np
    from sentence_transformers import SentenceTransformer
    HAS_SEMANTIC = True
except ImportError:
    HAS_SEMANTIC = False
    np = None
    SentenceTransformer = None

try:
    from prance import ResolvingParser
    HAS_PRANCE = True
except ImportError:
    HAS_PRANCE = False
    ResolvingParser = None

# Import error handler
from .error_handler import PropactErrorHandler, MatchError, ErrorMode

# Import LLM proxy for enhanced matching
try:
    from .llm_proxy import LiteLLMProxy, match_intent
    HAS_LLM = True
except ImportError:
    HAS_LLM = False
    LiteLLMProxy = None
    match_intent = None


class EndpointMatcher:
    """Matches markdown content to OpenAPI endpoints using semantic similarity."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", error_handler: Optional[PropactErrorHandler] = None):
        """Initialize the matcher with a sentence transformer model."""
        if not HAS_SEMANTIC:
            raise ImportError(
                "Semantic matching requires sentence-transformers and numpy. "
                "Install with: pip install propact[semantic]"
            )
        
        self.embedder = SentenceTransformer(model_name)
        self.model_name = model_name
        self.error_handler = error_handler or PropactErrorHandler(ErrorMode.RECOVER)
    
    def extract_intent(self, md_content: str) -> str:
        """Extract intent from markdown content."""
        # Remove images and code blocks
        text = re.sub(r'!\[.*?\]\(.*?\)|```.*?```', '', md_content, flags=re.DOTALL)
        
        # Extract headers and comments
        headers = re.findall(r'^#+\s*(.*?)$', text, re.MULTILINE)
        
        # Keep first paragraph
        first_para = re.split(r'\n\n', text.strip())[0] if text.strip() else ""
        
        # Combine intent signals
        intent_parts = []
        if headers:
            intent_parts.append(" ".join(headers[:3]))  # Top 3 headers
        if first_para:
            intent_parts.append(first_para[:200])  # First 200 chars
        
        intent = " ".join(intent_parts).strip()
        return intent[:500]  # Limit to 500 characters
    
    def extract_endpoints(self, openapi_spec: Dict[str, Any]) -> List[Tuple[str, str, str]]:
        """Extract endpoints from OpenAPI spec.
        
        Returns:
            List of (method, path, description) tuples.
        """
        endpoints = []
        
        if not openapi_spec or "paths" not in openapi_spec:
            return endpoints
        
        for path, path_item in openapi_spec["paths"].items():
            for method, operation in path_item.items():
                if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                    # Prioritize LLM-enhanced descriptions
                    description = ""
                    
                    # Use x-enhanced-description from openapi-llm if available
                    if "x-enhanced-description" in operation:
                        description = operation["x-enhanced-description"]
                    else:
                        # Fallback to standard OpenAPI fields
                        summary = operation.get("summary", "")
                        op_description = operation.get("description", "")
                        llm_intent = operation.get("x-llm-intent", "")
                        description = f"{summary} {op_description} {llm_intent}".strip()
                    
                    # Add operationId if available
                    if "operationId" in operation:
                        description += f" {operation['operationId']}"
                    
                    endpoints.append((method.upper(), path, description))
        
        return endpoints
    
    def compute_similarities(self, intent: str, endpoints: List[Tuple[str, str, str]]) -> List[Tuple[str, str, float]]:
        """Compute similarity scores between intent and endpoints."""
        if not endpoints:
            return []
        
        # Embed intent
        intent_emb = self.embedder.encode(intent)
        
        # Embed all endpoint descriptions
        descriptions = [desc for _, _, desc in endpoints]
        desc_embeddings = self.embedder.encode(descriptions)
        
        # Compute cosine similarities
        similarities = np.dot(desc_embeddings, intent_emb) / (
            np.linalg.norm(desc_embeddings, axis=1) * np.linalg.norm(intent_emb)
        )
        
        # Return with scores
        results = []
        for (method, path, _), score in zip(endpoints, similarities):
            results.append((method, path, float(score)))
        
        return results
    
    async def match(self, md_content: str, openapi_spec: Dict[str, Any], top_k: int = 3) -> List[Dict[str, Any]]:
        """Match markdown content to best endpoints with error recovery.
        
        Args:
            md_content: Markdown content to analyze
            openapi_spec: OpenAPI specification dictionary
            top_k: Number of top matches to return
            
        Returns:
            List of matches with method, path, and score
        """
        if not HAS_SEMANTIC:
            return []
        
        # Extract intent from markdown
        intent = self.extract_intent(md_content)
        
        # Extract endpoints from spec
        endpoints = self.extract_endpoints(openapi_spec)
        
        if not endpoints:
            return []
        
        # Compute similarities
        similarities = self.compute_similarities(intent, endpoints)
        
        # Sort by score (descending)
        similarities.sort(key=lambda x: x[2], reverse=True)
        
        # Check if best match has sufficient confidence
        best_score = similarities[0][2] if similarities else 0.0
        
        # If confidence is too low, try error recovery
        if best_score < 0.3 and self.error_handler:
            error = MatchError(
                type="no_match",
                confidence=best_score,
                error_msg=f"No good match found (best score: {best_score:.3f})",
                candidates=[{"method": m, "path": p, "score": s} for m, p, s in similarities[:3]]
            )
            
            # Try to recover
            recovered_endpoint = await self.error_handler.handle_match_failure(
                error, md_content, openapi_spec
            )
            
            if recovered_endpoint:
                # Parse recovered endpoint
                parts = recovered_endpoint.split(' ', 1)
                if len(parts) == 2:
                    method, path = parts
                    # Return as a high-confidence match
                    return [{
                        "method": method,
                        "path": path,
                        "score": 0.5,  # Moderate confidence for recovered matches
                        "endpoint": recovered_endpoint,
                        "recovered": True
                    }]
        
        # Format results
        results = []
        for method, path, score in similarities[:top_k]:
            results.append({
                "method": method,
                "path": path,
                "score": score,
                "endpoint": f"{method} {path}",
                "recovered": False
            })
        
        return results
    
    async def match_from_file(self, md_path: str, openapi_path: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Match from file paths.
        
        Args:
            md_path: Path to markdown file
            openapi_path: Path to OpenAPI spec file
            top_k: Number of top matches to return
            
        Returns:
            List of matches
        """
        # Read markdown
        md_content = Path(md_path).read_text()
        
        # Load OpenAPI spec
        if openapi_path.endswith('.json'):
            with open(openapi_path, 'r') as f:
                spec = json.load(f)
        elif HAS_PRANCE:
            parser = ResolvingParser(openapi_path)
            spec = parser.specification
        else:
            raise ImportError(
                "Parsing YAML OpenAPI specs requires prance. "
                "Install with: pip install propact[semantic]"
            )
        
        return await self.match(md_content, spec, top_k)


def create_matcher(model_name: str = "all-MiniLM-L6-v2", error_handler: Optional[PropactErrorHandler] = None) -> Optional[EndpointMatcher]:
    """Create an EndpointMatcher if dependencies are available."""
    if not HAS_SEMANTIC:
        return None
    return EndpointMatcher(model_name, error_handler)


class OpenAPILLMMatcher:
    """LLM-based semantic matcher for fast/accurate endpoint selection.
    
    Uses LiteLLM for multi-provider support - can switch between:
    - groq: Fast matching (<200ms)
    - anthropic: Accurate for complex cases
    - local: Offline Ollama support
    """
    
    def __init__(
        self, 
        fast_provider: str = "groq",
        accurate_provider: str = "anthropic"
    ):
        """Initialize LLM matcher with provider configuration.
        
        Args:
            fast_provider: Provider for quick matching (groq, local)
            accurate_provider: Provider for accurate reasoning (anthropic, cloud)
        """
        if not HAS_LLM:
            raise ImportError(
                "LLM matching requires litellm. "
                "Install with: pip install litellm"
            )
        
        self.llm_fast = LiteLLMProxy(fast_provider)
        self.llm_accurate = LiteLLMProxy(accurate_provider)
    
    async def _llm_select(
        self, 
        intent: str, 
        candidates: list, 
        spec: dict,
        use_accurate: bool = False
    ) -> dict:
        """Use LLM to select best endpoint.
        
        Args:
            intent: User intent/query
            candidates: List of candidate endpoint dicts
            spec: Full OpenAPI spec for context
            use_accurate: Use accurate provider instead of fast
            
        Returns:
            Selected endpoint info
        """
        llm = self.llm_accurate if use_accurate else self.llm_fast
        
        candidates_str = "\n".join([
            f"- {c.get('method', 'GET')} {c.get('path', '/')} : {c.get('description', 'N/A')}"
            for c in candidates[:10]  # Limit to top 10
        ])
        
        prompt = f"""Select the best API endpoint for this intent.

Intent: "{intent}"

Candidate Endpoints:
{candidates_str}

Respond with ONLY the selected endpoint path (e.g., "GET /weather/forecast"), nothing else."""

        response = await llm.generate(prompt, temperature=0.1)
        selected = response.strip()
        
        # Parse response
        parts = selected.split(' ', 1)
        if len(parts) == 2:
            method, path = parts
        else:
            method, path = "GET", selected
        
        return {
            "method": method,
            "path": path,
            "endpoint": f"{method} {path}",
            "llm_selected": True
        }
    
    async def match(
        self, 
        md_content: str, 
        openapi_spec: Dict[str, Any],
        top_k: int = 3,
        use_accurate: bool = False
    ) -> List[Dict[str, Any]]:
        """Match markdown to endpoints using LLM.
        
        Args:
            md_content: Markdown content
            openapi_spec: OpenAPI spec dict
            top_k: Number of results (LLM returns best match)
            use_accurate: Use accurate provider
            
        Returns:
            List of matches (typically 1 from LLM)
        """
        # Extract intent
        intent = self._extract_intent(md_content)
        
        # Extract candidate endpoints
        candidates = self._extract_candidates(openapi_spec)
        
        if not candidates:
            return []
        
        # Use LLM to select
        selected = await self._llm_select(intent, candidates, openapi_spec, use_accurate)
        
        return [{
            "method": selected["method"],
            "path": selected["path"],
            "score": 0.9 if use_accurate else 0.8,  # High confidence for LLM
            "endpoint": selected["endpoint"],
            "recovered": False,
            "llm_matched": True
        }]
    
    def _extract_intent(self, md_content: str) -> str:
        """Extract intent from markdown."""
        # Remove code blocks
        text = re.sub(r'```.*?```', '', md_content, flags=re.DOTALL)
        # Get headers and first paragraph
        headers = re.findall(r'^#+\s*(.*?)$', text, re.MULTILINE)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        intent_parts = []
        if headers:
            intent_parts.extend(headers[:2])
        if paragraphs:
            intent_parts.append(paragraphs[0][:200])
        
        return " ".join(intent_parts).strip()[:500]
    
    def _extract_candidates(self, spec: Dict[str, Any]) -> list:
        """Extract endpoint candidates from spec."""
        candidates = []
        paths = spec.get("paths", {})
        
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.upper() in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                    description = " ".join([
                        operation.get("summary", ""),
                        operation.get("description", ""),
                        operation.get("operationId", "")
                    ]).strip()
                    
                    candidates.append({
                        "method": method.upper(),
                        "path": path,
                        "description": description
                    })
        
        return candidates
    
    async def hybrid_match(
        self,
        md_content: str,
        openapi_spec: Dict[str, Any],
        semantic_matcher: Optional[EndpointMatcher] = None,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """Hybrid matching: LLM + Semantic fallback.
        
        Args:
            md_content: Markdown content
            openapi_spec: OpenAPI spec
            semantic_matcher: Optional semantic matcher for fallback
            top_k: Number of results
            
        Returns:
            Combined results from both methods
        """
        # Try LLM first (fast)
        llm_results = await self.match(md_content, openapi_spec, use_accurate=False)
        
        # If LLM confidence is low and semantic available, combine
        if llm_results and llm_results[0].get("score", 0) < 0.7 and semantic_matcher:
            semantic_results = await semantic_matcher.match(md_content, openapi_spec, top_k)
            
            # Merge results, deduplicate by endpoint
            seen = {r["endpoint"] for r in llm_results}
            for r in semantic_results:
                if r["endpoint"] not in seen:
                    llm_results.append(r)
            
            # Re-sort by score
            llm_results.sort(key=lambda x: x["score"], reverse=True)
        
        return llm_results[:top_k]


def create_llm_matcher(
    fast_provider: str = "groq",
    accurate_provider: str = "anthropic"
) -> Optional[OpenAPILLMMatcher]:
    """Create an LLM-based matcher if litellm is available."""
    if not HAS_LLM:
        return None
    return OpenAPILLMMatcher(fast_provider, accurate_provider)
