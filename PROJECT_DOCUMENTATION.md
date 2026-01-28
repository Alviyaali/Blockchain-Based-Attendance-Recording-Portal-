# Blockchain-Based Attendance Recording Portal - Detailed Documentation

## Table of Contents
1. [Project Purpose](#project-purpose)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Data Flow](#data-flow)
5. [Backend Functions](#backend-functions)
6. [API Endpoints](#api-endpoints)
7. [Frontend Components](#frontend-components)
8. [Database Structure](#database-structure)
9. [Security Features](#security-features)
10. [Usage Guide](#usage-guide)

---

## Project Purpose

The **Blockchain-Based Attendance Recording Portal** is a web application designed to securely record and maintain student/employee attendance using blockchain technology. The system prevents:

- **Data Tampering**: Once attendance is recorded and added to the blockchain, it cannot be modified without detection
- **Duplicate Entries**: Prevents marking the same student as present/absent multiple times on the same date
- **Loss of Records**: Uses SHA-256 hashing and Proof of Work (PoW) to ensure immutability
- **Unauthorized Access**: Each record is cryptographically secured

### Key Objectives:
- Provide a tamper-proof attendance system
- Implement blockchain as an immutable ledger
- Allow real-time attendance marking
- Maintain complete attendance history with timestamps
- Verify blockchain integrity at any time

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (HTML/JS)                       │
│  - Mark Attendance Form                                     │
│  - View Blockchain Ledger                                   │
│  - Search Attendance History                                │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP Requests
                       │ JSON Data
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              FLASK API SERVER (app.py)                       │
│  - /add       (POST)  - Add attendance record               │
│  - /chain     (GET)   - Retrieve full blockchain            │
│  - /history   (GET)   - Get student attendance history      │
│  - /          (GET)   - Health check                        │
└──────────────────────┬──────────────────────────────────────┘
                       │ Uses
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           BLOCKCHAIN ENGINE (blockchain_1.py)               │
│  - Block Class                                              │
│    • calculate_hash()                                       │
│    • mine_block(difficulty)                                 │
│  - Blockchain Class                                         │
│    • create_genesis_block()                                 │
│    • add_block(data)                                        │
│    • verify_chain()                                         │
│    • get_latest_block()                                     │
└──────────────────────┬──────────────────────────────────────┘
                       │ Reads/Writes
                       ▼
┌─────────────────────────────────────────────────────────────┐
│        PERSISTENT STORAGE (attendance_data.json)            │
│  - JSON array of serialized blockchain blocks              │
└─────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | HTML, CSS, JavaScript | User interface for marking attendance |
| **Backend** | Flask, Flask-CORS | REST API server |
| **Blockchain** | Python, SHA-256, JSON | Cryptographic hashing & block management |
| **Storage** | JSON file (attendance_data.json) | Persistent data storage |
| **Hashing** | hashlib (SHA-256) | Cryptographic block identification |
| **Communication** | HTTP/REST, JSON | Client-Server communication |

---

## Data Flow

### 1. **Marking Attendance Flow**

```
User Fills Form (index.html)
    ↓
User Clicks "Add Attendance"
    ↓
JavaScript: addEntry() function collects:
  - Student Name
  - Date
  - Time
  - Status (Present/Absent)
    ↓
fetch() → POST /add endpoint with JSON body
    ↓
Flask app.py receives data
    ↓
Validation: Check for required fields
    ↓
attendance_chain.add_block(data) is called
    ↓
BLOCKCHAIN PROCESSING:
  ├─ Create unique key: "{student}-{date}"
  ├─ Check if key exists in attendance_log
  ├─ If exists → Return 409 (Conflict) error
  ├─ If new:
  │   ├─ Get latest block (previous_hash)
  │   ├─ Create new Block object with data
  │   ├─ Mine block (find nonce that gives difficulty=3 leading zeros)
  │   ├─ Append to blockchain.chain
  │   └─ Add key to attendance_log
    ↓
save_chain() serializes blockchain to JSON
    ↓
Return 201 (Created) with block hash & mining time
    ↓
JavaScript updates UI:
  ├─ Show success message
  ├─ Reload blockchain table
  └─ Clear form fields
```

### 2. **Retrieving Full Ledger Flow**

```
User Loads Page / Clicks Refresh
    ↓
JavaScript: loadChain() function executes
    ↓
fetch() → GET /chain endpoint
    ↓
Flask iterates through attendance_chain.chain
    ↓
For each Block, extract:
  - index
  - timestamp
  - data (student, date, time, status)
  - previous_hash
  - hash
    ↓
Return JSON array of all blocks
    ↓
JavaScript:
  ├─ Parse JSON response
  ├─ Clear existing table
  ├─ Insert new rows for each block
  └─ Display in HTML table
```

### 3. **Searching Attendance History Flow**

```
User enters Student Name in search box
    ↓
User clicks "Show History"
    ↓
JavaScript: loadHistory() function
    ↓
fetch() → GET /history/{studentName}
    ↓
Flask app.py:
  ├─ Iterate through attendance_chain.chain
  ├─ Find blocks where block.data.student == studentName
  ├─ Extract: index, date, time, status, hash
  └─ Collect in history_list
    ↓
Return JSON array of matching records
    ↓
JavaScript displays in formatted table
```

### 4. **Blockchain Verification Flow** (On-Demand)

```
Client calls: attendance_chain.verify_chain()
    ↓
For each block (starting at index 1):
  ├─ Recalculate block's hash
  ├─ Compare with stored hash
  ├─ Check previous_hash matches previous block's hash
  └─ If mismatch → Return False
    ↓
If all blocks valid → Return True
```

---

## Backend Functions

### **blockchain_1.py**

#### **Block Class**

##### **`__init__(index, timestamp, data, previous_hash='')`**
- **Purpose**: Initialize a new block in the blockchain
- **Parameters**:
  - `index` (int): Block position in chain (0 for genesis)
  - `timestamp` (float): Unix timestamp when block created
  - `data` (dict/str): Attendance data {student, date, time, status}
  - `previous_hash` (str): Hash of previous block
- **Returns**: Block object
- **Side Effects**: Calls `calculate_hash()` to set initial hash
- **Example**:
  ```python
  block = Block(1, time(), {"student": "Alviya", "date": "2025-11-10"}, "00092bde...")
  ```

##### **`calculate_hash()`**
- **Purpose**: Generate SHA-256 hash of block content
- **Process**:
  1. Create dictionary with: index, timestamp, data, previous_hash, nonce
  2. Convert to JSON string (sorted keys for consistency)
  3. Encode as bytes
  4. Apply SHA-256 hashing
  5. Return hexadecimal hash
- **Returns**: 64-character hex string (SHA-256)
- **Note**: Hash changes if nonce changes (used in mining)
- **Example Output**: `000b48d3920b1f5ebf4e81f18679c1b5f8bf9518ff150db1b9e78f1609556e5f`

##### **`mine_block(difficulty)`**
- **Purpose**: Perform Proof of Work (PoW) to secure the block
- **Parameters**:
  - `difficulty` (int): Number of leading zeros required in hash (default: 3)
- **Algorithm**:
  1. Create target string of `difficulty` zeros (e.g., "000" for difficulty=3)
  2. Initialize nonce to 0
  3. Loop until `hash[:difficulty] == target`:
     - Increment nonce
     - Recalculate hash
  4. Record mining time
  5. Print mining status and time
- **Returns**: Mining time in seconds (float)
- **Security**: Prevents rapid block creation; computationally expensive to forge
- **Example Output**:
  ```
  ⛏ Mining block 1 with difficulty 3...
  ✅ Block mined: 000b48d3920b1f5ebf4e81f18679c1b5f8bf9518ff150db1b9e78f1609556e5f
  ⏱ Mining time: 0.245 seconds
  ```

---

#### **Blockchain Class**

##### **`__init__()`**
- **Purpose**: Initialize the blockchain with genesis block
- **Attributes**:
  - `difficulty` (int): Set to 3 (leading zeros required)
  - `chain` (list): Starts with genesis block
  - `attendance_log` (dict): Tracks {student-date: True} to prevent duplicates
- **Side Effects**: Creates and mines genesis block

##### **`create_genesis_block()`**
- **Purpose**: Create the first block in the blockchain
- **Block Content**: 
  - Index: 0
  - Timestamp: Current time
  - Data: "Genesis Block - Attendance Ledger"
  - Previous Hash: "0" (no predecessor)
- **Process**:
  1. Create Block object
  2. Mine block with difficulty=3
  3. Return block
- **Returns**: Mined Block object
- **Note**: Called once during Blockchain initialization

##### **`get_latest_block()`**
- **Purpose**: Retrieve the most recent block in chain
- **Returns**: Last Block object in `self.chain`
- **Safety**: Creates genesis block if chain is empty
- **Usage**: Used to get previous_hash for new blocks

##### **`add_block(data)`**
- **Purpose**: Add a new attendance record to blockchain
- **Parameters**:
  - `data` (dict): {student, date, time, status}
- **Validation**:
  1. Extract student name and date from data
  2. Create key: `{student}-{date}`
  3. Check if key exists in `attendance_log`
  4. If exists → Return error 409 (Duplicate prevention)
- **Block Creation**:
  1. Get previous block's hash
  2. Create new Block with:
     - index = len(chain)
     - timestamp = current time
     - data = attendance data
     - previous_hash = latest block's hash
  3. Mine the block (PoW)
  4. Append to chain
  5. Add key to attendance_log
- **Returns**: Tuple `(response_dict, status_code)`
  - Success: `({"success": True, "mining_time": X}, 201)`
  - Duplicate: `({"error": "..."}, 409)`
- **Example**:
  ```python
  response, status = blockchain.add_block({
      "student": "James",
      "date": "2025-11-19",
      "time": "11:30",
      "status": "Present"
  })
  # Returns: ({"success": True, "mining_time": 0.189}, 201)
  ```

##### **`verify_chain()`**
- **Purpose**: Validate blockchain integrity
- **Verification Steps**:
  1. For each block (starting from index 1):
     - Recalculate block's hash
     - Check if matches stored hash
     - Verify previous_hash matches previous block's hash
  2. Any mismatch indicates tampering
- **Returns**: Boolean (True if valid, False if tampered)
- **Use Case**: Audit and security verification
- **Example**:
  ```python
  if blockchain.verify_chain():
      print("✅ Blockchain is valid")
  else:
      print("⚠️ Blockchain has been tampered with!")
  ```

---

### **app.py (Flask Application)**

#### **`save_chain()`**
- **Purpose**: Serialize blockchain to JSON file
- **Process**:
  1. Create empty list `data_list`
  2. For each block in `attendance_chain.chain`:
     - Extract: index, timestamp, data, previous_hash, hash
     - Append dictionary to `data_list`
  3. Write to file with indentation (4 spaces)
- **File**: `attendance_data.json`
- **Called**: After each successful block addition
- **Format**: Pretty-printed JSON for readability

#### **`home()` Route**
- **Endpoint**: GET `/`
- **Purpose**: Health check / API status
- **Returns**: "📘 Attendance Blockchain Running!"
- **Status Code**: 200 (OK)

#### **`add_block()` Route**
- **Endpoint**: POST `/add`
- **Purpose**: Mark attendance for a student
- **Request Body** (JSON):
  ```json
  {
    "student": "Student Name",
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "status": "Present or Absent"
  }
  ```
- **Validation**:
  1. Check all required fields present and not empty
  2. Return 400 (Bad Request) if validation fails
- **Processing**:
  1. Call `attendance_chain.add_block(data)`
  2. If status != 201 → Return error
  3. Call `save_chain()` to persist
  4. Get latest block details
- **Response** (201 Created):
  ```json
  {
    "message": "Attendance Block Added!",
    "hash": "000b48d3920...",
    "mining_time": 0.245,
    "data": { "student": "...", "date": "...", ... }
  }
  ```
- **Error Responses**:
  - 400: Missing/empty field
  - 409: Duplicate attendance for same date

#### **`chain()` Route**
- **Endpoint**: GET `/chain`
- **Purpose**: Retrieve entire blockchain
- **Returns**: JSON array of all blocks with:
  - index
  - timestamp
  - data
  - previous_hash
  - hash
- **Status Code**: 200 (OK)
- **Usage**: Frontend loads full ledger
- **Response Size**: Grows with number of blocks

#### **`history(student)` Route**
- **Endpoint**: GET `/history/<student>`
- **Purpose**: Get attendance history for specific student
- **Parameters**:
  - `student` (str): Student name from URL path
- **Processing**:
  1. Iterate through all blocks
  2. Find blocks where `block.data.student == student`
  3. Extract: index, date, time, status, hash
  4. Collect in list
- **Returns**: JSON array of matching records
  ```json
  [
    {
      "index": 1,
      "date": "2025-11-10",
      "time": "11:30",
      "status": "Present",
      "hash": "000b48d3920..."
    },
    ...
  ]
  ```
- **Empty Result**: Returns `[]` if no records found

---

## API Endpoints

| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| GET | `/` | Health check | None | "📘 Attendance Blockchain Running!" |
| POST | `/add` | Mark attendance | {student, date, time, status} | {message, hash, mining_time, data} |
| GET | `/chain` | Get full blockchain | None | [{index, timestamp, data, previous_hash, hash}, ...] |
| GET | `/history/<student>` | Get student history | None (in URL) | [{index, date, time, status, hash}, ...] |

---

## Frontend Components

### **index.html Structure**

#### **1. Input Form Section**
```html
<input id="name" type="text">              <!-- Student Name -->
<input id="date" type="date">               <!-- Date Picker -->
<input id="time" type="time">               <!-- Time Picker -->
<select id="status">                        <!-- Present/Absent -->
<button onclick="addEntry()">              <!-- Submit Button -->
```

#### **2. Blockchain Ledger Display**
```html
<table id="tbl">                            <!-- Full chain table -->
  <tr><th>Index</th><th>Student</th>...
```

#### **3. History Search Section**
```html
<input id="historyName">                    <!-- Student name search -->
<button onclick="loadHistory()">           <!-- Load history button -->
<div id="historyBox">                      <!-- History results table -->
```

### **JavaScript Functions**

#### **`addEntry()`**
- **Triggered**: When user clicks "Add Attendance" button
- **Steps**:
  1. Collect form values: name, date, time, status
  2. Validate all fields filled
  3. Create JSON body object
  4. Send POST request to `/add` endpoint
  5. Display success message
  6. Call `loadChain()` to refresh table
- **Error Handling**: Alert if validation fails

#### **`loadChain()`**
- **Triggered**: On page load and after adding entry
- **Steps**:
  1. Fetch GET `/chain`
  2. Parse JSON response
  3. Clear table (reset innerHTML)
  4. For each block:
     - Insert row
     - Populate: index, student, date, time, status
  5. Handle blocks with missing data (show "-")

#### **`loadHistory()`**
- **Triggered**: When user clicks "Show History" button
- **Steps**:
  1. Get student name from input
  2. Validate name entered
  3. Fetch GET `/history/{studentName}`
  4. Parse response
  5. Build HTML table with results
  6. Display in `historyBox` div
  7. Handle no results gracefully

---

## Database Structure

### **attendance_data.json Format**

```json
[
  {
    "index": 0,
    "timestamp": 1763482543.372431,
    "data": "Genesis Block - Attendance Ledger",
    "previous_hash": "0",
    "hash": "00092bde3e94013c71aa5cd2e4fdcf2571ae5d9c94f38bed6bdbd2d8e37a3c83"
  },
  {
    "index": 1,
    "timestamp": 1763482581.4501975,
    "data": {
      "student": "Alviya",
      "date": "2025-11-10",
      "time": "11:30",
      "status": "Present"
    },
    "previous_hash": "00092bde3e94013c71aa5cd2e4fdcf2571ae5d9c94f38bed6bdbd2d8e37a3c83",
    "hash": "000b48d3920b1f5ebf4e81f18679c1b5f8bf9518ff150db1b9e78f1609556e5f"
  }
]
```

### **Block Structure**

| Field | Type | Description |
|-------|------|-------------|
| `index` | Integer | Position in blockchain (0 = genesis) |
| `timestamp` | Float | Unix timestamp of block creation |
| `data` | String/Dict | "Genesis Block..." OR {student, date, time, status} |
| `previous_hash` | String | Hash of preceding block (or "0" for genesis) |
| `hash` | String | SHA-256 hash of this block (64 chars) |

### **Runtime Memory Structure**

```python
attendance_chain = {
    "difficulty": 3,
    "chain": [Block, Block, Block, ...],
    "attendance_log": {
        "Alviya-2025-11-10": True,
        "James-2025-11-19": True,
        ...
    }
}
```

---

## Security Features

### **1. SHA-256 Hashing**
- **What**: Each block's content hashed with SHA-256
- **Why**: Impossible to reverse-engineer data from hash
- **Impact**: Any change to block data changes hash, breaking chain

### **2. Proof of Work (PoW)**
- **What**: Difficulty of 3 (find nonce for 3 leading zeros in hash)
- **Why**: Requires computational work to mine each block
- **Impact**: Slows down mining; makes tampering expensive
- **Example**: Block took 0.245 seconds to mine

### **3. Hash Chain**
- **What**: Each block contains previous block's hash
- **Why**: Links blocks together; tampering one breaks all subsequent blocks
- **Impact**: Can detect tampering at any point in chain

### **4. Duplicate Prevention**
- **What**: attendance_log tracks {student}-{date} combinations
- **Why**: Prevents marking same student twice on same day
- **Impact**: Returns 409 error on duplicate attempts

### **5. Immutability**
- **What**: Once block added and saved, modifying is detected
- **Why**: `verify_chain()` recalculates hashes; tampering breaks verification
- **Impact**: Auditable and tamper-evident

---

## Usage Guide

### **1. Starting the Application**

```bash
cd "c:\Users\az682\OneDrive\Desktop\Block\Blockchain-Based-Attendance-Recording-Portal\venv"
python app.py
```

**Output**:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### **2. Accessing the Web Interface**

- Open browser: `http://127.0.0.1:5000`
- You should see: "📘 Attendance Blockchain Running!"
- Navigate to `index.html` or open directly

### **3. Marking Attendance**

1. **Fill Form**:
   - Student Name: "Alviya"
   - Date: "2025-11-10"
   - Time: "11:30"
   - Status: "Present"

2. **Click "Add Attendance"**
   - Block is mined (shows in console)
   - Blockchain updated
   - Data saved to JSON
   - Table refreshed

3. **Check Ledger**
   - New row appears in table
   - Shows all attributes

### **4. Searching History**

1. **Enter Student Name**: "Alviya"
2. **Click "Show History"**
3. **View Results**:
   - All attendance records for that student
   - Date, time, status visible
   - Formatted in table

### **5. Verifying Blockchain**

```python
# In Python console
from blockchain_1 import Blockchain
blockchain = Blockchain()
is_valid = blockchain.verify_chain()
print(f"Blockchain valid: {is_valid}")
```

---

## Example Workflow

```
Step 1: User enters attendance data
        Name: "James", Date: "2025-11-19", Time: "11:30", Status: "Present"

Step 2: Frontend sends POST /add request

Step 3: Flask validates data
        ✓ All fields present
        ✓ Not a duplicate

Step 4: Blockchain processes
        ├─ Create Block(index=4, data={...}, previous_hash="000d70087...")
        ├─ Mine block: Try nonce values until hash starts with "000"
        ├─ Found nonce=45231 → hash="0005a3249a96be4df..."
        ├─ Append to chain
        └─ Add "James-2025-11-19" to attendance_log

Step 5: Save to disk
        ├─ Serialize all 5 blocks (genesis + 4 attendance)
        └─ Write to attendance_data.json (pretty-printed)

Step 6: Return response
        {
          "message": "Attendance Block Added!",
          "hash": "0005a3249a96be4df4982a0cdef4645781d13c79...",
          "mining_time": 0.189,
          "data": {...}
        }

Step 7: Frontend updates
        ├─ Show success message ✔
        ├─ Reload blockchain table
        └─ Clear form fields

Step 8: User searches "James" history
        ├─ Backend finds 1 record
        └─ Frontend displays date, time, status
```

---

## File Structure

```
Block/
├── Blockchain-Based-Attendance-Recording-Portal/
│   └── venv/
│       ├── app.py                          [Flask server & routes]
│       ├── blockchain_1.py                 [Block & Blockchain classes]
│       ├── index.html                      [Frontend UI]
│       ├── attendance_data.json            [Persistent blockchain storage]
│       ├── README.md                       [Quick overview]
│       └── PROJECT_DOCUMENTATION.md        [This file - detailed docs]
└── attendance_data.json                    [Backup copy]
```

---

## Conclusion

This system demonstrates a practical application of blockchain technology for attendance management. By leveraging SHA-256 hashing, Proof of Work, and hash chaining, it creates an immutable, tamper-evident attendance record that is secure, auditable, and trustworthy.

**Key Strengths**:
- ✅ Tamper-proof (cryptographic hashing)
- ✅ Immutable (chain validation)
- ✅ Duplicate-resistant (attendance_log)
- ✅ Auditable (full history preserved)
- ✅ User-friendly (simple web interface)

**Potential Enhancements**:
- Database integration (SQL/MongoDB) for scalability
- Authentication/authorization for faculty
- Attendance reports and analytics
- Mobile app interface
- Role-based access control
- Automatic backup mechanisms
