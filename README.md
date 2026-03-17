# 🔒 LLM Security Gateway 🛡️
A Comprehensive Security Solution for Large Language Models  

Protecting LLMs from Prompt Injection, Jailbreak Attempts, and PII Leakage

---

## 👩‍💻 Author Information

| Field | Details |
|------|--------|
| Name | Iqra Mushtaq |
| Student ID | 01-134241-018 |
| Email | 01-134241-018@student.bahria.edu.pk |
| Instructor | Sir Arshad Farhad |
| Date | March 17, 2026 |
| Institution | Bahria University |

---

## 📋 Table of Contents

- Project Overview  
- Key Features  
- Architecture
- Data Flow  
- Requirements Matrix  
- Installation  
- Configuration  
- Test Results  
- Project Structure    
- License  
- Contact  

---

## 🎯 Project Overview

The **LLM Security Gateway** is a modular, production-ready security solution designed to protect Large Language Models from various security threats.

### 🔹 It acts as a middleware layer that:
- Intercepts user input  
- Detects threats  
- Applies policies  
- Returns safe responses  

---

## 🛡️ Protected Against

- 🔓 Prompt Injection Attacks  
- ⛓️ Jailbreak Attempts  
- 🔑 System Prompt Extraction  
- 📧 PII Leakage (Emails, Phones)  
- 🔐 API Key Exposure  
- 🆔 Internal ID Disclosure  

---

## ✨ Key Features

| Feature | Description | Implementation |
|--------|------------|----------------|
| 🔍 Multi-layer Detection | Injection + PII analysis | `core.py` |
| 🎯 Scoring System | Confidence scoring (0.0–1.0) | `injection.py` |
| 🧠 Custom PII Recognizers | 4+ recognizers | `custom.py` |
| 📊 Policy Engine | ALLOW / MASK / BLOCK | `decision.py` |
| ⚙️ Configurable Thresholds | YAML-based config | `config.yaml` |
| ⏱️ Performance Monitoring | Latency tracking | `core.py` |
| 🔄 Composite Detection | Multiple entity handling | `decision.py` |

---

## 🏗️ Architecture

User Input → Injection Detection → PII Analysis → Policy Decision → Output

---

## 🔄 Data Flow

1. Input enters gateway  
2. Injection detection runs  
3. PII analysis using Presidio  
4. Policy evaluation  
5. Action returned  

---

## ✅ Requirements Matrix

| # | Requirement | Status | Description |
|--|------------|--------|------------|
| 1 | Modular Code | ✅ | Structured modules |
| 2 | Injection Scoring | ✅ | Pattern-based scoring |
| 3 | Presidio Customization | ✅ | 4 recognizers |
| 4 | Context-Aware Detection | ✅ | Phone detection |
| 5 | Composite Detection | ✅ | Multiple PII |
| 6 | Confidence Calibration | ✅ | 0.6–0.95 |
| 7 | Configurable Thresholds | ✅ | YAML config |
| 8 | Policy Decisions | ✅ | ALLOW/MASK/BLOCK |
| 9 | Latency Measurement | ✅ | ms precision |
|10 | Attack Coverage | ✅ | 5+ attacks |

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip
- Git  

### Steps

```bash
git clone https://github.com/Iqra7672/llm-security-gateway.git
cd llm-security-gateway

python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/macOS)
source venv/bin/activate

pip install -r requirements.txt

python -m spacy download en_core_web_lg

python test_gateway.py


## 📦 Dependencies

presidio-analyzer==2.2.33
spacy==3.7.4
pyyaml==6.0.1

---

## ⚙️ Configuration

Edit config/config.yaml

injection:
  threshold: 0.5
  patterns:
    - "ignore instructions"
    - "jailbreak"
    - "system prompt"
    - "extraction"

policy:
  block_threshold: 0.7
  mask_threshold: 0.4

pii:
  entities:
    - "EMAIL_ADDRESS"
    - "PHONE_NUMBER"
    - "API_KEY"
    - "INTERNAL_ID"
  min_confidence: 0.6

---

## 📊 Test Results (from actual execution)

| Input Type                  | Injection Score | PII Found   | Decision   | Time (ms) |
|---------------------------|-----------------|-------------|------------|-----------|
| ✅ Normal query           | 0.00            | None        | 🟢 ALLOW   | 0.12      |
| ⚠️ "Ignore instructions" | 0.10            | None        | 🟢 ALLOW   | 0.20      |
| 📧 Email + Phone         | 0.00            | 2 entities  | 🟡 MASK    | 0.23      |
| 🔑 API Key               | 0.00            | 1 entity    | 🔴 BLOCK   | 0.52      |
| 🆔 Internal ID           | 0.00            | 1 entity    | 🟡 MASK    | 0.20      |
| 📞 Phone number          | 0.00            | 1 entity    | 🟡 MASK    | 0.16      |

---

## 📁 Project Structure


llm-security-gateway/
├── gateway/
│ ├── init.py
│ ├── core.py # Main gateway logic
│ ├── detectors/
│ │ ├── init.py
│ │ └── injection.py # Injection detection
│ ├── recognizers/
│ │ ├── init.py
│ │ └── custom.py # PII detection
│ └── policies/
│ ├── init.py
│ └── decision.py # Policy engine
├── config/
│ └── config.yaml # Configuration
├── tests/
│ └── init.py
├── test_gateway.py # Test script
├── requirements.txt
└── README.md


---

## 📄 License

© 2026 Iqra Mushtaq  
Bahria University  

---

## 📧 Contact

- Email: 01-134241-018@student.bahria.edu.pk  
- GitHub: https://github.com/Iqra7672  
- Institution: Bahria University, Islamabad  

  

