import csv
from pathlib import Path
from datetime import datetime


def export_jobs_to_csv(jobs: list[dict]) -> str:
    Path("data").mkdir(exist_ok=True)
    filename = f"data/jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    if not jobs:
        # still create an empty CSV with no rows? not possible without columns
        # so just return the filename for consistency
        return filename

    fieldnames = list(jobs[0].keys())

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)

    return filename