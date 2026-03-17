🔐 LLM Security Gateway
<p align="center"> <b>A Modular Security Layer for Large Language Models (LLMs)</b><br> Protecting against prompt injection, jailbreaks, and sensitive data leakage </p>
👩‍💻 Author

Iqra Mushtaq

🎓 Student ID: 01-134241-018

📧 Email: 01-134241-018@student.bahria.edu.pk

👨‍🏫 Instructor: Sir Arshad Farhad

📅 Date: March 17, 2026

📋 Project Overview

This project implements a modular security gateway designed to protect Large Language Models (LLMs) from common security threats.

🔒 Key Protections

🚫 Prompt Injection Attacks

🔓 Jailbreak Attempts

🧾 System Prompt Extraction

🔍 PII Leakage Detection:

Emails

Phone Numbers

API Keys

Internal IDs

🏗️ System Architecture
User Input 
   ↓
Injection Detection 
   ↓
PII Analysis 
   ↓
Policy Decision 
   ↓
Secure Output
✨ Features

🔧 Modular and scalable architecture

🎯 Injection detection with scoring system

🔍 Custom PII recognizers (Presidio-based)

🧠 Context-aware detection logic

🔗 Composite entity detection

📊 Confidence scoring (0.6 – 0.95)

⚙️ Configurable thresholds

⚖️ Policy-based decision engine (ALLOW / MASK / BLOCK)

⏱️ Low latency processing

✅ Assignment Requirements
Requirement	Status	Implementation
Modular structure	✅	/gateway
Injection scoring	✅	detectors/injection.py
Presidio customization	✅ (4)	recognizers/custom.py
Context-aware scoring	✅	Phone detection
Composite detection	✅	Multi-PII
Confidence calibration	✅	0.6–0.95
Configurable thresholds	✅	config.yaml
Policy engine	✅	policies/decision.py
Latency measurement	✅	core.py
Attack coverage (5+)	✅	Implemented
🚀 Installation & Setup
# Clone repository
git clone https://github.com/Iqra7672/llm-security-gateway.git

# Move into project
cd llm-security-gateway

# Create virtual environment
python -m venv venv

# Activate environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the project
python test_gateway.py
📊 Test Results
Input	Injection Score	PII	Decision	Time (ms)
Normal query	0.00	None	🟢 ALLOW	0.12
"Ignore instructions"	0.10	None	🟢 ALLOW	0.20
Email + Phone	0.00	2 entities	🟡 MASK	0.23
API Key	0.00	1 entity	🔴 BLOCK	0.52
Internal ID	0.00	1 entity	🟡 MASK	0.20
Phone number	0.00	1 entity	🟡 MASK	0.16
📁 Project Structure
llm-security-gateway/
│
├── gateway/
│   ├── core.py              # Main gateway logic
│   ├── detectors/
│   │   └── injection.py     # Injection detection
│   ├── recognizers/
│   │   └── custom.py        # PII detection
│   └── policies/
│       └── decision.py      # Policy engine
│
├── config/
│   └── config.yaml          # Threshold configuration
│
├── tests/
├── test_gateway.py
├── requirements.txt
└── README.md
⚙️ Configuration

Modify thresholds in:

📄 config/config.yaml

injection:
  threshold: 0.5

policy:
  block_threshold: 0.7
  mask_threshold: 0.4
🔗 Repository

👉 GitHub:
https://github.com/Iqra7672/llm-security-gateway

📝 License

This project is developed for academic purposes at Bahria University.

📬 Contact

For questions or collaboration:

📧 01-134241-018@student.bahria.edu.pk
