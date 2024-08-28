import pytest
from unittest.mock import patch, MagicMock
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restx import Api
from src.database import db
from src.email.router import api as email_router
from src.email_sent.router import api as email_sent_router
from src.recipient.router import api as recipient_router

print("Applying global mocks...")

@pytest.fixture(autouse=True)
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # Initialize the database
    db.init_app(app)

    # Initialize Flask-RESTX API
    api = Api(app, version='1.0', title='Email API', description='A simple Email API')

    # Register routers
    api.add_namespace(email_router, path='/api/email')
    api.add_namespace(recipient_router, path='/api/recipient')
    api.add_namespace(email_sent_router, path='/api/email_sent')

    yield app

@pytest.fixture(autouse=True)
def client(app):
    return app.test_client()

# Mock the SQLAlchemy instance globally
@pytest.fixture(autouse=True)
def mock_sqlalchemy():
    with patch('src.database.db', new=MagicMock(spec=SQLAlchemy)) as mock_db:
        yield mock_db

# Mock the database session globally
@pytest.fixture(autouse=True)
def mock_db_session():
    with patch("src.database.db.session") as mock_session:
        print("Mocking session:", mock_session)
        yield mock_session.return_value

# Mock the database create all globally
@pytest.fixture(autouse=True)
def mock_db_create_all():
    with patch('src.database.db.create_all') as mock_create_all:
        yield mock_create_all
