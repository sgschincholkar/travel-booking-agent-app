import logging
import os

import resend

logger = logging.getLogger(__name__)


def send_html_email(travel_html: str, sender: str, receiver: str, subject: str) -> str:
    """
    Uses Resend to send travel_html as the email body.
    Returns a status string. Raises on failure so callers see a real error
    instead of a success-shaped string.
    """
    resend.api_key = os.environ.get("RESEND_API_KEY")
    try:
        result = resend.Emails.send(
            {
                "from": sender,
                "to": receiver,
                "subject": subject,
                "html": travel_html,
            }
        )
    except Exception:
        logger.exception(
            "send_html_email failed: sender=%s receiver=%s subject=%s",
            sender, receiver, subject,
        )
        raise
    return f"Email sent (id {result.get('id')})"
