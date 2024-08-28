import pytest
from unittest.mock import patch

@patch('src.email_sent.router.get_email_sent')
def test_get_email_sent_no_filters(mock_get_email_sent, client):
    # Arrange
    mock_get_email_sent.return_value = [{
        'id': '1',
        'email_id': '1',
        'recipient': 'recipient@example.com',
        'batch_id': 'batch123',
        'status': 'sent'
    }]

    # Act
    response = client.get('/api/email_sent/get_email_sent')

    # Assert
    assert response.status_code == 200

    expected_data = [{
        'id': '1',
        'email_id': '1',
        'recipient': 'recipient@example.com',
        'batch_id': 'batch123',
        'status': 'sent'
    }]

    assert response.json == expected_data
    mock_get_email_sent.assert_called_once_with()

@patch('src.email_sent.router.get_email_sent')
def test_get_email_sent_with_filters(mock_get_email_sent, client):
    # Arrange
    mock_get_email_sent.return_value = [{
        'id': '2',
        'email_id': '1',
        'recipient': 'another@example.com',
        'batch_id': 'batch124',
        'status': 'failed'
    }]

    # Act
    response = client.get('/api/email_sent/get_email_sent?id=2&status=failed')

    # Assert
    assert response.status_code == 200

    expected_data = [{
        'id': '2',
        'email_id': '1',
        'recipient': 'another@example.com',
        'batch_id': 'batch124',
        'status': 'failed'
    }]

    assert response.json == expected_data
    mock_get_email_sent.assert_called_once_with(id='2', status='failed')