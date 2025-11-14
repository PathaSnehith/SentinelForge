# SentinelForge - Complete Project Explanation (For Beginners)

## 🎯 What is SentinelForge?

**SentinelForge** is a **Security Operations Center (SOC) Simulator** - think of it as a cybersecurity monitoring system that watches for suspicious activities and attacks, just like security cameras watch for intruders.

### Real-World Analogy:
Imagine you're a security guard at a building:
- You watch who enters/exits (login attempts)
- You notice if someone tries the door 10 times (brute-force attack)
- You see if someone downloads huge files (data theft)
- You alert when something suspicious happens

**SentinelForge does this automatically for computer systems!**

---

## 🔍 What Problem Does It Solve?

In real companies, security teams need to:
1. **Monitor** thousands of user activities every day
2. **Detect** attacks like hackers trying to break in
3. **Alert** security staff when something bad happens
4. **Analyze** patterns to catch sophisticated attacks

**SentinelForge simulates this entire process** so you can:
- Learn how SOC (Security Operations Center) works
- Test detection rules on large datasets
- Demonstrate cybersecurity concepts
- Train on real-world attack scenarios

---

## 🏗️ How Does It Work? (Simple Explanation)

Think of SentinelForge as a **3-step pipeline**:

```
📥 INPUT (Logs)  →  🔍 ANALYSIS (Detection)  →  📊 OUTPUT (Alerts)
```

### Step 1: INPUT - Logs Come In
- Users log in, download files, change settings
- Each action creates a "log entry" (like a diary entry)
- Example log: "Alice tried to login at 10:00 AM from IP 192.168.1.100 - FAILED"

### Step 2: ANALYSIS - Detection Engine Checks
- The system looks for suspicious patterns:
  - ❌ 5 failed logins in 5 minutes? → **BRUTE_FORCE attack!**
  - ❌ User logged in from India, then USA 30 minutes later? → **IMPOSSIBLE_TRAVEL!**
  - ❌ Someone downloaded 500 MB of sensitive data? → **DATA_EXFILTRATION!**

### Step 3: OUTPUT - Alerts Generated
- When something suspicious is found, an **ALERT** is created
- Alerts show: What happened? Who did it? How serious is it?

---

## 📁 Project Structure (What Each File Does)

### **Backend (The Brain)**
- `app/main.py` - The main server that receives requests
- `app/detections.py` - The "detective" that finds attacks (7 different detection rules)
- `app/database.py` - Stores all logs and alerts in a database
- `app/models.py` - Defines what a "log" and "alert" look like
- `app/services.py` - Helper functions that process data

### **Frontend (The Display)**
- `static/index.html` - The web page you see
- `static/app.js` - Makes the page interactive (refreshes data, shows alerts)
- `static/styles.css` - Makes it look nice (dark theme, colors)

### **Data (Training Material)**
- `data/dataset_1_brute_force.json` - 1,256 log entries showing brute-force attacks
- `data/dataset_2_data_theft.json` - 2,117 entries showing data theft
- `data/dataset_3_privilege_abuse.json` - 2,012 entries showing privilege abuse
- `data/dataset_4_comprehensive.json` - 2,618 entries with mixed attacks
- `data/dataset_5_massive_training.json` - 5,120 entries (the big one!)
- `data/sample_logs.json` - 13 entries for quick testing

### **Tools**
- `analyze_logs.py` - Command-line tool to analyze datasets
- `generate_large_datasets.py` - Script that creates the training datasets
- `requirements.txt` - List of Python packages needed

---

## 🛡️ The 7 Detection Rules (What Attacks It Catches)

### 1. **BRUTE_FORCE** (HIGH Severity)
- **What it detects:** Someone trying to guess passwords
- **How:** If 5+ failed logins happen in 5 minutes from same IP
- **Example:** "Hacker tries password123, password456, etc. 10 times"

### 2. **IMPOSSIBLE_TRAVEL** (MEDIUM Severity)
- **What it detects:** User logging in from two distant places too quickly
- **How:** If user logs in from Location A, then Location B within 1 hour (impossible!)
- **Example:** "User logged in from India at 10:00 AM, then USA at 10:30 AM"

### 3. **DATA_EXFIL** (HIGH Severity)
- **What it detects:** Someone stealing large amounts of data
- **How:** If download is >200 MB (suspiciously large)
- **Example:** "User downloaded 2 GB of customer database"

### 4. **ADMIN_AFTER_HOURS** (MEDIUM Severity)
- **What it detects:** Admins logging in at weird times (could be compromised)
- **How:** If admin logs in between 10 PM - 6 AM
- **Example:** "Admin logged in at 2:00 AM (suspicious!)"

### 5. **SENSITIVE_RESOURCE_ANOM** (MEDIUM Severity)
- **What it detects:** Sensitive files downloaded from untrusted devices
- **How:** If finance/payroll files downloaded from non-VDI devices
- **Example:** "User downloaded payroll.xlsx from personal laptop"

### 6. **UNAUTHORIZED_PRIV_ACTION** (CRITICAL Severity)
- **What it detects:** Regular users trying to do admin tasks
- **How:** If non-admin executes `config_change` or `privilege_escalation`
- **Example:** "Regular user tried to change firewall settings"

### 7. **LOW_SUCCESS_RATE** (MEDIUM Severity)
- **What it detects:** Device with too many failed logins
- **How:** If device has 5+ login attempts with <20% success rate
- **Example:** "Device had 10 login attempts, only 1 succeeded"

---

