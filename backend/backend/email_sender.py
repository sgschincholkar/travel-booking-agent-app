import logging
import os

import markdown
import resend

logger = logging.getLogger(__name__)


def send_html_email(travel_html: str, sender: str, receiver: str, subject: str) -> str:
    """
    Uses Resend to send travel_html (markdown from the model) as the email
    body, rendered to HTML first so it displays correctly in email clients.
    Returns a status string. Raises on failure so callers see a real error
    instead of a success-shaped string.
    """
    resend.api_key = os.environ.get("RESEND_API_KEY")
    rendered_html = markdown.markdown(travel_html)
    try:
        result = resend.Emails.send(
            {
                "from": sender,
                "to": receiver,
                "subject": subject,
                "html": rendered_html,
            }
        )
    except Exception:
        logger.exception(
            "send_html_email failed: sender=%s receiver=%s subject=%s",
            sender, receiver, subject,
        )
        raise
    return f"Email sent (id {result.get('id')})"
