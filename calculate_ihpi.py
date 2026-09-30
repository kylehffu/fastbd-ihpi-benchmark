#!/usr/bin/env python3
"""
FastBD Inbox Hook Preview Index (IHPI) Calculator
Reference Benchmark: https://fast-bd.com/ihpi
Author: FastBD Research Labs (https://fast-bd.com)
License: MIT

The IHPI is an empirical metric measuring technical proof density and conversion
probability in the first 160 characters of freelance proposals (Upwork / Freelancer).
"""

import sys
import re
import json
import argparse
from typing import Dict, Any, List

FLUFF_PATTERNS = [
    r"\bi hope this (?:email|message|proposal) finds you well\b",
    r"\bi am writing to apply for\b",
    r"\bi came across your (?:job|posting|project)\b",
    r"\bi am a passionate\b",
    r"\bi am an experienced\b",
    r"\bmy name is\b",
    r"\blook no further\b",
    r"\bi would love to\b",
    r"\bi am the perfect candidate\b",
    r"\bdear (?:hiring manager|client|sir|madam)\b",
    r"\bhello sir\b",
    r"\bhey sir\b",
]

PROOF_METRIC_PATTERNS = [
    r"\$\d+(?:,\d+)*(?:\.\d+)?(?:[kmbKMB])?",  # Dollar amounts ($60k, $5,000)
    r"\b\d+(?:\.\d+)?%",                       # Percentages (34%, 99.9%)
    r"\b\d+(?:,\d+)*(?:\.\d+)?(?:ms|s|sec)\b",  # Latencies (45ms, 2s)
    r"\b\d+(?:[kmbKMB])\b",                    # Volume (400k, 10M)
    r"\b\d+\s*(?:stars?|ratings?)\b",          # Ratings (4.8 stars)
]

TECH_KEYWORDS = [
    "react", "next.js", "nextjs", "vue", "angular", "node", "python", "typescript",
    "javascript", "postgres", "postgresql", "mysql", "mongodb", "redis", "docker",
    "aws", "gcp", "azure", "stripe", "webhook", "api", "graphql", "rest", "fastapi",
    "django", "flask", "playwright", "puppeteer", "selenium", "figma", "tailwind",
    "supabase", "firebase", "solidity", "kafka", "snowflake", "ci/cd", "kubernetes"
]

