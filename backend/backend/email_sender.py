import os

import resend


def send_html_email(travel_html: str, sender: str, receiver: str, subject: str) -> str:
    """
    Uses Resend to send travel_html as the email body.
    Returns a status string.
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
        return f"Email sent (id {result.get('id')})"
    except Exception as e:
        return f"Error sending email: {e}"
