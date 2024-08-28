import pytest
from unittest.mock import patch

@patch('src.email.router.save_email')
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

@patch('src.email.router.get_emails')
def test_get_emails_no_filters(mock_get_emails, client):
    # Arrange
    mock_get_emails.return_value = [{
        'id': '1',
        'event_id': 1,
        'email_subject': 'Test Subject',
        'email_content': 'Test Content',
        'timestamp': '2023-01-01T00:00:00',
        'status': 'pending'
    }]

    # Act
    response = client.get('/api/email/get_emails')

    # Assert
    assert response.status_code == 200
    expected_data = [{
        'id': '1',
        'event_id': 1,
        'email_subject': 'Test Subject',
        'email_content': 'Test Content',
        'timestamp': '2023-01-01T00:00:00',
        'status': 'pending'
    }]

    assert response.json == expected_data
    mock_get_emails.assert_called_once_with()

@patch('src.email.router.get_emails')
def test_get_emails_with_filters(mock_get_emails, client):
    # Arrange
    mock_get_emails.return_value = [{
        'id': '1',
        'event_id': 1,
        'email_subject': 'Test Subject',
        'email_content': 'Test Content',
        'timestamp': '2023-01-01T00:00:00',
        'status': 'pending'
    }]

    # Act
    response = client.get('/api/email/get_emails?event_id=1&status=pending')

    # Assert
    assert response.status_code == 200
    assert response.json == [{
        'id': '1',
        'event_id': 1,
        'email_subject': 'Test Subject',
        'email_content': 'Test Content',
        'timestamp': '2023-01-01T00:00:00',
        'status': 'pending'
    }]
    mock_get_emails.assert_called_once_with(event_id='1', status='pending')

@patch('src.email.router.get_emails')
def test_get_emails_empty_response(mock_get_emails, client):
    # Arrange
    mock_get_emails.return_value = []

    # Act
    response = client.get('/api/email/get_emails?status=sent')

    # Assert
    assert response.status_code == 200
    assert response.json == []
    mock_get_emails.assert_called_once_with(status='sent')