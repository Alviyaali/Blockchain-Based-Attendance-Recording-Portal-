# Blockchain-Based Attendance Recording Portal

> **A secure, tamper-proof attendance marking system powered by blockchain technology**

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.1.2-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Usage Guide](#usage-guide)
- [Blockchain Implementation](#blockchain-implementation)
- [Security Features](#security-features)
- [Sample Data](#sample-data)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 About the Project

The **Blockchain-Based Attendance Recording Portal** is a web application that securely records and maintains attendance using a custom Python blockchain implementation. This system eliminates the possibility of data tampering, prevents duplicate entries, and ensures complete transparency and immutability of attendance records.

### Problem Statement
Traditional attendance systems are vulnerable to:
- **Data Tampering**: Records can be altered after entry
- **Duplicate Entries**: Same student marked multiple times on the same date
- **Lost Records**: No audit trail for modifications
- **Unauthorized Access**: No cryptographic verification

### Solution
By leveraging blockchain technology with SHA-256 hashing and Proof of Work (PoW), this system ensures:
- ✅ **Immutable Records**: Once added, attendance cannot be modified
- ✅ **Duplicate Prevention**: System prevents same student-date combinations
- ✅ **Complete Audit Trail**: Hash chain provides cryptographic verification
- ✅ **Real-time Recording**: Instant marking with mining confirmation
- ✅ **Historical Tracking**: Full attendance history with timestamps

---

## ⭐ Key Features

| Feature | Description |
|---------|-------------|
| **🔐 Blockchain Technology** | Custom Python blockchain with SHA-256 hashing |
| **⛏️ Proof of Work (PoW)** | Difficulty-based mining (default: 3 leading zeros) |
| **📝 Attendance Marking** | Simple form-based interface for marking attendance |
| **📊 Ledger Viewing** | Display complete blockchain ledger in real-time |
| **🔍 History Search** | Search individual student attendance history |
| **🔗 Chain Verification** | Validate blockchain integrity on-demand |
| **💾 Persistent Storage** | JSON-based storage for blockchain data |
| **🌐 REST API** | Flask-based RESTful API endpoints |
| **🛡️ CORS Enabled** | Cross-Origin Resource Sharing for web security |
| **⚡ Real-time Updates** | Auto-refresh ledger after new entries |

---

## 🛠️ Technology Stack

| Category | Technology |
|----------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) |
| **Backend** | Python 3.8+, Flask 3.1.2 |
| **Blockchain** | Custom Python implementation |
| **Cryptography** | SHA-256 (hashlib) |
| **Database** | JSON (File-based) |
| **API** | REST with Flask-CORS |
| **Server** | Flask development server |

---

## 📁 Project Structure

```
Blockchain-Based-Attendance-Recording-Portal/
│
├── README.md                          # Project documentation
├── PROJECT_DOCUMENTATION.md           # Detailed technical documentation
├── requirements.txt                   # Python dependencies
├── attendance_data.json               # Persistent blockchain storage
│
├── Backend/                           # Flask API Server
│   ├── app.py                         # Flask application entry point
│   ├── blockchain_1.py                # Block & Blockchain classes
│   ├── core_logic.py                  # Initialization & persistence
│   ├── routs.py                       # API endpoint definitions
│   └── __pycache__/                   # Compiled Python files
│
└── Frontend/                          # Web Interface
    └── index.html                     # Main UI application
```

### File Descriptions

| File | Purpose |
|------|---------|
| **app.py** | Initializes Flask app, enables CORS, registers blueprints |
| **blockchain_1.py** | Core blockchain logic: Block class, Blockchain class |
| **core_logic.py** | Initialization, JSON persistence, chain loading |
| **routs.py** | Flask API routes and endpoints |
| **index.html** | User interface with forms and ledger display |
| **attendance_data.json** | Persistent storage of blockchain blocks |

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ index.html - Web Interface                             │  │
│  │ • Mark Attendance Form                                 │  │
│  │ • Blockchain Ledger Display                            │  │
│  │ • Student History Search                               │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────┬───────────────────────────────────────┘
                       │ HTTP/REST JSON
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                    API LAYER                                  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Flask Application (app.py)                             │  │
│  │ • Routes Manager (routs.py)                            │  │
│  │ • CORS Enabled                                         │  │
│  │ • Port: 5000                                           │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────┬───────────────────────────────────────┘
                       │ Calls
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                  BLOCKCHAIN LAYER                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Blockchain Engine (blockchain_1.py)                    │  │
│  │                                                         │  │
│  │ Block Class:                                            │  │
│  │ • calculate_hash() - SHA-256 hashing                   │  │
│  │ • mine_block() - Proof of Work                         │  │
│  │ • nonce - Work counter                                 │  │
│  │                                                         │  │
│  │ Blockchain Class:                                       │  │
│  │ • create_genesis_block() - Initial block               │  │
│  │ • add_block() - Add new attendance                      │  │
│  │ • verify_chain() - Integrity check                     │  │
│  │ • attendance_log - Duplicate prevention                │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────┬───────────────────────────────────────┘
                       │ Reads/Writes
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                  STORAGE LAYER                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ JSON File (attendance_data.json)                       │  │
│  │ • Serialized blockchain blocks                         │  │
│  │ • Persistent data across sessions                      │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

Before setting up the project, ensure you have:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** (Python package manager) - Usually comes with Python
- **Git** (optional) - For cloning the repository
- **Modern Web Browser** - Chrome, Firefox, Edge, Safari
- **Text Editor** (optional) - VS Code, PyCharm, or similar

### System Requirements
- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 512MB
- **Disk Space**: Minimum 100MB
- **Internet**: Not required for local execution

---

## 🚀 Installation & Setup

### Step 1: Clone or Download the Project

**Using Git:**
```bash
git clone <repository-url>
cd Blockchain-Based-Attendance-Recording-Portal
```

**Or download and extract the ZIP file manually.**

### Step 2: Navigate to Project Directory

```bash
# Windows
cd path\to\Blockchain-Based-Attendance-Recording-Portal

# macOS/Linux
cd path/to/Blockchain-Based-Attendance-Recording-Portal
```

### Step 3: Create a Python Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed Flask-3.1.2 flask_cors-6.0.2
```

### Step 5: Verify Installation

```bash
python --version
python -m flask --version
```

---

## ▶️ Running the Project

### Method 1: Using Python Directly

#### Terminal 1 - Start Flask Backend:

```bash
cd Backend
python app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

#### Terminal 2 - Open Frontend:

**Windows:**
```bash
start Frontend\index.html
```

**macOS:**
```bash
open Frontend/index.html
```

**Linux:**
```bash
xdg-open Frontend/index.html
```

**Or manually:**
1. Open your web browser
2. Navigate to `Frontend/index.html` (file path)

> **Note**: If opening directly doesn't work, use a local server (see Method 2)

---

### Method 2: Using Live Server (Recommended)

#### Start Backend:
```bash
cd Backend
python app.py
```

#### Open Frontend with Live Server:

**Using Python's built-in server:**
```bash
cd Frontend
python -m http.server 5500
```

Then open: `http://127.0.0.1:5500`

**Using VS Code Live Server Extension:**
1. Install "Live Server" extension in VS Code
2. Right-click `index.html` → "Open with Live Server"
3. Ensure backend is running on port 5000

---

## 📡 API Endpoints

### Base URL
```
http://127.0.0.1:5000
```

### 1. **Health Check**
```
GET /
```
**Response:**
```json
"📘 Attendance Blockchain Running!"
```

---

### 2. **Add Attendance Record**
```
POST /add
```

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "student": "Ahmad Zain",
  "date": "2026-01-26",
  "time": "22:13",
  "status": "Present"
}
```

**Success Response (201):**
```json
{
  "message": "Attendance Block Added!",
  "hash": "000fc5a8b1aae7e1af417940a7e60dd9850febd468cd5c5a10ebfff9d9978072",
  "mining_time": 2.345,
  "data": {
    "student": "Ahmad Zain",
    "date": "2026-01-26",
    "time": "22:13",
    "status": "Present"
  }
}
```

**Error Response (409 - Duplicate):**
```json
{
  "error": "Attendance already marked for this student today"
}
```

**Error Response (400 - Missing Fields):**
```json
{
  "error": "Missing or empty field: student"
}
```

---

### 3. **Get Full Blockchain Ledger**
```
GET /chain
```

**Response:**
```json
[
  {
    "index": 0,
    "timestamp": 1769445574.2243032,
    "data": "Genesis Block - Attendance Ledger",
    "previous_hash": "0",
    "hash": "000dbf0d5e50261441f8949b465d711983b0fb3bdb1c41358f2dba70e3b3b650"
  },
  {
    "index": 1,
    "timestamp": 1769445802.6759732,
    "data": {
      "student": "Zain",
      "date": "2026-01-26",
      "time": "22:13",
      "status": "Present"
    },
    "previous_hash": "000dbf0d5e50261441f8949b465d711983b0fb3bdb1c41358f2dba70e3b3b650",
    "hash": "000fc5a8b1aae7e1af417940a7e60dd9850febd468cd5c5a10ebfff9d9978072"
  }
]
```

---

### 4. **Get Student Attendance History**
```
GET /history/{studentName}
```

**Example:**
```
GET /history/Ahmad%20Zain
```

**Response:**
```json
[
  {
    "index": 1,
    "date": "2026-01-26",
    "time": "22:13",
    "status": "Present",
    "hash": "000fc5a8b1aae7e1af417940a7e60dd9850febd468cd5c5a10ebfff9d9978072"
  },
  {
    "index": 2,
    "date": "2026-01-27",
    "time": "01:22",
    "status": "Present",
    "hash": "00050edee025bd44c2dba593210eed285ea38c89c7f1d2da9c4e299de0267311"
  }
]
```

---

## 💡 Usage Guide

### Marking Attendance

1. **Open the Frontend:**
   - Navigate to `index.html` in your web browser

2. **Fill in the Form:**
   - **Student Name**: Enter full name (e.g., "Ahmad Zain")
   - **Date**: Select date using date picker
   - **Time**: Select time using time picker
   - **Status**: Choose "Present" or "Absent"

3. **Submit:**
   - Click "Add Attendance" button
   - System will mine the block (may take 2-5 seconds)
   - Success message displays with mining time

4. **View Ledger:**
   - Blockchain updates automatically below the form
   - All recorded attendance displays in table format

### Searching History

1. **Enter Student Name:**
   - Type student name in "Search Attendance History" field
   - Click "Show History"

2. **View Results:**
   - All attendance records for that student display
   - Shows Date, Time, and Status

### Verifying Blockchain Integrity

To verify the blockchain hasn't been tampered with:

```python
# From Python terminal:
from Backend.core_logic import attendance_chain

# Verify chain integrity
is_valid = attendance_chain.verify_chain()
print(f"Blockchain Valid: {is_valid}")
```

---

## ⛓️ Blockchain Implementation

### Block Structure

Each block contains:

```python
class Block:
    index        # Position in chain (0 = genesis)
    timestamp    # Creation time (Unix timestamp)
    data         # Attendance data or message
    previous_hash # Hash of previous block
    nonce        # Proof of Work counter
    hash         # SHA-256 hash of block
```

### Hashing Algorithm

```
SHA-256({
  "index": 1,
  "timestamp": 1769445802.6759732,
  "data": {"student": "Zain", ...},
  "previous_hash": "000dbf0d5e50...",
  "nonce": 12345
}) → "000fc5a8b1aae7e1af417940a7e60dd9850febd..."
```

### Proof of Work (PoW)

- **Difficulty**: 3 (default) - requires 3 leading zeros
- **Process**: Incrementally increase nonce until hash matches target
- **Time**: ~2-5 seconds per block (varies by machine)
- **Purpose**: Makes tampering computationally expensive

### Chain Validation

```python
verify_chain():
    For each block (starting from block 1):
        ✓ Verify current block hash is correct
        ✓ Verify current.previous_hash matches previous.hash
    Return True if all valid, False if tampered
```

---

## 🔐 Security Features

### 1. **Cryptographic Hashing**
- SHA-256 hashing ensures data integrity
- Any change to block data produces different hash
- Makes tampering instantly detectable

### 2. **Proof of Work**
- Difficulty-based mining prevents rapid block creation
- Computationally expensive to forge blocks
- Deters malicious modifications

### 3. **Duplicate Prevention**
- Attendance log tracks `{student}-{date}` keys
- Prevents marking same student twice on same day
- Returns 409 error for duplicate entries

### 4. **Chain Linking**
- Each block references previous block's hash
- Breaking any block breaks all subsequent blocks
- Ensures immutability of past records

### 5. **CORS Protection**
- API only accepts requests from allowed origin
- Configured for `http://127.0.0.1:5500`
- Prevents unauthorized cross-origin requests

### 6. **Data Validation**
- Required fields validation on backend
- Type checking for attendance data
- Error handling for malformed requests

---

## 📊 Sample Data

The project includes `attendance_data.json` with sample records:

```json
[
  {
    "index": 0,
    "timestamp": 1769445574.2243032,
    "data": "Genesis Block - Attendance Ledger",
    "previous_hash": "0",
    "hash": "000dbf0d5e50261441f8949b465d711983b0fb3bdb1c41358f2dba70e3b3b650"
  },
  {
    "index": 1,
    "timestamp": 1769445802.6759732,
    "data": {
      "student": "Zain",
      "date": "2026-01-26",
      "time": "22:13",
      "status": "Present"
    },
    "previous_hash": "000dbf0d5e50261441f8949b465d711983b0fb3bdb1c41358f2dba70e3b3b650",
    "hash": "000fc5a8b1aae7e1af417940a7e60dd9850febd468cd5c5a10ebfff9d9978072"
  }
]
```

To start fresh, delete or backup `attendance_data.json`, and the system will create a new one with only the genesis block.

---

## 🐛 Troubleshooting

### Issue: "Connection refused" or "Cannot GET /"

**Solution:**
- Ensure Flask backend is running on port 5000
- Check command: `python app.py` in Backend folder
- Verify no other process uses port 5000

### Issue: "CORS error" or "Access denied"

**Solution:**
- Verify frontend is on `http://127.0.0.1:5500`
- Check CORS configuration in `app.py` matches your frontend URL
- Clear browser cache and refresh

### Issue: "Mining takes too long" (>30 seconds)

**Solution:**
- Normal on slow machines (reduce difficulty in `blockchain_1.py`)
- Modify `self.difficulty = 2` for faster mining
- Check system resources (CPU, memory)

### Issue: "attendance_data.json not found"

**Solution:**
- File is auto-created on first run
- Ensure Backend folder has write permissions
- Check file path is in project root

### Issue: "Module not found" errors

**Solution:**
```bash
# Verify packages are installed
pip list

# Reinstall if needed
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.8+
```

### Issue: Port 5000 already in use

**Solution:**
```bash
# Kill process using port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
kill -9 <PID>
```

---

## 📚 Additional Resources

- **PROJECT_DOCUMENTATION.md** - Detailed technical documentation
- **requirements.txt** - Complete dependency list
- **attendance_data.json** - Blockchain storage format

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub

---

## 🙏 Acknowledgments

- Built with Flask for REST API
- Blockchain implementation using Python
- SHA-256 cryptographic hashing
- Inspired by blockchain technology principles

---

**Last Updated**: January 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✅
