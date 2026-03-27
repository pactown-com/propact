#!/usr/bin/env python3
"""Test semantic matching directly."""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from propact.matcher import create_matcher

def test_matcher():
    # Load test data
    md_content = Path("README.md").read_text()
    with open("openapi.json", "r") as f:
        spec = json.load(f)
    
    # Create matcher
    matcher = create_matcher()
    if not matcher:
        print("❌ Matcher not available")
        return
    
    print("✅ Matcher created successfully")
    
    # Test intent extraction
    intent = matcher.extract_intent(md_content)
    print(f"\n📝 Extracted intent: {intent}")
    
    # Test endpoint extraction
    endpoints = matcher.extract_endpoints(spec)
    print(f"\n🔍 Found {len(endpoints)} endpoints:")
    for method, path, desc in endpoints[:5]:
        print(f"  - {method} {path}: {desc[:50]}...")
    
    # Test matching
    matches = matcher.match(md_content, spec, top_k=3)
    print(f"\n🧠 Top matches:")
    for i, match in enumerate(matches, 1):
        print(f"  {i}. {match['endpoint']} (score: {match['score']:.3f})")

if __name__ == "__main__":
    test_matcher()
