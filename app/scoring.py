from app.config import JOB_KEYWORDS, SKILL_KEYWORDS, LOCATION_KEYWORDS

REJECT_TERMS = [
    "account executive",
    "sales",
    "recruiter",
    "attorney",
    "designer",
    "marketing",
    "customer support",
    "partnerships",
    "software engineer",
    "frontend",
    "backend",
    "full stack",
    "devops",
    "site reliability",
    "sre",
    "product manager",
]

SENIOR_TERMS = [
    "senior",
    "staff",
    "principal",
    "director",
    "manager",
    "lead",
    "head of",
    "vp",
    "vice president",
]

ENTRY_LEVEL_TERMS = [
    "intern",
    "internship",
    "entry level",
    "entry-level",
    "junior",
    "new grad",
    "new graduate",
    "campus",
    "early career",
    "associate",
    "analyst i",
    "analyst 1",
    "apprentice",
    "trainee",
]

ANALYST_TITLE_TERMS = [
    "data analyst",
    "business analyst",
    "bi analyst",
    "reporting analyst",
    "business intelligence analyst",
    "analytics analyst",
    "product analyst",
    "operations analyst",
]

US_POSITIVE_TERMS = [
    "united states",
    "usa",
    "us",
    "u.s.",
    "remote",
    "new york",
    "california",
    "texas",
    "florida",
    "illinois",
    "ohio",
    "washington",
    "massachusetts",
    "georgia",
    "north carolina",
    "virginia",
    "pennsylvania",
    "michigan",
    "colorado",
    "arizona",
    "new jersey",
]

NON_US_TERMS = [
    "canada",
    "toronto",
    "vancouver",
    "ontario",
    "montreal",
    "india",
    "bengaluru",
    "bangalore",
    "hyderabad",
    "mumbai",
    "pune",
    "germany",
    "berlin",
    "munich",
    "france",
    "paris",
    "ireland",
    "dublin",
    "brazil",
    "sao paulo",
    "mexico",
    "uk",
    "united kingdom",
    "london",
    "singapore",
    "japan",
    "tokyo",
    "australia",
    "sydney",
    "poland",
    "luxembourg",
    "spain",
    "netherlands",
]

TOO_SENIOR_DESCRIPTION_TERMS = [
    "7+ years",
    "8+ years",
    "10+ years",
    "12+ years",
    "15+ years",
    "extensive experience",
]


def score_job(job: dict) -> tuple[float, list[str]]:
    title = (job.get("title") or "").lower()
    description = (job.get("description") or "").lower()
    location = (job.get("location") or "").lower()

    score = 0
    matches: list[str] = []

    # Hard reject bad functions
    if any(term in title for term in REJECT_TERMS):
        return -100.0, ["rejected:irrelevant-title"]

    # Hard reject all clearly non-US locations
    if any(term in location for term in NON_US_TERMS):
        return -100.0, ["rejected:non-us"]

    # Hard reject missing location
    if not location.strip():
        return -100.0, ["rejected:missing-location"]

    # Must contain some US signal
    if not any(term in location for term in US_POSITIVE_TERMS):
        return -100.0, ["rejected:not-us-location"]

    # Strong title targeting
    title_match = False
    for term in ANALYST_TITLE_TERMS:
        if term in title:
            score += 20
            matches.append(f"title:{term}")
            title_match = True

    for kw in JOB_KEYWORDS:
        kw_lower = kw.lower()
        if kw_lower in title:
            score += 10
            matches.append(f"title_kw:{kw}")
            title_match = True
        elif kw_lower in description:
            score += 3
            matches.append(f"description_kw:{kw}")

    if not title_match:
        return -80.0, ["rejected:no-analyst-title-match"]

    # Entry-level / internship required
    entry_match = False
    for term in ENTRY_LEVEL_TERMS:
        if term in title:
            score += 18
            matches.append(f"entry_title:{term}")
            entry_match = True
        elif term in description:
            score += 8
            matches.append(f"entry_desc:{term}")
            entry_match = True

    if not entry_match:
        score -= 10
        matches.append("penalty:not-entry-level")

    # Reject senior titles
    if any(term in title for term in SENIOR_TERMS):
        return -100.0, ["rejected:senior-title"]

    if any(term in description for term in TOO_SENIOR_DESCRIPTION_TERMS):
        score -= 15
        matches.append("penalty:high-experience")

    for kw in SKILL_KEYWORDS:
        kw_lower = kw.lower()
        if kw_lower in description:
            score += 4
            matches.append(f"skill:{kw}")

    for kw in LOCATION_KEYWORDS:
        kw_lower = kw.lower()
        if kw_lower in location:
            score += 2
            matches.append(f"location_kw:{kw}")

    return float(score), matches