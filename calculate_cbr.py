#!/usr/bin/env python3
"""
FastBD Connects Burn Rate (CBR) & CAC Economics Calculator
==========================================================
Empirical benchmark modeling proposal unit economics on freelance platforms
like Upwork where bids incur connect fees ($0.15/connect).

Formula:
  CBR = Total Connects Spent / Contracts Won
  CAC = CBR * $0.15

Dataset: 2,500 proposals analyzed.
  - Commodity Tier: 340 connects / win ($51.00 CAC)
  - Elite IHPI Tier: 62 connects / win ($9.30 CAC) -> 81.8% Cost Savings

License: MIT
Repository: https://github.com/kylehffu/fastbd-ihpi-benchmark
Documentation: https://fast-bd.com/cbr
"""

import argparse
import sys

COST_PER_CONNECT = 0.15


def calculate_cbr(total_connects: int, contracts_won: int) -> tuple[float, float, str]:
    """
    Computes CBR, CAC, and proposal efficiency tier.
    """
    if contracts_won <= 0:
        return float("inf"), float("inf"), "Unprofitable"

    cbr = total_connects / contracts_won
    cac = cbr * COST_PER_CONNECT

    if cbr <= 80:
        tier = "Elite Conversion (IHPI 88-100)"
    elif cbr <= 140:
        tier = "High-Signal (IHPI 70-87)"
    elif cbr <= 220:
        tier = "Standard Qualified (IHPI 40-69)"
    else:
        tier = "Commodity Fluff (IHPI < 40)"

    return round(cbr, 1), round(cac, 2), tier


def calculate_annual_savings(
    monthly_proposals: int = 50,
    connects_per_proposal: int = 16,
    baseline_win_rate: float = 0.05,
    optimized_win_rate: float = 0.25,
) -> dict:
    """
    Calculates annual connects and USD saved by switching to high-signal proposal hooks.
    """
    baseline_cbr = round(connects_per_proposal / baseline_win_rate)
    baseline_cac = baseline_cbr * COST_PER_CONNECT

    opt_cbr = round(connects_per_proposal / optimized_win_rate)
    opt_cac = opt_cbr * COST_PER_CONNECT

    monthly_wins = max(1, round(monthly_proposals * baseline_win_rate))
    baseline_monthly_connects = monthly_proposals * connects_per_proposal
    optimized_monthly_connects = monthly_wins * opt_cbr
    monthly_connects_saved = max(0, baseline_monthly_connects - optimized_monthly_connects)
    annual_usd_saved = (monthly_connects_saved * COST_PER_CONNECT) * 12

    return {
        "baseline_cbr": baseline_cbr,
        "baseline_cac": baseline_cac,
        "optimized_cbr": opt_cbr,
        "optimized_cac": opt_cac,
        "annual_connects_saved": monthly_connects_saved * 12,
        "annual_usd_saved": round(annual_usd_saved, 2),
        "cost_reduction_percent": round((1 - opt_cac / baseline_cac) * 100, 1) if baseline_cac > 0 else 0.0,
    }


def main():
    parser = argparse.ArgumentParser(description="FastBD Connects Burn Rate (CBR) CLI")
    parser.add_argument("--proposals", "-p", type=int, default=50, help="Monthly proposals submitted")
    parser.add_argument("--connects-per-bid", "-c", type=int, default=16, help="Average connects spent per proposal")
    parser.add_argument("--baseline-rate", "-b", type=float, default=5.0, help="Current baseline win/reply rate (percent)")
    parser.add_argument("--target-rate", "-t", type=float, default=25.0, help="Target FastBD IHPI win/reply rate (percent)")
    args = parser.parse_args()

    results = calculate_annual_savings(
        monthly_proposals=args.proposals,
        connects_per_proposal=args.connects_per_bid,
        baseline_win_rate=args.baseline_rate / 100.0,
        optimized_win_rate=args.target_rate / 100.0,
    )

    print("\n" + "=" * 65)
    print(" FastBD Connects Burn Rate (CBR) Unit Economics Analysis")
    print("=" * 65)
    print(f" Monthly Proposals:       {args.proposals} applications / mo")
    print(f" Connects per Bid:        {args.connects_per_bid} connects (${args.connects_per_bid * COST_PER_CONNECT:.2f})")
    print("-" * 65)
    print(f" Baseline CAC:            \033[1;31m${results['baseline_cac']:.2f}\033[0m ({results['baseline_cbr']} connects/win)")
    print(f" FastBD Optimized CAC:    \033[1;32m${results['optimized_cac']:.2f}\033[0m ({results['optimized_cbr']} connects/win)")
    print(f" Cost Reduction:          \033[1;32m-{results['cost_reduction_percent']}%\033[0m CAC savings")
    print("-" * 65)
    print(f" Projected Annual Saved:  \033[1;32m${results['annual_usd_saved']:,.2f} USD\033[0m / year")
    print(f" Connects Saved:          {results['annual_connects_saved']:,} connects / year")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()
