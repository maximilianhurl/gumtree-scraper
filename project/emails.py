from project.settings import MAILGUN_KEY, MAILGUN_URL, REPORT_EMAIL
import requests


def send_email(subject, message):
    response = requests.post(
        MAILGUN_URL,
        auth=("api", MAILGUN_KEY),
        data={
            "from": 'gumtreescraper@maxhurl.co.uk',
            "to": REPORT_EMAIL,
            "subject": subject,
            "text": message
        }
    )

    if response.status_code != 200:
        raise Exception(
            f"Unable to send email - Status: {response.status_code} Text: {response.text}"
        )
