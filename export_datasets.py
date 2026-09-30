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
    "updated": "2026-09-30",
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "publisher": "FastBD Research Labs (https://fast-bd.com)",
    "benchmarks": {
        "ihpi": {
            "name": "Inbox Hook Preview Index",
            "sample_size": 2500,
            "url": "https://fast-bd.com/ihpi",
            "tiers": [
                {"tier": "Commodity Fluff", "reply_rate": 0.048, "score_range": "0-39"},
                {"tier": "Standard Qualified", "reply_rate": 0.126, "score_range": "40-69"},
                {"tier": "High-Signal Hook", "reply_rate": 0.234, "score_range": "70-87"},
                {"tier": "Elite Conversion", "reply_rate": 0.382, "score_range": "88-100"}
            ]
        },
        "cnrr": {
            "name": "Client Name Recovery Rate",
            "sample_size": 18400,
            "recovery_rate": 0.734,
            "lift": 2.40,
            "url": "https://fast-bd.com/cnrr"
        },
        "cbr": {
            "name": "Connects Burn Rate",
            "sample_size": 2500,
            "url": "https://fast-bd.com/cbr",
            "commodity_cbr": 340,
            "commodity_cac": 51.00,
            "elite_cbr": 62,
            "elite_cac": 9.30
        },
        "lcr": {
            "name": "LinkedIn Connection Rate & ALPS",
            "sample_size": 14200,
            "url": "https://fast-bd.com/lcr",
            "pitch_acceptance": 0.142,
            "hook_acceptance": 0.437
        },
        "mvvr": {
            "name": "Mobile Viewport Vulnerability Rate",
            "sample_size": 8600,
            "url": "https://fast-bd.com/mvvr",
            "viewport_failure_rate": 0.412,
            "generic_pitch_reply": 0.012,
            "flaw_teardown_reply": 0.246
        }
    }
}

CSV_ROWS = [
    ["Benchmark", "Metric", "Category", "Sample_Size", "Primary_Value", "Lift_Or_Baseline", "Source_URL"],
    ["IHPI", "Reply_Rate", "Commodity_Fluff", 2500, "4.8%", "Baseline (0%)", "https://fast-bd.com/ihpi"],
    ["IHPI", "Reply_Rate", "Standard_Qualified", 2500, "12.6%", "+162%", "https://fast-bd.com/ihpi"],
    ["IHPI", "Reply_Rate", "High_Signal_Hook", 2500, "23.4%", "+387%", "https://fast-bd.com/ihpi"],
    ["IHPI", "Reply_Rate", "Elite_Conversion", 2500, "38.2%", "+695%", "https://fast-bd.com/ihpi"],
    ["CNRR", "Salutation_Reply_Rate", "Generic_Opening", 18400, "8.4%", "Baseline (0%)", "https://fast-bd.com/cnrr"],
    ["CNRR", "Salutation_Reply_Rate", "Neutral_Casual", 18400, "14.2%", "+69%", "https://fast-bd.com/cnrr"],
    ["CNRR", "Salutation_Reply_Rate", "Verified_First_Name", 18400, "28.6%", "+240%", "https://fast-bd.com/cnrr"],
    ["CBR", "Connects_Per_Contract", "Commodity_Bidding", 2500, "340 connects ($51.00 CAC)", "Baseline (0%)", "https://fast-bd.com/cbr"],
    ["CBR", "Connects_Per_Contract", "Standard_Bidding", 2500, "175 connects ($26.25 CAC)", "-48.5% Cost", "https://fast-bd.com/cbr"],
    ["CBR", "Connects_Per_Contract", "High_Signal_Bidding", 2500, "98 connects ($14.70 CAC)", "-71.2% Cost", "https://fast-bd.com/cbr"],
    ["CBR", "Connects_Per_Contract", "Elite_Hook_Bidding", 2500, "62 connects ($9.30 CAC)", "-81.8% Cost", "https://fast-bd.com/cbr"],
    ["LCR", "Connection_Acceptance_Rate", "Immediate_Sales_Pitch", 14200, "14.2%", "Baseline (0%)", "https://fast-bd.com/lcr"],
    ["LCR", "Connection_Acceptance_Rate", "Blank_No_Note", 14200, "28.4%", "+100%", "https://fast-bd.com/lcr"],
    ["LCR", "Connection_Acceptance_Rate", "Peer_Compliment", 14200, "31.8%", "+124%", "https://fast-bd.com/lcr"],
    ["LCR", "Connection_Acceptance_Rate", "Observation_Hook_60_120_Chars", 14200, "43.7%", "+207%", "https://fast-bd.com/lcr"],
    ["MVVR", "Outbound_Cold_Reply_Rate", "Generic_Design_Pitch", 8600, "1.2%", "Baseline (0%)", "https://fast-bd.com/mvvr"],
    ["MVVR", "Outbound_Cold_Reply_Rate", "Templated_Portfolio", 8600, "3.8%", "+216%", "https://fast-bd.com/mvvr"],
    ["MVVR", "Outbound_Cold_Reply_Rate", "Technical_Flaw_Teardown", 8600, "24.6%", "+1950%", "https://fast-bd.com/mvvr"],
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
