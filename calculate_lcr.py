#!/usr/bin/env python3
"""
FastBD LCR (LinkedIn Connection Rate) & ALPS (Account Longevity Protection Score) Engine
Part of the FastBD B2B Open Benchmark Suite (https://fast-bd.com/lcr).

Zero external dependencies - runs on pure Python 3.8+.
"""

import sys
import argparse

PITCH_BUZZWORDS = [
    "hop on a quick call", "quick call", "synergy", "synergies", "scale your business",
    "demo", "free consultation", "guarantee", "help you grow", "quick 15 min",
    "schedule a time", "our services", "boost your sales", "let's talk", "let's connect and chat"
]

def score_linkedin_note(note_text: str) -> dict:
    """
    Evaluates a candidate LinkedIn connection note against the 300-char boundary,
    mobile push truncation (120 chars), and pitch buzzword penalties.
    """
    clean_text = note_text.strip()
    char_len = len(clean_text)
    lower = clean_text.lower()
    
    detected_pitches = [bw for bw in PITCH_BUZZWORDS if bw in lower]
    
    if char_len == 0:
        predicted_lcr = 29.8
        tier = "Blank Request (Ghost Risk on Touch 2)"
    elif char_len <= 120 and not detected_pitches:
        predicted_lcr = 43.7
        tier = "Elite Observation Hook (Tier A+)"
    elif char_len <= 200:
        penalty = len(detected_pitches) * 4.0
        predicted_lcr = max(5.0, 21.5 - penalty)
        tier = "Average Pitch (Tier B)"
    else:
        penalty = len(detected_pitches) * 3.5
        predicted_lcr = max(4.0, 14.2 - penalty)
        tier = "High-Risk Wall of Text (Tier F)"
        
    return {
        "char_length": char_len,
        "is_mobile_friendly": char_len <= 120 and char_len > 0,
        "detected_pitches": detected_pitches,
        "predicted_lcr": round(predicted_lcr, 1),
        "tier": tier
    }

def calculate_alps(weekly_sent: int, spam_flags: int, pending_over_14d: int) -> float:
    """
    Calculates Account Longevity Protection Score (ALPS).
    Formula: ALPS = 100 * [1 - (5.0 * spam_flags + pending_over_14d) / weekly_sent]
    Safe operating zone: ALPS > 85.0.
    """
    if weekly_sent <= 0:
        return 100.0
    risk_factor = (spam_flags * 5.0 + pending_over_14d) / weekly_sent
    alps = max(0.0, 100.0 * (1.0 - risk_factor))
    return round(alps, 1)

def main():
    parser = argparse.ArgumentParser(description="FastBD LinkedIn Connection Rate (LCR) & ALPS Scorer")
    parser.add_argument("--note", type=str, help="Candidate LinkedIn connection note text")
    parser.add_argument("--weekly-sent", type=int, default=100, help="Total weekly invitations sent")
    parser.add_argument("--spam-flags", type=int, default=0, help="Recipients clicking 'I don't know this person'")
    parser.add_argument("--pending-14d", type=int, default=5, help="Unaccepted pending requests older than 14 days")
    
    args = parser.parse_args()
    
    if args.note:
        result = score_linkedin_note(args.note)
        print("\n--- FastBD LinkedIn Note Audit ---")
        print(f"Character Length:    {result['char_length']} / 300")
        print(f"Mobile Friendly:     {'Yes (Fits push snippet)' if result['is_mobile_friendly'] else 'No (Truncated)'}")
        print(f"Predicted LCR:       {result['predicted_lcr']}%")
        print(f"Rating Tier:         {result['tier']}")
        if result['detected_pitches']:
            print(f"Spam Buzzwords:      {', '.join(result['detected_pitches'])}")
    
    alps_score = calculate_alps(args.weekly_sent, args.spam_flags, args.pending_14d)
    print("\n--- Account Longevity Protection Score (ALPS) ---")
    print(f"ALPS Score:          {alps_score} / 100.0")
    print(f"Account Health:      {'Safe & Green' if alps_score >= 85 else ('Warning - Throttling Risk' if alps_score >= 70 else 'CRITICAL - Pause Outbound')}\n")

if __name__ == "__main__":
    main()
