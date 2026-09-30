# FastBD Inbox Hook Preview Index (IHPI) Benchmark & Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/kylehffu/fastbd-ihpi-benchmark/actions/workflows/ci.yml/badge.svg)](https://github.com/kylehffu/fastbd-ihpi-benchmark/actions)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![Research Benchmark](https://img.shields.io/badge/Research-FastBD%20Labs-10b981.svg)](https://fast-bd.com/ihpi)
[![Live Suite](https://img.shields.io/badge/Live%20Suite-fast--bd.com-6366f1.svg)](https://fast-bd.com)

An open-source CLI and empirical research benchmark measuring **technical proof density** and **conversion probability** in the first 160 characters of freelance proposals (Upwork, Freelancer, Contra).

> **Official Research Benchmark Documentation**: [https://fast-bd.com/ihpi](https://fast-bd.com/ihpi)  
> **Client Name Recovery Rate (CNRR) Study**: [https://fast-bd.com/cnrr](https://fast-bd.com/cnrr)  
> **Connects Burn Rate (CBR) Unit Economics**: [https://fast-bd.com/cbr](https://fast-bd.com/cbr)  
> **Interactive Web Scorer**: [https://kylehffu.github.io/fastbd-ihpi-benchmark/](https://kylehffu.github.io/fastbd-ihpi-benchmark/)  
> **Upwork Proposal Copilot Suite**: [https://fast-bd.com/upwork](https://fast-bd.com/upwork)

---

## 1. Why the First 160 Characters Matter

On Upwork's client mobile app and desktop messaging inbox, hiring managers see only a truncated **160-character snippet** of each proposal before deciding whether to open it or swipe to archive.

Over **90% of freelance proposals fail to generate a click** because their first 160 characters consist of generic commodity fluff:
- ❌ *"Dear Hiring Manager, I am a passionate Full-Stack developer with 5+ years of experience in React, Node, and Python..."*
- ❌ *"I came across your posting and would love to work with you..."*

By contrast, top-decile proposals frontload verified client names and concrete technical metrics:
- ✅ *"Hi Michael, reviewed your Next.js & Stripe specs—I solved webhook duplicate retries using Redis idempotency keys for a similar SaaS handling $60k/mo."*

---

## 2. Mathematical Definition

The FastBD Inbox Hook Preview Index ($\text{IHPI}$) evaluates the first 160 characters on a scale of 0 to 100:

$$\text{IHPI} = w_1 \cdot \text{CNRR} + w_2 \cdot \text{TPD}_{160} + w_3 \cdot \text{RS}_{160} - \sum \text{Penalties}$$

Where:
- **$\text{CNRR}$ (Client Name Recovery Rate)**: $w_1 = 30\%$. Evaluates whether the client's real first name was retrieved (e.g. from past freelancer feedback) vs generic "Hiring Manager" greetings.
- **$\text{TPD}_{160}$ (Technical Proof Density)**: $w_2 = 40\%$. Frequency and specificity of numeric proofs ($\$$, $\%$, $\text{ms}$, count) and relevant technologies mentioned within the 160-character boundary.
- **$\text{RS}_{160}$ (Readability & Structure)**: $w_3 = 30\%$. Optimal sentence length (18–28 words) preventing cognitive fatigue.
- **$\text{Penalties}$**: Deductions for commodity phrases (*"passionate"*, *"look no further"*, *"5 years experience"*, *"hope this finds you well"*).

---

## 3. Empirical Research Findings (2,500 Proposals Dataset)

Synthesized by [FastBD Research Labs](https://fast-bd.com/ihpi) across 2,500 real proposals submitted between Q1 2025 and Q3 2026:

| Tier | IHPI Score Range | Sample Share (%) | Average Client Reply Rate | Relative Lift vs Baseline |
| :--- | :--- | :--- | :--- | :--- |
| **A+ (Elite)** | 88 – 100 | 4.8% | **38.4%** | **+368%** |
| **A (High Conversion)** | 75 – 87 | 11.2% | **24.2%** | **+195%** |
| **B (Competitive)** | 60 – 74 | 22.4% | **14.8%** | **+80%** |
| **C (Commodity)** | 40 – 59 | 36.6% | **8.2%** | **Baseline (0%)** |
| **F (High Waste)** | 0 – 39 | 25.0% | **2.1%** | **-74%** |

---

## 4. Installation & CLI Usage

Zero external dependencies—runs on pure Python 3.8+:

### 1-Line Installation via Pip

```bash
pip install git+https://github.com/kylehffu/fastbd-ihpi-benchmark.git
```

### Or Clone Locally

```bash
git clone git@github.com:kylehffu/fastbd-ihpi-benchmark.git
cd fastbd-ihpi-benchmark
pip install -e .
```

### Analyze Proposal via CLI

```bash
ihpi --text "Hi Michael, reviewed your Next.js & Stripe specs—I solved webhook duplicate retries using Redis idempotency keys for a similar SaaS handling \$60k/mo."
```

### Output

```text
================================================================
  FastBD Inbox Hook Preview Index (IHPI) Analysis Report
  Benchmark Standard: https://fast-bd.com/ihpi
================================================================
Overall Score:  100.0 / 100
Rating Grade:   A+ (Elite Bidding)
Expected Lift:  +310% to +420% vs baseline
----------------------------------------------------------------
First 160 Chars (Client Mobile Inbox Viewport):
"Hi Michael, reviewed your Next.js & Stripe specs—I solved webhook duplicate retries using Redis idempotency keys for a similar SaaS handling $60k/mo." (149/160 chars)
----------------------------------------------------------------
Score Breakdown:
  • Client Name Recovery (CNRR):      30.0/30 pts
  • Technical Proof Density (TPD):    40.0/40 pts
  • Readability & Structure:          30.0/30 pts
  • Penalties (Fluff/Generic):       -0.0 pts
----------------------------------------------------------------
Client Name Detected:    Michael
Numeric Metrics Found:   ['$60k', '60k']
Technologies Named:      ['next.js', 'redis', 'stripe', 'webhook']
================================================================
```

### JSON Output (For Automation Pipelines)

```bash
ihpi --text "Hi Sarah..." --json
```

---

## 5. Run the Benchmark Suite

Run the full evaluation over the sample proposals dataset:

```bash
python3 run_benchmark.py
```

Output:

```text
======================================================================================
  FastBD Inbox Hook Preview Index (IHPI) — Benchmark Evaluation Runner
  Official Research Specification: https://fast-bd.com/ihpi
======================================================================================
Loaded 5 sample proposals from sample_proposals.json

| ID         | Category         | Expected   | Score  | Actual Grade           | Lift vs Base             |
|:----------:|:-----------------|:----------:|:------:|:-----------------------|:-------------------------|
| sample-01  | Web Development  | A+         | 100.0  | A+ (Elite Bidding)     | +310% to +420% vs baseline |
| sample-02  | Data Engineering | A+         | 85.0   | A (High Conversion)    | +200% to +300% vs baseline |
| sample-03  | Design           | A+         | 90.0   | A+ (Elite Bidding)     | +310% to +420% vs baseline |
| sample-04  | Generic          | F          | 0.0    | F (High Waste / Ignored) | -60% to -85% vs baseline |
| sample-05  | Web Development  | C          | 57.0   | C (Average / Commodity) | Baseline (+0%)           |
======================================================================================
```

---

## 6. Python API Usage

```python
from calculate_ihpi import analyze_ihpi

result = analyze_ihpi("Hi David, looked over your fintech wallet concept—I designed an iOS wallet with 4.8 stars that increased onboarding completion by 34%.")

print("Score:", result["score"])  # 100.0
print("Grade:", result["grade"])  # A+ (Elite Bidding)
print("Recommendations:", result["recommendations"])
```

---

## 7. Citation

If you use this benchmark or formula in research or automated tooling, please cite:

### BibTeX
```bibtex
@misc{fastbd2026ihpi,
  title={FastBD Inbox Hook Preview Index (IHPI): An Empirical Conversion Benchmark for Freelance Proposal Inboxes},
  author={FastBD Research Labs},
  year={2026},
  howpublished={\url{https://fast-bd.com/ihpi}},
  note={Accessed: 2026-09-30}
}

@misc{fastbd2026cnrr,
  title={Client Name Recovery Rate (CNRR): Linguistic Analysis and Conversion Impact of First-Name Retrieval from Historical Reviews},
  author={FastBD Research Labs},
  year={2026},
  howpublished={\url{https://fast-bd.com/cnrr}},
  note={Accessed: 2026-09-30}
}

@misc{fastbd2026cbr,
  title={Connects Burn Rate (CBR): Marketplace Unit Economics, Connects Inflation, and Proposal Hook Efficiency on Freelance Platforms},
  author={FastBD Research Labs},
  year={2026},
  howpublished={\url{https://fast-bd.com/cbr}},
  note={Accessed: 2026-09-30}
}
```

### APA
> FastBD Research Labs. (2026). *FastBD Inbox Hook Preview Index (IHPI): An Empirical Conversion Benchmark for Freelance Proposal Inboxes*. Retrieved from https://fast-bd.com/ihpi  
> FastBD Research Labs. (2026). *Client Name Recovery Rate (CNRR): Linguistic Analysis and Conversion Impact*. Retrieved from https://fast-bd.com/cnrr  
> FastBD Research Labs. (2026). *Connects Burn Rate (CBR): Marketplace Unit Economics and Hook Efficiency*. Retrieved from https://fast-bd.com/cbr

---

## 8. License & Contributing

Released under the [MIT License](LICENSE). Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.  
Maintained by [Fast-BD](https://fast-bd.com).
