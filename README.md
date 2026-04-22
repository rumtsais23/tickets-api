# 🔐 AI Security Fusion Engine

An AI-powered security system that detects, analyzes, and classifies malicious inputs targeting LLMs and APIs.

## 🚀 Overview

This project combines:
- LLM-based analysis (OpenAI API)
- Prompt injection detection
- STRIDE threat modeling
- Risk scoring fusion engine

The goal is to evaluate user inputs and determine potential security risks in AI-driven systems.

---

## 🧠 Architecture

Input → Security Engine → Threat Model Engine → Fusion Engine → Final Verdict

---

## 🔍 Features

### AI Layer
- Text and code analysis using OpenAI GPT models

### Security Engine
- Detects prompt injection attacks
- Identifies malicious patterns (jailbreak attempts, system override)

### Threat Modeling (STRIDE)
- Spoofing detection
- Information disclosure risk
- Tampering detection
- Privilege escalation signals
- Denial of Service heuristics

### Fusion Engine
- Weighted risk scoring system
- Combines multiple security signals
- Produces final classification:
  LOW / MEDIUM / HIGH / CRITICAL
  + ALLOW / BLOCK decision

---

## ⚙️ Tech Stack

- Python
- Flask
- OpenAI API
- Rule-based security engine
- STRIDE methodology

---

## 📡 API Endpoints

### POST /analyze
Unified analysis endpoint (text / code / security)

### POST /security-scan
Prompt injection detection

### POST /threat-model
STRIDE-based threat analysis

### POST /ai-analyze
Final fused security verdict

---

## 💡 What I Learned

- LLM security risks and prompt injection attacks
- Threat modeling for AI systems
- Designing modular backend architectures
- Building fusion decision engines from multiple signals

---

## 🚀 Future Improvements

- Add vector DB memory layer
- Real-time API firewall mode
- JWT + authentication layer
- Docker deployment
