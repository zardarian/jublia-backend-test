from .models import db, Email
from sqlalchemy import func
import uuid

def save_email(event_id, email_subject, email_content, timestamp):
    email = Email(
        id=uuid.uuid4(),
        event_id=event_id,
        email_subject=email_subject,
        email_content=email_content,
        timestamp=timestamp,
        status='pending'
    )
    db.session.add(email)
    db.session.commit()

def get_emails_to_send(current_time):
    return Email.query.filter(Email.status == 'pending').filter(Email.timestamp <= current_time).all()

def update_emails_status(id, status):
    email = Email.query.filter_by(id=id).first()
    
    if email:
        email.status = status
        
        db.session.commit()
        return True
    else:
        return False
