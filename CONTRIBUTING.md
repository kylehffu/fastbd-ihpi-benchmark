# Contributing to FastBD IHPI Benchmark

Thank you for your interest in improving the **FastBD Inbox Hook Preview Index (IHPI)**!

We welcome contributions from freelancers, data analysts, and software engineers to expand the empirical proposal dataset and refine the hook conversion formula.

---

## How You Can Contribute

1. **Submit Anonymized Proposal Samples:**
   Add new proposal text samples to `sample_proposals.json` with the following schema:
   ```json
   {
     "id": "sample-06",
     "title": "Your Project Title",
     "category": "Mobile App / DevOps / Design",
     "proposal": "First 2-3 sentences of the proposal...",
     "expected_grade": "A+"
   }
   ```
2. **Refine Regex & Weights:**
   Help expand `TECH_KEYWORDS` or refine `PROOF_METRIC_PATTERNS` in `calculate_ihpi.py` for emerging languages and platforms.
3. **Report Edge Cases:**
   Submit an issue if a high-converting hook was incorrectly penalized or an invalid pattern bypassed fluff filters.

---

## Local Development & Testing

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/fastbd-ihpi-benchmark.git
   cd fastbd-ihpi-benchmark
   ```
2. Install in editable mode:
   ```bash
   pip install -e .
   ```
3. Run the unit tests:
   ```bash
   python3 -m unittest discover tests
   ```
4. Run the benchmark runner:
   ```bash
   python3 run_benchmark.py
   ```

---

## Code of Conduct & Standards

- All code, comments, and documentation must be written in **100% English**.
- Ensure all automated unit tests pass before opening a Pull Request.
- Follow the MIT License terms.
