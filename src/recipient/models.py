from ..database import db

class Recipient(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'id': str(self.id),
            'email': self.email,
        }