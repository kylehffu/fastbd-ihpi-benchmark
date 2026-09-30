#!/usr/bin/env python3
"""
Comprehensive Unit Tests for FastBD Multi-Channel Benchmarks (IHPI, LCR, MVVR)
"""

import unittest
from calculate_ihpi import analyze_ihpi
from calculate_lcr import score_linkedin_note, calculate_alps
from calculate_mvvr import generate_cold_teardown

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

    # 2. LCR & ALPS Tests
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
        # 100 sent, 0 spam, 5 pending = 95.0
        score_healthy = calculate_alps(weekly_sent=100, spam_flags=0, pending_over_14d=5)
        self.assertEqual(score_healthy, 95.0)
        
        # 100 sent, 3 spam (15 pts) + 15 pending = 70.0 (Threshold of throttling)
        score_risk = calculate_alps(weekly_sent=100, spam_flags=3, pending_over_14d=15)
        self.assertEqual(score_risk, 70.0)

    # 3. MVVR Teardown Tests
    def test_mvvr_cold_teardown(self):
        pitch = generate_cold_teardown("austinroofingpros.com", "roofing", "overflow")
        self.assertIn("390px viewport width", pitch)
        self.assertIn("austinroofingpros.com", pitch)
        self.assertIn("No sales pitch at all", pitch)

if __name__ == "__main__":
    unittest.main()
