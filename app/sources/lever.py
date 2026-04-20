import requests
from datetime import datetime, UTC

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def fetch_lever_jobs(company_slug: str, company_name: str) -> list[dict]:
    url = f"https://api.lever.co/v0/postings/{company_slug}?mode=json"
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    data = response.json()

    jobs = []
    now = datetime.now(UTC).isoformat()

    for item in data:
        categories = item.get("categories", {}) or {}

        hosted_url = item.get("hostedUrl")
        title = (item.get("text") or "").strip()

        if not hosted_url or not title:
            continue

        jobs.append({
            "source": "Lever",
            "source_company": company_name,
            "external_job_id": item.get("id", ""),
            "title": title,
            "company": company_name,
            "location": categories.get("location"),
            "remote_type": None,
            "department": categories.get("team"),
            "employment_type": categories.get("commitment"),
            "description": item.get("descriptionPlain", "") or "",
            "posted_date": None,
            "url": hosted_url,
            "first_seen_at": now,
            "last_seen_at": now,
        })

    return jobs