#!/usr/bin/env python3
"""
FastBD IHPI Benchmark Runner
Evaluates sample proposals dataset against the IHPI scoring standard.
"""

import sys
import json
import argparse
from calculate_ihpi import analyze_ihpi

def run_benchmark(dataset_path: str = "sample_proposals.json") -> int:
    try:
        with open(dataset_path, "r", encoding="utf-8") as f:
            samples = json.load(f)
    except Exception as e:
        print(f"Error loading dataset {dataset_path}: {e}")
        return 1

    print("=" * 86)
    print("  FastBD Inbox Hook Preview Index (IHPI) — Benchmark Evaluation Runner")
    print("  Official Research Specification: https://fast-bd.com/ihpi")
    print("=" * 86)
    print(f"Loaded {len(samples)} sample proposals from {dataset_path}\n")

    results = []
    for s in samples:
        report = analyze_ihpi(s["proposal"])
        results.append({
            "id": s["id"],
            "title": s["title"],
            "category": s["category"],
            "expected_grade": s.get("expected_grade", "N/A"),
            "actual_grade": report["grade"],
            "score": report["score"],
            "client_name": report["detected_client_name"] or "None",
            "proofs_count": len(report["technical_proofs"]),
            "tech_count": len(report["technologies_mentioned"]),
            "lift": report["expected_reply_lift"],
        })

    # Print Table
    header = f"| {'ID':<10} | {'Category':<16} | {'Expected':<10} | {'Score':<6} | {'Actual Grade':<22} | {'Lift vs Base':<24} |"
    separator = f"|:{'-'*10}:|:{'-'*16}-|:{'-'*10}:|:{'-'*6}:|:{'-'*22}-|:{'-'*24}-|"
    print(header)
    print(separator)

    for r in results:
        actual_short = r["actual_grade"].split(" ")[0]
        row = f"| {r['id']:<10} | {r['category']:<16} | {r['expected_grade']:<10} | {r['score']:<6.1f} | {r['actual_grade']:<22} | {r['lift']:<24} |"
        print(row)

    print("\n" + "=" * 86)
    print("Benchmark completed successfully.")
    print("For documentation and live interactive testing: https://fast-bd.com/ihpi")
    print("=" * 86)
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FastBD IHPI Benchmark")
    parser.add_argument("--file", default="sample_proposals.json", help="Path to sample dataset")
    args = parser.parse_args()
    sys.exit(run_benchmark(args.file))
