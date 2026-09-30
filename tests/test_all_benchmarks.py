#!/usr/bin/env python3
"""
Comprehensive Unit Tests for FastBD Multi-Channel Benchmarks (IHPI, CNRR, CBR, LCR, MVVR)
"""

import unittest
from calculate_ihpi import analyze_ihpi
from calculate_lcr import score_linkedin_note, calculate_alps
from calculate_mvvr import generate_cold_teardown
from calculate_cnrr import extract_client_name, calculate_cnrr, generate_salutation_hook
from calculate_cbr import calculate_cbr, calculate_annual_savings


class TestFastBDBenchmarks(unittest.TestCase):
    # 1. IHPI Tests
    def test_ihpi_elite(self):
        text = "Hi Michael, reviewed your Next.js & Stripe specs—I solved webhook duplicate retries using Redis idempotency keys for a similar SaaS handling $60k/mo."
        res = analyze_ihpi(text)
        self.assertGreaterEqual(res["score"], 88.0)
        self.assertIn("A+", res["grade"])

    def test_ihpi_fluff(self):
        text = "Dear Hiring Manager, I am a passionate developer with 5 years experience. Look no further."
        res = analyze_ihpi(text)
        self.assertLessEqual(res["score"], 20.0)
        self.assertIn("F", res["grade"])

    # 2. CNRR Tests
    def test_cnrr_extraction_gratitude(self):
        reviews = ["Thanks Michael for the prompt communication and clear specs!"]
        name, pattern = extract_client_name(reviews)
        self.assertEqual(name, "Michael")
        self.assertIn("Pattern 1", pattern)

    def test_cnrr_extraction_relational(self):
        reviews = ["Working with Sarah was an absolute pleasure from day one."]
        name, pattern = extract_client_name(reviews)
        self.assertEqual(name, "Sarah")
        self.assertIn("Pattern 2", pattern)

    def test_cnrr_dataset_rate(self):
        dataset = [
            ["Thanks Michael for the great job."],
            ["Working with David was awesome."],
            ["Great client."],
            ["All the best to Elena."]
        ]
        rate = calculate_cnrr(dataset)
        self.assertEqual(rate, 75.0)

    # 3. CBR Tests
    def test_cbr_elite_tier(self):
        cbr, cac, tier = calculate_cbr(total_connects=62, contracts_won=1)
        self.assertEqual(cbr, 62.0)
        self.assertEqual(cac, 9.30)
        self.assertIn("Elite", tier)

    def test_cbr_commodity_tier(self):
        cbr, cac, tier = calculate_cbr(total_connects=340, contracts_won=1)
        self.assertEqual(cbr, 340.0)
        self.assertEqual(cac, 51.00)
        self.assertIn("Commodity", tier)

    def test_cbr_savings_model(self):
        savings = calculate_annual_savings(monthly_proposals=50, connects_per_proposal=16, baseline_win_rate=0.05, optimized_win_rate=0.25)
        self.assertGreater(savings["annual_usd_saved"], 1000.0)
        self.assertGreater(savings["cost_reduction_percent"], 75.0)

    # 4. LCR & ALPS Tests
    def test_lcr_observation_hook(self):
        note = "Hi Sarah, loved your post on webhook idempotency! Rebuilt a Stripe pipeline solving that. Would love to connect."
        res = score_linkedin_note(note)
        self.assertTrue(res["is_mobile_friendly"])
        self.assertEqual(res["predicted_lcr"], 43.7)
        self.assertIn("Elite", res["tier"])

    def test_lcr_pitch_penalty(self):
        note = "Hi Sarah, I would love to hop on a quick call and demo our services to scale your business!"
        res = score_linkedin_note(note)
        self.assertGreater(len(res["detected_pitches"]), 0)
        self.assertLess(res["predicted_lcr"], 20.0)

    def test_alps_formula(self):
        score_healthy = calculate_alps(weekly_sent=100, spam_flags=0, pending_over_14d=5)
        self.assertEqual(score_healthy, 95.0)
        
        score_risk = calculate_alps(weekly_sent=100, spam_flags=3, pending_over_14d=15)
        self.assertEqual(score_risk, 70.0)

    # 5. MVVR Teardown Tests
    def test_mvvr_cold_teardown(self):
        pitch = generate_cold_teardown("austinroofingpros.com", "roofing", "overflow")
        self.assertIn("390px viewport width", pitch)
        self.assertIn("austinroofingpros.com", pitch)
        self.assertIn("No sales pitch at all", pitch)


if __name__ == "__main__":
    unittest.main()
