import logging
from pathlib import Path
from datetime import datetime, UTC

from app.config import MIN_SCORE
from app.storage import (
    init_db,
    upsert_job,
    fetch_jobs_seen_since,
    fetch_top_matching_jobs,
)
from app.services.collector import collect_all_jobs
from app.services.reporter import export_jobs_to_csv
from app.scoring import score_job
from app.emailer import build_html_email, send_summary_email

Path("logs").mkdir(exist_ok=True)


logging.basicConfig(
    filename="logs/tracker.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def run_tracker() -> None:
    print("1. Starting tracker")

    init_db()
    print("2. Database initialized")

    run_started = datetime.now(UTC).isoformat()

    jobs = collect_all_jobs()
    print(f"3. Collected {len(jobs)} jobs")

    inserted_count = 0
    kept_jobs = []

    for job in jobs:
        score, matches = score_job(job)
        job["score"] = score
        job["matched_keywords"] = ", ".join(matches)

        if score < MIN_SCORE:
            continue

        kept_jobs.append(job)

        is_new = upsert_job(job)
        if is_new:
            inserted_count += 1

    print(f"4. Jobs kept after scoring: {len(kept_jobs)}")
    print(f"5. New jobs inserted: {inserted_count}")

    new_jobs = fetch_jobs_seen_since(run_started)

    # fallback logic
    if new_jobs:
        jobs_for_email = new_jobs
        subject = f"Daily Job Tracker - {inserted_count} new jobs"
        print("6. Sending NEW jobs")
    else:
        jobs_for_email = fetch_top_matching_jobs(limit=20)
        subject = "Daily Job Tracker - Top current matches"
        print("6. No new jobs, sending top matches")

    csv_file = export_jobs_to_csv(jobs_for_email)
    print(f"7. CSV exported: {csv_file}")

    html_body = build_html_email(jobs_for_email)

    send_summary_email(subject, html_body)
    print("8. Email sent successfully")


if __name__ == "__main__":
    run_tracker()
