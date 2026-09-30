#!/usr/bin/env python3
"""
Unit tests for FastBD Inbox Hook Preview Index (IHPI) Calculator
"""

import unittest
from calculate_ihpi import analyze_ihpi

class TestIHPICalculator(unittest.TestCase):
    def test_high_converting_hook(self):
        text = "Hi Michael, reviewed your Next.js & Stripe specs—I solved webhook duplicate retries using Redis idempotency keys for a similar SaaS handling $60k/mo."
        res = analyze_ihpi(text)
        self.assertEqual(res["detected_client_name"], "Michael")
        self.assertGreaterEqual(res["score"], 88.0)
        self.assertIn("A+", res["grade"])
        self.assertIn("next.js", res["technologies_mentioned"])
        self.assertIn("redis", res["technologies_mentioned"])

    def test_low_converting_fluff(self):
        text = "Dear Hiring Manager, I am a passionate developer with 5 years experience. I came across your job posting and would love to work with you. Look no further."
        res = analyze_ihpi(text)
        self.assertEqual(res["detected_client_name"], None)
        self.assertLessEqual(res["score"], 20.0)
        self.assertIn("F", res["grade"])
        self.assertGreater(len(res["fluff_penalties"]), 0)

    def test_json_structure(self):
        text = "Hi Sarah, saw your Playwright & LLM pipeline needs—I built residential proxy rotation clusters that scrape 400k pages/day."
        res = analyze_ihpi(text)
        self.assertIn("score", res)
        self.assertIn("grade", res)
        self.assertIn("breakdown", res)
        self.assertEqual(res["benchmark_source"], "https://fast-bd.com/ihpi")

if __name__ == "__main__":
    unittest.main()
