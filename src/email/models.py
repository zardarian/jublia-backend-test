from ..database import db

class Email(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    event_id = db.Column(db.Integer, nullable=False)
    email_subject = db.Column(db.String(255), nullable=False)
    email_content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(200), nullable=True)
