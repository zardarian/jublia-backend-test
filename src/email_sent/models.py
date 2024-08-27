from ..database import db

class EmailSent(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    email_id = db.Column(db.String(36), nullable=False)
    recipient = db.Column(db.Text, nullable=False)
    batch_id = db.Column(db.String(36), nullable=False)
    status = db.Column(db.String(200), nullable=False)
