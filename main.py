from flask import Flask
from flask_restx import Api
from src.email.router import api as email_router
from src.recipient.router import api as recipient_router
from src.database import init_db
from src.celery_config import make_celery
from dotenv import load_dotenv
from src.config import Config
import os


load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    init_db(app)

    # Initialize Flask-RESTX API
    api = Api(app, version='1.0', title='Email API', description='A simple Email API')

    # Register routers
    api.add_namespace(email_router, path='/api/email')
    api.add_namespace(recipient_router, path='/api/recipient')

    return app

# Initialize app & celery
app = create_app()
celery = make_celery(app)

if __name__ == "__main__":
    app.run(debug=True)
