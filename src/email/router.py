from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from .schemas import EmailSchema
from .queries import save_email

api = Namespace('email', description='Email related operations')

email_model = api.model('Email', {
    'event_id': fields.Integer(required=True, description='ID of the event'),
    'email_subject': fields.String(required=True, description='Subject of the email'),
    'email_content': fields.String(required=True, description='Content of the email'),
    'timestamp': fields.DateTime(required=True, description='Timestamp when the email should be sent')
})
@api.route('/save_emails')
class SaveEmails(Resource):
    @api.expect(email_model)
    @api.response(201, 'Email saved successfully')
    @api.response(400, 'Validation Error')
    def post(self):
        data = request.get_json()
        schema = EmailSchema()
        errors = schema.validate(data)
        if errors:
            return errors, 400
        
        save_email(
            event_id=data['event_id'],
            email_subject=data['email_subject'],
            email_content=data['email_content'],
            timestamp=data['timestamp']
        )
        return {"message": "Email saved successfully"}, 201
