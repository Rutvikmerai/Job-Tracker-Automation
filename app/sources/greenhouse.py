import requests
from datetime import datetime, UTC

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def fetch_greenhouse_jobs(board_token: str, company_name: str) -> list[dict]:
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    data = response.json()

    jobs = []
    now = datetime.now(UTC).isoformat()

    for item in data.get("jobs", []):
        location = item.get("location", {})
        location_name = location.get("name") if isinstance(location, dict) else None

        absolute_url = item.get("absolute_url")
        title = (item.get("title") or "").strip()

        if not absolute_url or not title:
            continue

        jobs.append({
            "source": "Greenhouse",
            "source_company": company_name,
            "external_job_id": str(item.get("id", "")),
            "title": title,
            "company": company_name,
            "location": location_name,
            "remote_type": None,
            "department": None,
            "employment_type": None,
            "description": "",
            "posted_date": None,
            "url": absolute_url,
            "first_seen_at": now,
            "last_seen_at": now,
        })

    return jobs