# LLM Security Gateway

## 👩‍💻 Author Information
- **Name:** Iqra Mushtaq
- **Student ID:** 01-134241-018
- **Email:** 01-134241-018@student.bahria.edu.pk
- **Instructor:** Sir Arshad Farhad
- **Date:** March 17, 2026

## 📋 Project Overview
A modular security gateway for Large Language Models (LLMs) that protects against:
- Prompt injection attacks
- Jailbreak attempts
- System prompt extraction
- PII leakage (emails, phones, API keys, internal IDs)

## 🏗️ Architecture
User Input → Injection Detection → PII Analysis → Policy Decision → Output


## ✅ Assignment Requirements Met

| Requirement | Status | Location |
|------------|--------|----------|
| 🔧 Modular code structure | ✅ Complete | `/gateway` folder |
| 🎯 Injection detection scoring | ✅ Complete | `detectors/injection.py` |
| 🔍 Presidio customizations (3+) | ✅ Complete (4) | `recognizers/custom.py` |
| 🧠 Context-aware scoring | ✅ Complete | Phone number detection |
| 🔗 Composite entity detection | ✅ Complete | Multiple PII handling |
| 📊 Confidence calibration | ✅ Complete | Scores 0.6-0.95 |
| ⚙️ Configurable thresholds | ✅ Complete | `config/config.yaml` |
| ⚖️ Policy decisions | ✅ Complete | `policies/decision.py` |
| ⏱️ Latency measurement | ✅ Complete | `core.py` |
| 🛡️ 5+ attack types | ✅ Complete | All covered |


## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/Iqra7672/llm-security-gateway.git
cd llm-security-gateway

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run the gateway
python test_gateway.py


## 📊 Test Results (from actual execution)

| Input Type | Injection Score | PII Found | Decision | Time (ms) |
|------------|-----------------|-----------|----------|-----------|
| ✅ Normal query | 0.00 | None | 🟢 ALLOW | 0.12 |
| ⚠️ "Ignore instructions" | 0.10 | None | 🟢 ALLOW | 0.20 |
| 📧 Email + Phone | 0.00 | 2 entities | 🟡 MASK | 0.23 |
| 🔑 API Key | 0.00 | 1 entity | 🔴 BLOCK | 0.52 |
| 🆔 Internal ID | 0.00 | 1 entity | 🟡 MASK | 0.20 |
| 📞 Phone number | 0.00 | 1 entity | 🟡 MASK | 0.16 |


📁 Project Structure
text
llm-security-gateway/
├── gateway/
│   ├── __init__.py
│   ├── core.py              # Main gateway logic
│   ├── detectors/
│   │   ├── __init__.py
│   │   └── injection.py     # Injection detection
│   ├── recognizers/
│   │   ├── __init__.py
│   │   └── custom.py        # PII detection
│   └── policies/
│       ├── __init__.py
│       └── decision.py      # Policy engine
├── config/
│   └── config.yaml          # Configuration
├── tests/
│   └── __init__.py
├── test_gateway.py          # Test script
├── requirements.txt
└── README.md

⚙️ Configuration
Edit config/config.yaml to adjust thresholds:

yaml
injection:
  threshold: 0.5
policy:
  block_threshold: 0.7
  mask_threshold: 0.4


🔗 GitHub Repository
https://github.com/Iqra7672/llm-security-gateway

📝 License
Academic Project - Bahria University

📧 Contact
For questions: 01-134241-018@student.bahria.edu.pk