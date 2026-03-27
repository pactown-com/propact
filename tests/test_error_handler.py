#!/usr/bin/env python3
"""Test error recovery functionality."""

import sys
import json
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from propact.error_handler import PropactErrorHandler, MatchError, ErrorMode
from propact.matcher import create_matcher


async def test_no_match_recovery():
    """Test recovery when no good match is found."""
    print("\n=== Testing No Match Recovery ===")
    
    # Create a spec with no relevant endpoints
    spec = {
        "paths": {
            "/api/v1/invoices": {
                "post": {
                    "summary": "Create invoice",
                    "description": "Create a new invoice"
                }
            },
            "/api/v1/reports": {
                "get": {
                    "summary": "Generate report",
                    "description": "Generate financial report"
                }
            }
        }
    }
    
    md_content = "# Upload Image\nI need to upload a profile picture"
    
    # Create matcher with error handler
    error_handler = PropactErrorHandler(ErrorMode.DEBUG)
    matcher = create_matcher(error_handler=error_handler)
    
    # Test matching
    matches = await matcher.match(md_content, spec)
    
    print(f"Found {len(matches)} matches:")
    for match in matches:
        recovered = "🔄" if match.get("recovered") else "✓"
        print(f"  {recovered} {match['endpoint']} (score: {match['score']:.3f})")


async def test_validation_error_recovery():
    """Test LLM self-correction for validation errors."""
    print("\n=== Testing Validation Error Recovery ===")
    
    error = MatchError(
        type="validation",
        confidence=0.1,
        error_msg="Missing required field: email",
        candidates=[{"method": "POST", "path": "/users", "score": 0.1}],
        endpoint="POST /users"
    )
    
    md_content = "# Create User\nNew user signup with email: test@example.com"
    
    # Test with different error modes
    for mode in [ErrorMode.STRICT, ErrorMode.RECOVER, ErrorMode.DEBUG]:
        print(f"\nTesting with mode: {mode.value}")
        handler = PropactErrorHandler(mode)
        
        result = await handler.handle_match_failure(error, md_content, {})
        print(f"  Result: {result}")


async def test_fallback_search():
    """Test keyword-based fallback search."""
    print("\n=== Testing Fallback Search ===")
    
    spec = {
        "paths": {
            "/api/v1/files/upload": {
                "post": {
                    "summary": "Upload file",
                    "description": "Upload a file to storage"
                }
            },
            "/api/v1/users/create": {
                "post": {
                    "summary": "Create user",
                    "description": "Create a new user account"
                }
            }
        }
    }
    
    error = MatchError(
        type="no_match",
        confidence=0.0,
        error_msg="No match for upload image request",
        candidates=[]
    )
    
    handler = PropactErrorHandler(ErrorMode.DEBUG)
    result = await handler._fallback_search(error, spec)
    
    print(f"Fallback result: {result}")
    assert result == "POST /api/v1/files/upload", f"Expected upload endpoint, got {result}"


async def test_retry_logic():
    """Test exponential backoff retry logic."""
    print("\n=== Testing Retry Logic ===")
    
    error = MatchError(
        type="http_5xx",
        confidence=0.0,
        error_msg="Internal server error",
        candidates=[],
        endpoint="POST /api/test"
    )
    
    handler = PropactErrorHandler(ErrorMode.DEBUG, max_retries=2)
    
    # First retry
    result1 = await handler._retry_with_backoff(error)
    print(f"First retry: {result1}")
    assert result1 == "POST /api/test"
    
    # Second retry
    result2 = await handler._retry_with_backoff(error)
    print(f"Second retry: {result2}")
    assert result2 == "POST /api/test"
    
    # Third retry should fail (max retries reached)
    result3 = await handler._retry_with_backoff(error)
    print(f"Third retry: {result3}")
    assert result3 is None, "Should return None after max retries"


async def test_interactive_mode():
    """Test interactive mode (simulated)."""
    print("\n=== Testing Interactive Mode ===")
    
    # Note: This test would require user input, so we'll just show the structure
    error = MatchError(
        type="http_400",
        confidence=0.0,
        error_msg="Bad request: invalid parameter",
        candidates=[],
        endpoint="POST /api/test"
    )
    
    handler = PropactErrorHandler(ErrorMode.INTERACTIVE)
    print("Interactive mode would prompt user for input")
    print("Options: [r]etry, [s]kip, [e]dit endpoint, [q]uit")


async def main():
    """Run all error recovery tests."""
    print("🧪 Testing Propact Error Recovery System")
    
    await test_no_match_recovery()
    await test_validation_error_recovery()
    await test_fallback_search()
    await test_retry_logic()
    await test_interactive_mode()
    
    print("\n✅ All error recovery tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
