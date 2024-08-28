from ..database import db

class EmailSent(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    email_id = db.Column(db.String(36), nullable=False)
    recipient = db.Column(db.Text, nullable=False)
    batch_id = db.Column(db.String(36), nullable=False)
    status = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            'id': str(self.id),
            'email_id': self.email_id,
            'recipient': self.recipient,
            'batch_id': self.batch_id,
            'status': self.status,
        }