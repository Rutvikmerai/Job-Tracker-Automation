import logging

from app.sources.greenhouse import fetch_greenhouse_jobs


def collect_all_jobs() -> list[dict]:
    all_jobs: list[dict] = []

    greenhouse_sources = [
        {"board_token": "airtable", "company_name": "Airtable"},
        {"board_token": "discord", "company_name": "Discord"},
        {"board_token": "coinbase", "company_name": "Coinbase"},
        {"board_token": "robinhood", "company_name": "Robinhood"},
        {"board_token": "brex", "company_name": "Brex"},
    ]
    

    for source in greenhouse_sources:
        try:
            jobs = fetch_greenhouse_jobs(
                board_token=source["board_token"],
                company_name=source["company_name"]
            )

            all_jobs.extend(jobs)

            print(f"Greenhouse returned {len(jobs)} jobs for {source['company_name']}")
            logging.info(
                "Collected %s jobs from %s",
                len(jobs),
                source["company_name"]
            )

        except Exception as e:
            print(f"Failed for {source['company_name']}: {e}")
            logging.exception(
                "Error collecting jobs from %s: %s",
                source["company_name"],
                e
            )
            continue

    return all_jobs