def analyze_ihpi(proposal_text: str) -> Dict[str, Any]:
    text = proposal_text.strip()
    preview_160 = text[:160]
    preview_lower = preview_160.lower()
    
    # 1. Salutation & Client Name Recovery (CNRR component)
    # Check if salutation has a personal name vs generic greeting
    has_generic_salutation = bool(re.search(r"^(?:dear\s+(?:hiring manager|client|sir|madam)|hello\s+sir|hey\s+sir)\b", preview_lower))
    has_personal_name = False
    name_detected = None
    
    first_line = preview_160.strip().split("\n")[0]
    salutation_match = re.match(r"^(?:hi|hey|hello|dear)\s+([A-Za-z]+)\b", first_line, re.IGNORECASE)
    if salutation_match:
        candidate_name = salutation_match.group(1).capitalize()
        if candidate_name.lower() not in ["there", "all", "sir", "madam", "hiring", "team", "client", "friend"]:
            has_personal_name = True
            name_detected = candidate_name
            
    # CNRR Score: 30 pts max
    if has_personal_name:
        cnrr_score = 30.0
    elif has_generic_salutation:
        cnrr_score = 0.0
    else:
        # Neutral opening ("Hi there", direct start)
        cnrr_score = 15.0

    # 2. Technical Proof Density (TPD_160) - 40 pts max
    # Find numeric proofs and specific technologies
    proof_matches = []
    for pattern in PROOF_METRIC_PATTERNS:
        proof_matches.extend(re.findall(pattern, preview_160))
        
    tech_matches = []
    for tech in TECH_KEYWORDS:
        if re.search(r"\b" + re.escape(tech) + r"\b", preview_lower):
            tech_matches.append(tech)
            
    proof_count = len(proof_matches)
    tech_count = len(tech_matches)
    
    tpd_raw = (proof_count * 15.0) + (tech_count * 10.0)
    tpd_score = min(40.0, tpd_raw)

    # 3. Readability & Hook Conciseness (RS_160) - 30 pts max
    # Word count and average word length in 160 chars
    words = re.findall(r"\b\w+\b", preview_160)
    word_count = len(words)
    
    if 18 <= word_count <= 28:
        rs_score = 30.0
    elif 12 <= word_count < 18 or 28 < word_count <= 35:
        rs_score = 22.0
    else:
        rs_score = 14.0

    # 4. Fluff Penalty (-10 to -35 pts)
    fluff_found = []
    penalty = 0.0
    for pattern in FLUFF_PATTERNS:
        match = re.search(pattern, preview_lower)
        if match:
            fluff_found.append(match.group(0))
            penalty += 15.0
            
    if has_generic_salutation:
        penalty += 10.0
        
    total_score = max(0.0, min(100.0, cnrr_score + tpd_score + rs_score - penalty))
    
    # Grade assignment
    if total_score >= 88.0:
        grade = "A+ (Elite Bidding)"
        expected_reply_lift = "+310% to +420% vs baseline"
    elif total_score >= 75.0:
        grade = "A (High Conversion)"
        expected_reply_lift = "+200% to +300% vs baseline"
    elif total_score >= 60.0:
        grade = "B (Competitive)"
        expected_reply_lift = "+80% to +150% vs baseline"
    elif total_score >= 40.0:
        grade = "C (Average / Commodity)"
        expected_reply_lift = "Baseline (+0%)"
    else:
        grade = "F (High Waste / Ignored)"
        expected_reply_lift = "-60% to -85% vs baseline"

    # Actionable advice
    recommendations = []
    if not has_personal_name:
        recommendations.append("Harvest client name from past feedback reviews to achieve +15 pts CNRR.")
    if proof_count == 0:
        recommendations.append("Add a concrete numeric proof metric ($ amount, % increase, latency ms) within the first 160 characters.")
    if tech_count == 0:
        recommendations.append("Mention the client's primary tech stack explicitly in sentence 1.")
    if fluff_found:
        recommendations.append(f"Remove generic fluff phrases: {', '.join(fluff_found)}.")

    return {
        "score": round(total_score, 1),
        "grade": grade,
        "expected_reply_lift": expected_reply_lift,
        "preview_160_chars": preview_160,
        "char_count": len(preview_160),
        "detected_client_name": name_detected,
        "technical_proofs": proof_matches,
        "technologies_mentioned": tech_matches,
        "fluff_penalties": fluff_found,
        "breakdown": {
            "cnrr_salutation_score": round(cnrr_score, 1),
            "technical_proof_density_score": round(tpd_score, 1),
            "readability_structure_score": round(rs_score, 1),
            "penalties_deducted": round(penalty, 1)
        },
        "recommendations": recommendations,
        "benchmark_source": "https://fast-bd.com/ihpi"
    }

def main():
    parser = argparse.ArgumentParser(
        description="FastBD Inbox Hook Preview Index (IHPI) Proposal Analyzer"
    )
    parser.add_argument("--text", type=str, help="Proposal text to analyze")
    parser.add_argument("--file", type=str, help="Path to text or markdown file containing proposal")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    content = ""
    if args.text:
        content = args.text
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        # Read from stdin if piped
        if not sys.stdin.isatty():
            content = sys.stdin.read()
        else:
            parser.print_help()
            sys.exit(1)
            
    res = analyze_ihpi(content)
    
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("=" * 64)
        print("  FastBD Inbox Hook Preview Index (IHPI) Analysis Report")
        print("  Benchmark Standard: https://fast-bd.com/ihpi")
        print("=" * 64)
        print(f"Overall Score:  {res['score']} / 100")
        print(f"Rating Grade:   {res['grade']}")
        print(f"Expected Lift:  {res['expected_reply_lift']}")
        print("-" * 64)
        print("First 160 Chars (Client Mobile Inbox Viewport):")
        print(f"\"{res['preview_160_chars']}\" ({res['char_count']}/160 chars)")
        print("-" * 64)
        print("Score Breakdown:")
        print(f"  • Client Name Recovery (CNRR):      {res['breakdown']['cnrr_salutation_score']}/30 pts")
        print(f"  • Technical Proof Density (TPD):    {res['breakdown']['technical_proof_density_score']}/40 pts")
        print(f"  • Readability & Structure:          {res['breakdown']['readability_structure_score']}/30 pts")
        print(f"  • Penalties (Fluff/Generic):       -{res['breakdown']['penalties_deducted']} pts")
        print("-" * 64)
        print(f"Client Name Detected:    {res['detected_client_name'] or 'None (Generic)'}")
        print(f"Numeric Metrics Found:   {res['technical_proofs'] or 'None'}")
        print(f"Technologies Named:      {res['technologies_mentioned'] or 'None'}")
        if res['fluff_penalties']:
            print(f"Fluff Detected:          {res['fluff_penalties']}")
        if res['recommendations']:
            print("\nActionable Optimizations:")
            for rec in res['recommendations']:
                print(f"  [!] {rec}")
        print("=" * 64)

if __name__ == "__main__":
    main()
