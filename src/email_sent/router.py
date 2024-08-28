from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from .queries import get_email_sent

api = Namespace('email_sent', description='Email Sent related operations')

@api.route('/get_email_sent')
class GetEmailSent(Resource):
    @api.expect(api.parser()
        .add_argument('id', type=str, required=False, help='Filter by email sent id')
        .add_argument('email_id', type=str, required=False, help='Filter by email sent email id')
        .add_argument('recipient', type=str, required=False, help='Filter by email sent recipient')
        .add_argument('batch_id', type=str, required=False, help='Filter by email sent batch id')
        .add_argument('status', type=str, required=False, help='Filter by email sent status'))
    @api.response(200, 'Email Sent retrieved successfully')
    def get(self):
        args = request.args

        filters = {
            'id': args.get('id'),
            'email_id': args.get('email_id'),
            'recipient': args.get('recipient'),
            'batch_id': args.get('batch_id'),
            'status': args.get('status'),
        }

        filters = {k: v for k, v in filters.items() if v is not None}

        email_sent = get_email_sent(**filters)

        return email_sent