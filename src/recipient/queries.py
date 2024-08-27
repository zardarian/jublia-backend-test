from .models import db, Recipient
import uuid

def get_all_recipients():
    return Recipient.query.all()
