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

def get_emails(**filters):
    query = Email.query

    if 'event_id' in filters:
        query = query.filter_by(event_id=filters['event_id'])

    if 'email_subject' in filters:
        query = query.filter(Email.email_subject.like(f"%{filters['email_subject']}%"))

    if 'status' in filters:
        query = query.filter_by(status=filters['status'])

    return [email.to_dict() for email in query.all()]