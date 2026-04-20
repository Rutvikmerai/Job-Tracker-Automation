import sqlite3
from pathlib import Path

DB_PATH = Path("data/jobs.db")


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                source_company TEXT,
                external_job_id TEXT,
                title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                remote_type TEXT,
                department TEXT,
                employment_type TEXT,
                description TEXT,
                posted_date TEXT,
                url TEXT NOT NULL,
                score REAL DEFAULT 0,
                matched_keywords TEXT,
                first_seen_at TEXT NOT NULL,
                last_seen_at TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                UNIQUE(source, url)
            )
        """)
        conn.commit()


def upsert_job(job: dict) -> bool:
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT id FROM jobs WHERE source = ? AND url = ?",
            (job["source"], job["url"])
        ).fetchone()

        if existing:
            conn.execute("""
                UPDATE jobs
                SET title = ?,
                    company = ?,
                    location = ?,
                    remote_type = ?,
                    department = ?,
                    employment_type = ?,
                    description = ?,
                    posted_date = ?,
                    score = ?,
                    matched_keywords = ?,
                    last_seen_at = ?,
                    is_active = 1
                WHERE source = ? AND url = ?
            """, (
                job["title"],
                job.get("company"),
                job.get("location"),
                job.get("remote_type"),
                job.get("department"),
                job.get("employment_type"),
                job.get("description"),
                job.get("posted_date"),
                job.get("score", 0),
                job.get("matched_keywords"),
                job["last_seen_at"],
                job["source"],
                job["url"],
            ))
            conn.commit()
            return False

        conn.execute("""
            INSERT INTO jobs (
                source,
                source_company,
                external_job_id,
                title,
                company,
                location,
                remote_type,
                department,
                employment_type,
                description,
                posted_date,
                url,
                score,
                matched_keywords,
                first_seen_at,
                last_seen_at,
                is_active
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job["source"],
            job.get("source_company"),
            job.get("external_job_id"),
            job["title"],
            job.get("company"),
            job.get("location"),
            job.get("remote_type"),
            job.get("department"),
            job.get("employment_type"),
            job.get("description"),
            job.get("posted_date"),
            job["url"],
            job.get("score", 0),
            job.get("matched_keywords"),
            job["first_seen_at"],
            job["last_seen_at"],
            1,
        ))
        conn.commit()
        return True


def fetch_jobs_seen_since(run_started: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT *
            FROM jobs
            WHERE first_seen_at >= ?
            ORDER BY score DESC, first_seen_at DESC
        """, (run_started,)).fetchall()
        return [dict(row) for row in rows]


def fetch_top_matching_jobs(limit: int = 20) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT *
            FROM jobs
            WHERE is_active = 1
            ORDER BY score DESC, last_seen_at DESC
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(row) for row in rows]