# Job Tracker Automation

A Python-based automation tool that collects job postings from company career pages, filters them based on relevance, and sends a daily email summary of the best matches.

---

## Why I Built This

While searching for Data Analyst roles, I noticed:

- Job boards like Indeed and LinkedIn are noisy and repetitive 
- Many relevant jobs are posted directly on company career pages
- Manually checking multiple sites daily is inefficient

So I built this system to automate the process and surface only high-quality, relevant opportunities.

---

## What It Does

- Collects jobs from multiple company job boards (Greenhouse API)
- Filters jobs by:
  - Location (United States / Remote)
  - Role (Data Analyst / Business Analyst)
  - Experience level (Entry-level / Internship preference)
- Scores and ranks jobs based on relevance
- Stores jobs in SQLite database (avoids duplicates)
- Exports results to CSV
- Sends a daily email summary with top matching jobs

---

## How It Works (Architecture)
Company Job Boards (Greenhouse API)
↓
Python Collector (requests)
↓
Scoring & Filtering Layer
↓
SQLite Database (deduplication)
↓
CSV Export
↓
Email Summary (SMTP)


---

## Example Output

### Terminal Output
<img width="1184" height="310" alt="output" src="https://github.com/user-attachments/assets/8e605d20-7f7f-42bc-a9e9-ba64a023b92a" />

### Email Summary

<img width="1534" height="291" alt="Email output" src="https://github.com/user-attachments/assets/6bf58883-ed17-49fd-91a5-bf764f0e493f" />


---

## Tech Stack

- Python
- Requests (API calls)
- SQLite (data storage)
- SMTP (email automation)
- Environment variables for configuration

---

## Project Structure


job-tracker-automation/
│
├── app/
│ ├── main.py
│ ├── scoring.py
│ ├── storage.py
│ ├── emailer.py
│ ├── config.py
│ ├── services/
│ └── sources/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md


---
## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Rutvikmerai/job-tracker-automation.git
cd job-tracker-automation

---
### 2. Create virtual environment

python -m venv venv
venv\Scripts\activate

---

### 3. Install dependencies

pip install -r requirements.txt

---


### 4. Configure environment variables

Create a .env file based on .env.example

---

### 5. Run the project

python -m app.main

