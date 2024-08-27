from .models import db

def save_bulk_email_sent(email_sent):
    db.session.bulk_save_objects(email_sent)
    db.session.commit()
