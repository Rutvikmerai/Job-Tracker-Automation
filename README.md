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

![Terminal Output](https://github.com/user-attachments/assets/8404c7af-a8d3-47a4-80ed-d281e1e380c4)

### Email Summary

![Email Screenshot](https://github.com/user-attachments/assets/de7962e3-e09e-4048-9264-3e8ab51df01d)

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

