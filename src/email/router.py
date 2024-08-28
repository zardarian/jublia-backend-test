from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from .schemas import EmailSchema
from .queries import save_email, get_emails

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

@api.route('/get_emails')
class GetEmails(Resource):
    @api.expect(api.parser()
        .add_argument('event_id', type=int, required=False, help='Filter by event ID')
        .add_argument('email_subject', type=str, required=False, help='Filter by email subject')
        .add_argument('status', type=str, required=False, help='Filter by email status'))
    @api.response(200, 'Emails retrieved successfully')
    def get(self):
        # Parse query parameters
        args = request.args

        filters = {
            'event_id': args.get('event_id'),
            'email_subject': args.get('email_subject'),
            'status': args.get('status')
        }

        # Remove None values from filters
        filters = {k: v for k, v in filters.items() if v is not None}

        # Get the filtered emails
        emails = get_emails(**filters)

        return emails