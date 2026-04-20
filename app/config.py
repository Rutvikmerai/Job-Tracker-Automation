import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
EMAIL_TO = os.getenv("EMAIL_TO", "")

JOB_KEYWORDS = [x.strip() for x in os.getenv("JOB_KEYWORDS", "").split(",") if x.strip()]
SKILL_KEYWORDS = [x.strip() for x in os.getenv("SKILL_KEYWORDS", "").split(",") if x.strip()]
LOCATION_KEYWORDS = [x.strip() for x in os.getenv("LOCATION_KEYWORDS", "").split(",") if x.strip()]
MIN_SCORE = float(os.getenv("MIN_SCORE", "5"))