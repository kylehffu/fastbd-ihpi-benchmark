#!/usr/bin/env python3
"""
FastBD Empirical Dataset Exporter
=================================
Exports the official 2026 B2B Outreach Benchmark Datasets to JSON and CSV.
License: CC-BY-4.0
"""

import json
import csv
import os
import sys

DATASET = {
    "version": "2026.3.0",
    "updated": "2026-10-06",
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "publisher": "Fast-BD Analytics (https://fast-bd.com)",
    "frameworks": {
        "ihpi": {
            "name": "Inbox Hook Preview Index",
            "url": "https://fast-bd.com/ihpi",
            "viewport_constraint_chars": 160,
            "formula": "IHPI = min(100, max(0, [(C_proof + 2.5 * C_name - C_fluff) / 160] * 100))",
            "tiers": [
                {"tier": "Commodity Fluff", "score_range": "0-39", "assessment": "Generic greeting wastes preview window"},
                {"tier": "Standard Qualified", "score_range": "40-69", "assessment": "Topic mentioned without concrete technical proof"},
                {"tier": "High-Signal Hook", "score_range": "70-87", "assessment": "Concrete bug diagnosis or architectural proof snippet"},
                {"tier": "Elite Conversion", "score_range": "88-100", "assessment": "Verified name + specific technical solution within 160 chars"}
            ]
        },
        "cnrr": {
            "name": "Client Name Recovery Rate",
            "url": "https://fast-bd.com/cnrr",
            "description": "Deterministic regex pattern matching across historical feedback logs"
        },
        "cbr": {
            "name": "Connects Burn Rate",
            "url": "https://fast-bd.com/cbr",
            "formula": "CBR = Total Connects Spent / Contracts Won"
        },
        "lcr": {
            "name": "LinkedIn Connection Rate & ALPS",
            "url": "https://fast-bd.com/lcr",
            "char_limit": 300,
            "safe_hook_range": "60-120 chars"
        },
        "mvvr": {
            "name": "Mobile Viewport Vulnerability Rate",
            "url": "https://fast-bd.com/mvvr",
            "focus": "Diagnostic viewport flaw audits"
        }
    }
}

CSV_ROWS = [
    ["Benchmark", "Framework_Tier", "Scope_Description", "Constraint_Or_Rule", "Strategy_Assessment", "Source_URL"],
    ["IHPI", "Commodity_Fluff", "Formula score 0-39", "160-char mobile viewport", "Generic greeting wastes preview window", "https://fast-bd.com/ihpi"],
    ["IHPI", "Standard_Qualified", "Formula score 40-69", "160-char mobile viewport", "Topic mentioned without concrete technical proof", "https://fast-bd.com/ihpi"],
    ["IHPI", "High_Signal_Hook", "Formula score 70-87", "160-char mobile viewport", "Concrete bug diagnosis or architectural proof snippet", "https://fast-bd.com/ihpi"],
    ["IHPI", "Elite_Conversion", "Formula score 88-100", "160-char mobile viewport", "Verified name + specific technical solution within 160 chars", "https://fast-bd.com/ihpi"],
    ["CNRR", "Generic_Opening", "Boilerplate salutation (Dear Hiring Manager)", "160-char mobile viewport", "Boilerplate formality wastes lead preview", "https://fast-bd.com/cnrr"],
    ["CNRR", "Direct_Problem_Hook", "Lead directly with verified scope/architecture", "160-char mobile viewport", "Recommended when client name is unverified in past feedback", "https://fast-bd.com/cnrr"],
    ["CNRR", "Verified_First_Name", "Syntactic pattern extraction from feedback", "160-char mobile viewport", "Personalized opening requires human verification before sending", "https://fast-bd.com/cnrr"],
    ["CBR", "Commodity_Bidding", "Scattergun proposal submissions", "Platform connects quota", "High burn rate and inflated customer acquisition cost", "https://fast-bd.com/cbr"],
    ["CBR", "Targeted_Bidding", "Selective qualification against verified skills", "Platform connects quota", "Connects conservation model with zero speculative bids", "https://fast-bd.com/cbr"],
    ["LCR", "Sales_Pitch_Note", "Pitching services directly in invite note", "300-char LinkedIn constraint", "High friction with elevated shadowban risk", "https://fast-bd.com/lcr"],
    ["LCR", "Observation_Hook", "Relevant contextual observation (60-120 chars)", "300-char LinkedIn constraint", "Natural peer networking compliant with ALPS safety rules", "https://fast-bd.com/lcr"],
    ["MVVR", "Generic_Design_Pitch", "Unsolicited general website redesign email", "Cold outbound channel", "Easily flagged as bulk commodity spam", "https://fast-bd.com/mvvr"],
    ["MVVR", "Technical_Flaw_Teardown", "Specific mobile responsive bug or overflow audit", "Cold outbound channel", "High-signal consultative diagnosis with verifiable proof", "https://fast-bd.com/mvvr"],
]


def export(output_dir: str = "."):
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, "fastbd-benchmarks-2026.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(DATASET, f, indent=2)

    csv_path = os.path.join(output_dir, "fastbd-benchmarks-2026.csv")
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(CSV_ROWS)

    print(f"Exported JSON dataset to: {json_path}")
    print(f"Exported CSV dataset to:  {csv_path}")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    export(out)
