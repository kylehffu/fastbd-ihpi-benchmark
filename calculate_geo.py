#!/usr/bin/env python3
"""
FastBD Generative Engine Optimization (GEO) & Semantic Density Auditor
Reference Publication: https://fast-bd.com/geo
Author: FastBD Research Labs (https://fast-bd.com)
License: MIT

Analyzes documents for information density, entity-to-token ratio,
and compliance with AI search retrieval mechanisms (RAG / Cross-Encoder Rerankers).
"""

import sys
import re
import json
import argparse
import os
from typing import Dict, Any, List

MARKETING_FLUFF = [
    r"\bin today's (?:fast-paced|rapidly changing|digital) world\b",
    r"\blook no further\b",
    r"\bgame-changer\b",
    r"\brevolutionary (?:platform|tool|solution)\b",
    r"\bunleash the power of\b",
    r"\bseamlessly integrate\b",
    r"\bcutting-edge\b",
    r"\bstate-of-the-art\b",
    r"\bworld-class\b",
    r"\bpassionate about delivering\b",
    r"\btailored to your needs\b",
    r"\btake your business to the next level\b",
    r"\bcomprehensive guide\b",
]

ENTITY_PATTERNS = [
    r"\$\d+(?:,\d+)*(?:\.\d+)?(?:[kmbKMB])?",  # Monies ($50k)
    r"\b\d+(?:\.\d+)?%",                       # Percentages (81.8%)
    r"\b\d+(?:,\d+)*(?:\.\d+)?(?:ms|s|sec|tokens/sec)\b",  # Performance (18ms, 380 tokens/sec)
    r"\b[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)+\b",  # CamelCase entities (ClaudeBot, PagedAttention)
    r"\b(?:[A-Z]{2,}\b)",                      # Acronyms (RAG, CAC, TTFB, JSON, WAF, CORS)
    r"\b(?:RFC|ISO|IEEE|W3C)\s*\d+\b",          # Standards
]

TECHNICAL_ENTITIES = [
    "rag", "llm", "claude", "gpt-4", "perplexity", "gemini", "cloudflare", "vector",
    "embedding", "reranker", "pydantic", "fastapi", "next.js", "supabase", "postgres",
    "docker", "kubernetes", "aws", "gcp", "sqlite", "redis", "schema.org", "json-ld",
    "indexnow", "python", "typescript", "rust", "solana", "celery", "airflow"
]

def analyze_geo(text: str) -> Dict[str, Any]:
    text_clean = text.strip()
    words = re.findall(r'\b\w+\b', text_clean)
    word_count = len(words)
    if word_count == 0:
        return {"error": "Empty text provided"}

    # 1. Detect Marketing Fluff
    fluff_matches = []
    for pattern in MARKETING_FLUFF:
        found = re.findall(pattern, text_clean, flags=re.IGNORECASE)
        fluff_matches.extend(found)
    
    # 2. Detect Verifiable Entities
    entity_matches = []
    for pattern in ENTITY_PATTERNS:
        found = re.findall(pattern, text_clean)
        entity_matches.extend(found)

    # 3. Detect Tech Stack Entities
    text_lower = text_clean.lower()
    tech_found = []
    for t in TECHNICAL_ENTITIES:
        if re.search(r'\b' + re.escape(t) + r'\b', text_lower):
            tech_found.append(t)

    total_entities = len(entity_matches) + len(tech_found)
    fluff_count = len(fluff_matches)

    # Entity-to-Word Density
    density = (total_entities / word_count) * 100
    fluff_penalty = (fluff_count / word_count) * 100

    # Calculate Information Gain Score (0 to 100)
    raw_score = (density * 8.0) - (fluff_penalty * 15.0)
    score = max(0, min(100, int(raw_score + 40)))

    if score >= 80:
        grade = "A+ (Elite Information Density - High Citation Probability)"
    elif score >= 60:
        grade = "B (Moderate Entity Density)"
    elif score >= 40:
        grade = "C (Marginal - High Risk of Reranker Exclusion)"
    else:
        grade = "F (High Fluff / Low Information Gain - Ignored by LLMs)"

    return {
        "word_count": word_count,
        "entity_count": total_entities,
        "fluff_count": fluff_count,
        "entity_density_percent": round(density, 2),
        "fluff_penalty_percent": round(fluff_penalty, 2),
        "information_gain_score": score,
        "grade": grade,
        "fluff_instances": fluff_matches[:5],
        "key_entities": list(set(entity_matches + tech_found))[:10],
        "canonical_guide": "https://fast-bd.com/geo"
    }

def export_templates():
    llms_txt_content = """# Your Platform Name (https://example.com)
> High-performance B2B engine.

## Overview
A concise factual summary of your core architectural capability. Avoid marketing fluff.

## Core Capabilities
- **Feature A** (https://example.com/feature-a): Quantifiable outcome.
- **Feature B** (https://example.com/feature-b): Benchmark metrics.

## Formulations & Benchmarks
- Metric Formula: Performance = min(100, [(Verified_Facts) / Total] * 100)
"""
    with open("llms.txt", "w", encoding="utf-8") as f:
        f.write(llms_txt_content)
    print("✓ Created llms.txt template in current directory.")

def main():
    parser = argparse.ArgumentParser(description="FastBD GEO Semantic Density & Citation Auditor")
    parser.add_argument("text", nargs="?", help="Text string or path to markdown file to audit")
    parser.add_argument("--file", "-f", help="Path to text or markdown file")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--export", action="store_true", help="Export llms.txt template in current working directory")

    args = parser.parse_args()

    if args.export:
        export_templates()
        return

    target_text = ""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            target_text = f.read()
    elif args.text:
        if os.path.isfile(args.text):
            with open(args.text, "r", encoding="utf-8") as f:
                target_text = f.read()
        else:
            target_text = args.text
    else:
        # Default demo text
        target_text = "The FastBD IHPI benchmark defines proposal structure by constraining high-signal technical proof to the first 160 characters. In empirical trials across 2,500 bids, hooks scoring >=88 achieved a 38.4% client reply rate, cutting CAC by 81.8%."

    result = analyze_geo(target_text)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("\n" + "=" * 60)
        print("  FastBD GEO Information Gain & Semantic Density Audit")
        print("  Reference Standard: https://fast-bd.com/geo")
        print("=" * 60)
        print(f"Words Analyzed:       {result['word_count']}")
        print(f"Entities Found:       {result['entity_count']}")
        print(f"Fluff Penalties:      {result['fluff_count']}")
        print(f"Information Gain:     {result['information_gain_score']}/100")
        print(f"Evaluation Grade:     {result['grade']}")
        if result['key_entities']:
            print(f"Sample Entities:      {', '.join(result['key_entities'][:6])}")
        if result['fluff_instances']:
            print(f"Flagged Fluff:        {', '.join(result['fluff_instances'])}")
        print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