## 🚀 How to Use It (Step by Step)

### **Method 1: Web Dashboard (Visual)**

1. **Start the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Open browser:**
   - Go to: `http://localhost:8000/`
   - You'll see a dark dashboard

3. **Load data:**
   - Select a dataset from dropdown (e.g., "Dataset 5 Massive Training")
   - Click "Ingest Selected Dataset"
   - Watch alerts appear!

4. **View results:**
   - See alert count at top
   - Scroll through alerts table
   - See recent logs table

### **Method 2: Command Line (Fast)**

```bash
# Analyze a dataset
python analyze_logs.py --file data/dataset_5_massive_training.json
```

**Output shows:**
```
Ingested 5120 events. Generated 450 alerts.
[HIGH] BRUTE_FORCE - Five+ failed logins for alice...
[MEDIUM] IMPOSSIBLE_TRAVEL - User bob logged in from...
[HIGH] DATA_EXFIL - diana downloaded 700.0 MB...
```

---

## 📊 Example Scenario Walkthrough

### Scenario: Brute-Force Attack

1. **Attack happens:**
   - Hacker tries to login as "alice" 10 times
   - All attempts fail
   - Happens within 5 minutes

2. **System detects:**
   - Detection engine sees: 10 failed logins in 5 minutes
   - Rule triggers: **BRUTE_FORCE**
   - Severity: **HIGH**

3. **Alert created:**
   ```
   [HIGH] BRUTE_FORCE - Five+ failed logins for alice 
   from 192.168.1.100 within 5 minutes.
   ```

4. **Security team sees:**
   - Alert appears on dashboard
   - They can investigate and block the IP

---

## 🎓 Why This Project is Impressive

### **1. Real-World Application**
- Simulates actual SOC (Security Operations Center) systems
- Uses industry-standard detection techniques
- Handles large-scale data (13,000+ entries)

### **2. Technical Skills Demonstrated**
- **Backend:** FastAPI (modern Python web framework)
- **Database:** SQLite (data persistence)
- **Frontend:** HTML/CSS/JavaScript (web dashboard)
- **Data Processing:** Complex pattern matching algorithms

### **3. Cybersecurity Knowledge**
- Understands attack vectors (brute-force, data exfiltration)
- Implements detection rules based on security best practices
- Demonstrates threat analysis capabilities

### **4. Scalability**
- Processes thousands of log entries
- Real-time detection
- Extensible architecture (easy to add new rules)

---

## 💡 Key Concepts to Understand

### **SOC (Security Operations Center)**
- A team/room that monitors security 24/7
- Like a security control room for computers
- SentinelForge simulates this

### **Log Entry**
- A record of something that happened
- Contains: timestamp, user, action, IP address, etc.
- Example: "User 'alice' logged in at 10:00 AM from IP 192.168.1.100"

### **Alert**
- A warning that something suspicious happened
- Contains: severity, description, who/what/where
- Example: "HIGH severity: Brute-force attack detected"

### **Detection Rule**
- A pattern to look for
- Like a "if-then" statement
- Example: "IF 5 failed logins in 5 minutes THEN alert"

---

## 🎤 Presentation Tips

### **What to Say:**

1. **Introduction:**
   "SentinelForge is a Security Operations Center simulator that automatically detects cyber attacks by analyzing user activity logs."

2. **Problem:**
   "Companies need to monitor thousands of activities daily to catch hackers. This is time-consuming and requires automation."

3. **Solution:**
   "Our system uses 7 detection rules to automatically identify attacks like brute-force attempts, data theft, and privilege abuse."

4. **Demo:**
   - Show the dashboard
   - Load a dataset
   - Point out the alerts
   - Explain what each alert means

5. **Technical Highlights:**
   - "Processes 13,000+ log entries"
   - "Real-time detection with FastAPI backend"
   - "Web dashboard for visualization"
   - "Extensible detection engine"

---

## 🔧 Technical Stack (For Faculty Questions)

- **Language:** Python 3.11
- **Backend Framework:** FastAPI
- **Database:** SQLite (via SQLModel)
- **Frontend:** Vanilla JavaScript, HTML5, CSS3
- **Data Format:** JSON
- **Architecture:** RESTful API + Web Dashboard

---

## 📈 Project Statistics

- **Total Code:** ~1,200 lines
- **Training Data:** 13,123 log entries
- **Detection Rules:** 7 different attack types
- **Datasets:** 5 large-scale + 1 demo
- **Files:** 21 project files

---

## 🎯 Summary (One Sentence)

**SentinelForge is a cybersecurity monitoring system that automatically detects attacks by analyzing user activity logs using pattern-matching detection rules, with a web dashboard for visualization and support for processing thousands of log entries.**

---

## ❓ Common Questions & Answers

**Q: Is this real security data?**
A: No, all data is synthetically generated using our custom Python script for training purposes.

**Q: Can it detect real attacks?**
A: Yes! The detection rules are based on real-world security practices and can detect actual attack patterns.

**Q: How accurate is it?**
A: The rules are deterministic - they catch exactly what they're designed to catch. In production, you'd add machine learning for better accuracy.

**Q: What makes this different from other projects?**
A: It's a complete end-to-end system: data ingestion → detection → visualization, with large-scale training datasets.

**Q: Can you add more detection rules?**
A: Yes! Just add a new function in `app/detections.py` and register it in the `DETECTORS` list.

---

**Remember:** You built a complete SOC simulator that processes 13,000+ log entries and detects 7 different attack types. That's impressive! 🚀

