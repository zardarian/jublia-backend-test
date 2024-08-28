from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from .schemas import RecipientSchema
from .queries import save_bulk_recipients, get_recipients

api = Namespace('recipient', description='Recipient related operations')

recipient_model = api.model('Recipient', {
    'emails': fields.List(fields.String, required=True, description='List of emails'),
})
@api.route('/save_recipients')
class SaveRecipients(Resource):
    @api.expect(recipient_model)
    @api.response(201, 'Recipients saved successfully')
    @api.response(400, 'Validation Error')
    def post(self):
        data = request.get_json()
        schema = RecipientSchema()
        errors = schema.validate(data)
        if errors:
            return errors, 400
        
        save_bulk_recipients(emails=data['emails'])
        return {"message": "Recipients saved successfully"}, 201

@api.route('/get_recipients')
class GetRecipients(Resource):
    @api.expect(api.parser()
        .add_argument('id', type=str, required=False, help='Filter by recipient id')
        .add_argument('email', type=str, required=False, help='Filter by recipient email'))
    @api.response(200, 'Recipients retrieved successfully')
    def get(self):
        args = request.args

        filters = {
            'id': args.get('id'),
            'email': args.get('email'),
        }

        filters = {k: v for k, v in filters.items() if v is not None}

        recipients = get_recipients(**filters)

        return recipients