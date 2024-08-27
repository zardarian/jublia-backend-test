from .models import db, Email
from sqlalchemy import func
import uuid

def save_email(event_id, email_subject, email_content, timestamp):
    email = Email(
        id=uuid.uuid4(),
        event_id=event_id,
        email_subject=email_subject,
        email_content=email_content,
        timestamp=timestamp
    )
    db.session.add(email)
    db.session.commit()

def get_emails_to_send(current_time):
    truncated_current_time = func.date_trunc('minute', current_time)
    return Email.query.filter(func.date_trunc('minute', Email.timestamp) == truncated_current_time).all()
