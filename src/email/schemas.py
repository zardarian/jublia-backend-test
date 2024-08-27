from marshmallow import Schema, fields

class EmailSchema(Schema):
    event_id = fields.Int(required=True, description="ID of the event")
    email_subject = fields.Str(required=True, description="Subject of the email")
    email_content = fields.Str(required=True, description="Content of the email")
    timestamp = fields.DateTime(required=True, description="Timestamp when the email should be sent")
