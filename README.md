# Job Tracker Automation

A Python-based automation tool that collects job postings from company career pages, filters them based on relevance, and sends a daily email summary of the best matches.

---

## Why I Built This

While searching for Data Analyst roles, I noticed:

- Job boards like Indeed and LinkedIn are noisy and repetitive
- Many relevant jobs are posted directly on company career pages
- Manually checking multiple sites daily is inefficient

So I built this system to automate the process and surface only relevant opportunities.

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

## Example Output

### Terminal Output

### Email Summary

![Email Screenshot](assets/email_sample.png)

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

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Rutvikmerai/job-tracker-automation.git
cd job-tracker-automation
