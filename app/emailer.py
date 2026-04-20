import smtplib
from email.message import EmailMessage

from app.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, EMAIL_TO


def build_html_email(jobs: list[dict]) -> str:
    if not jobs:
        return """
        <html>
          <body>
            <h3>No new matching jobs found today.</h3>
          </body>
        </html>
        """

    rows = []
    for job in jobs:
        rows.append(f"""
        <tr>
            <td><a href="{job['url']}">{job['title']}</a></td>
            <td>{job.get('company', 'Unknown')}</td>
            <td>{job.get('location', 'Unknown')}</td>
            <td>{job.get('score', 0)}</td>
            <td>{job.get('matched_keywords', '')}</td>
        </tr>
        """)

    return f"""
    <html>
      <body>
        <h2>Daily Job Tracker Summary</h2>
        <p>Found {len(jobs)} new matching job(s).</p>
        <table border="1" cellpadding="6" cellspacing="0">
          <tr>
            <th>Title</th>
            <th>Company</th>
            <th>Location</th>
            <th>Score</th>
            <th>Matches</th>
          </tr>
          {''.join(rows)}
        </table>
      </body>
    </html>
    """


def send_summary_email(subject: str, html_body: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_TO
    msg.set_content("Your email client does not support HTML.")
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)