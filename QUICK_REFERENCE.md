# SentinelForge - Quick Reference Cheat Sheet

## 🎯 What is it?
**SOC Simulator** - Automatically detects cyber attacks by analyzing logs

## 🔄 How it works (3 steps)
```
LOGS → DETECTION ENGINE → ALERTS
```

## 🛡️ 7 Detection Rules

| Rule | Severity | What It Catches |
|------|----------|----------------|
| **BRUTE_FORCE** | HIGH | 5+ failed logins in 5 min |
| **IMPOSSIBLE_TRAVEL** | MEDIUM | Login from 2 places in <1 hour |
| **DATA_EXFIL** | HIGH | Download >200 MB |
| **ADMIN_AFTER_HOURS** | MEDIUM | Admin login 10 PM - 6 AM |
| **SENSITIVE_RESOURCE_ANOM** | MEDIUM | Sensitive file from untrusted device |
| **UNAUTHORIZED_PRIV_ACTION** | CRITICAL | Non-admin doing admin tasks |
| **LOW_SUCCESS_RATE** | MEDIUM | Device with <20% login success |

## 📊 Project Stats
- **13,123 log entries** across 5 datasets
- **7 detection rules**
- **Web dashboard** + **CLI tool**
- **FastAPI backend** + **SQLite database**

## 🚀 Quick Start

### Start Server:
```bash
uvicorn app.main:app --reload
```

### Open Dashboard:
```
http://localhost:8000/
```

### Analyze Dataset:
```bash
python analyze_logs.py --file data/dataset_5_massive_training.json
```

## 📁 Key Files

- `app/main.py` - Server/API
- `app/detections.py` - Attack detection logic
- `static/index.html` - Web dashboard
- `data/*.json` - Training datasets
- `analyze_logs.py` - CLI analyzer

## 💬 Elevator Pitch (30 seconds)

"SentinelForge is a Security Operations Center simulator that automatically detects cyber attacks. It processes 13,000+ log entries using 7 detection rules to identify threats like brute-force attacks, data theft, and privilege abuse. It includes a web dashboard for visualization and can handle real-time monitoring scenarios."

## 🎤 Demo Flow

1. Open dashboard (`http://localhost:8000/`)
2. Select "Dataset 5 Massive Training" (5,120 entries)
3. Click "Ingest Selected Dataset"
4. Show alerts appearing in real-time
5. Explain what each alert type means

## 🔑 Key Terms

- **SOC** = Security Operations Center (security monitoring team)
- **Log Entry** = Record of user action (login, download, etc.)
- **Alert** = Warning when attack detected
- **Detection Rule** = Pattern to look for suspicious activity

## 📈 Impressive Points

✅ Processes 13,000+ log entries  
✅ Real-time detection  
✅ 7 different attack types  
✅ Web dashboard visualization  
✅ Extensible architecture  
✅ Industry-standard techniques  

