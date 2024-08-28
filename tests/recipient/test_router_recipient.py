import pytest
from unittest.mock import patch

@patch('src.recipient.router.save_bulk_recipients')
def test_save_recipients_success(mock_save_bulk_recipients, client):
    # Arrange
    mock_save_bulk_recipients.return_value = None

    payload = {
        "emails": ["test1@example.com", "test2@example.com"]
    }

    # Act
    response = client.post('/api/recipient/save_recipients', json=payload)

    # Assert
    assert response.status_code == 201

    expected_data = {"message": "Recipients saved successfully"}
    assert response.json == expected_data

    mock_save_bulk_recipients.assert_called_once_with(emails=payload['emails'])


@patch('src.recipient.router.save_bulk_recipients')
def test_save_recipients_validation_error(mock_save_bulk_recipients, client):
    # Arrange
    payload = {
        "emails": "invalid_email"
    }

    # Act
    response = client.post('/api/recipient/save_recipients', json=payload)

    # Assert
    assert response.status_code == 400

    
    mock_save_bulk_recipients.assert_not_called()

@patch('src.recipient.router.get_recipients')
def test_get_recipients_no_filters(mock_get_recipients, client):
    # Arrange
    mock_get_recipients.return_value = [{
        'id': '1',
        'email': 'test1@example.com'
    }, {
        'id': '2',
        'email': 'test2@example.com'
    }]

    # Act
    response = client.get('/api/recipient/get_recipients')

    # Assert
    assert response.status_code == 200

    expected_data = [{
        'id': '1',
        'email': 'test1@example.com'
    }, {
        'id': '2',
        'email': 'test2@example.com'
    }]
    assert response.json == expected_data

    mock_get_recipients.assert_called_once_with()


@patch('src.recipient.router.get_recipients')
def test_get_recipients_with_filters(mock_get_recipients, client):
    # Arrange
    mock_get_recipients.return_value = [{
        'id': '1',
        'email': 'test1@example.com'
    }]

    # Act
    response = client.get('/api/recipient/get_recipients?id=1')

    # Assert
    assert response.status_code == 200

    expected_data = [{
        'id': '1',
        'email': 'test1@example.com'
    }]
    assert response.json == expected_data

    mock_get_recipients.assert_called_once_with(id='1')
