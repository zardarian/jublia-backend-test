import pytest
from unittest.mock import patch
from flask import Flask
from flask_restx import Api
from src.email.router import api as email_router
from src.database import db

@pytest.fixture
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

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@patch('src.email.queries.save_email')
def test_save_emails_success(mock_save_email, client):
    # Arrange
    # Mock the return values
    mock_save_email.return_value = None

    payload = {
        "event_id": 1,
        "email_subject": "Test Subject",
        "email_content": "Test Content",
        "timestamp": "2023-01-01T00:00:00"
    }

    # Act
    response = client.post('/api/email/save_emails', json=payload)

    # Assert
    assert response.status_code == 201
    assert response.json == {"message": "Email saved successfully"}

def test_save_emails_validation_error(client):
    # Arrange
    payload = {
        "email_subject": "Test Subject",
        "email_content": "Test Content",
        "timestamp": "2023-01-01T00:00:00"
    }

    # Act
    response = client.post('/api/email/save_emails', json=payload)
    
    # Assert
    assert response.status_code == 400
    assert "event_id" in response.json
