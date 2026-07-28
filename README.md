# 🤖 Log Analyzer and Root Cause Analysis (RCA) using AI

An intelligent AI-powered Log Analyzer built for **Contact Center environments** that automates log investigation, identifies incidents, performs **Root Cause Analysis (RCA)**, and generates human-readable AI summaries.

Instead of manually searching through thousands of log entries, simply upload a **.log**, **.csv**, or **.txt** file and let the application analyze it within seconds.

The project combines traditional log analysis with Large Language Models to help support engineers identify problems faster and reduce troubleshooting time.

---

## 🚀 Features

- 📂 Upload **Log (.log)**, **CSV (.csv)** and **Text (.txt)** files
- ⚡ Automatic log parsing and validation
- 🔍 Detect Errors, Warnings and Critical Events
- 🧠 AI-powered Root Cause Analysis (RCA)
- 🚨 Intelligent Incident Detection
- 📊 Severity Classification
- 🤖 AI-generated Investigation Summary
- 💾 Stores analysis history using SQLite
- 📑 Interactive Swagger API Documentation
- ⚙️ Handles large log files efficiently (100K+ Records)

---

## 🛠 Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn

### Database
- SQLite
- SQLAlchemy

### AI
- Groq API
- Llama 3.3 70B Versatile

### Data Processing
- Pandas
- Regular Expressions (Regex)
- CSV Processing

### Utilities
- Python Logging
- python-dotenv
- REST APIs
- Git & GitHub

---

# 📂 Project Structure

```
LogAnalyzer-RCA-AI
│
├── backend
│   ├── app
│   │   ├── api
│   │   ├── models
│   │   ├── services
│   │   ├── uploads
│   │   ├── utils
│   │   └── main.py
│   │
│   ├── requirements.txt
│   ├── .env
│   └── log_analyzer.db
│
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/AkshunMehrotra/log-Analyzer-and-RCA-using-AI.git
```

Move into the project

```bash
cd log-Analyzer-and-RCA-using-AI
```

Move into backend

```bash
cd backend
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file inside backend

```
GROQ_API_KEY=YOUR_API_KEY
```

Run the server

```bash
uvicorn app.main:app --reload
```

Backend

```
http://localhost:8000
```

Swagger Documentation

```
http://localhost:8000/docs
```

---

# 🔄 How It Works

```text
Upload File
      │
      ▼
Validate File
      │
      ▼
Parse Log Entries
      │
      ▼
Extract Errors & Warnings
      │
      ▼
Generate Root Cause Analysis
      │
      ▼
Detect Incidents
      │
      ▼
Generate AI Summary
      │
      ▼
Save Analysis
      │
      ▼
Display Final Report
```

---

# 📡 API Endpoints

## Upload File

```
POST /upload
```

Supported Files

- .log
- .csv
- .txt

---

## Analyze Uploaded File

```
GET /api/analyze/analyze
```

Returns

- AI Summary
- Root Cause Analysis
- Incident Report
- Severity
- Error Statistics

---

# 📊 Sample Response

```json
{
    "success": true,
    "message": "Log Analysis Completed",
    "statistics": {
        "total_logs": 100000,
        "errors": 215,
        "warnings": 48,
        "severity": "HIGH"
    },
    "overall_status": "Needs Investigation"
}
```

---

# 💡 Why This Project?

Support engineers often spend hours manually reviewing huge log files to locate failures.

This project reduces that effort by automatically extracting important events, identifying possible root causes, detecting incidents, and generating AI-powered explanations that are easy to understand.

The result is **faster debugging, quicker RCA generation, and improved operational efficiency**.

---

# 🚀 Future Improvements

- 📈 Interactive Dashboard
- 📄 PDF Report Export
- ☁ Cloud Deployment
- 🐳 Docker Support
- 🔐 Authentication
- 📬 Email Notifications
- 📊 Analytics Dashboard
- 📡 Real-time Log Monitoring
- 🔍 Elasticsearch Integration
- 📈 Grafana Visualization

---

# 👨‍💻 Author

**Akshun Mehrotra**

AI Internship Project

Developed as part of a Contact Center automation initiative to simplify log investigation using Artificial Intelligence and Root Cause Analysis.

---

### ⭐ If you found this project useful, consider giving it a Star.
