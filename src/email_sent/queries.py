from .models import db, EmailSent

def save_bulk_email_sent(email_sent):
    db.session.bulk_save_objects(email_sent)
    db.session.commit()

def get_email_sent(**filters):
    query = EmailSent.query

    if 'id' in filters:
        query = query.filter_by(id=filters['id'])

    if 'email_id' in filters:
        query = query.filter_by(email_id=filters['email_id'])

    if 'recipient' in filters:
        query = query.filter(EmailSent.recipient.like(f"%{filters['recipient']}%"))

    if 'batch_id' in filters:
        query = query.filter_by(batch_id=filters['batch_id'])

    if 'status' in filters:
        query = query.filter_by(status=filters['status'])

    return [recipient.to_dict() for recipient in query.all()]