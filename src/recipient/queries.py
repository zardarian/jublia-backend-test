from .models import db, Recipient
import uuid

def save_bulk_recipients(emails):
    payload_recipients = []
    for email in emails:
        payload = Recipient(
            id = uuid.uuid4(),
            email = email
        )
        payload_recipients.append(payload)

    db.session.bulk_save_objects(payload_recipients)
    db.session.commit()

def get_all_recipients():
    return Recipient.query.all()
