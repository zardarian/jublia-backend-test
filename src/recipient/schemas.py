from marshmallow import Schema, fields

class RecipientSchema(Schema):
    emails = fields.List(fields.Str(), required=True, description="List of email addresses")
