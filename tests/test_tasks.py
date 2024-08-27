
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from unittest.mock import patch, MagicMock, call
from src.celery_worker import check_emails_to_be_delivered, send_emails_task, send_email
from datetime import datetime
from freezegun import freeze_time
import uuid

def test_send_email():
    subject = "Test Subject"
    body = "Test Content"
    recipients = ["recipient@example"] * 20
    send_email(subject, body, recipients)
    
    assert True

@freeze_time("2024-08-27 22:22:53")
@patch('src.celery_worker.get_emails_to_send')
@patch('src.celery_worker.get_all_recipients')
@patch('src.celery_worker.send_email')
@patch('src.celery_worker.save_bulk_email_sent')
def test_check_emails_to_be_delivered(mock_save_bulk_email_sent, mock_send_email, mock_get_all_recipients, mock_get_emails_to_send):
    # Arrange
    # Mock the return values
    mock_email = MagicMock()
    mock_email.id = uuid.uuid4()
    mock_email.email_subject = "Test Subject"
    mock_email.email_content = "Test Content"
    mock_get_emails_to_send.return_value = [mock_email]

    mock_recipient = MagicMock()
    mock_recipient.email = "recipient@example.com"
    mock_get_all_recipients.return_value = [mock_recipient] * 20

    mock_send_email.return_value = True

    # Act
    check_emails_to_be_delivered()

    # Assert
    mock_get_emails_to_send.assert_called_once_with(datetime.now())
    mock_get_all_recipients.assert_called_once()

    # Ensure send_email & bulk_email called based on recipients chunks
    assert mock_send_email.call_count == 2
    assert mock_save_bulk_email_sent.call_count == 2

    # Check the arguments passed to save_bulk_email_sent to ensure correct payload was created
    args, kwargs = mock_save_bulk_email_sent.call_args
    email_sent_list = args[0]
    assert len(email_sent_list) == 10
    for email_sent in email_sent_list:
        assert email_sent.status == 'sent'
        assert email_sent.email_id == mock_email.id

@freeze_time("2024-08-27 22:22:53")
@patch('src.celery_worker.get_emails_to_send')
@patch('src.celery_worker.get_all_recipients')
@patch('src.celery_worker.send_email')
@patch('src.celery_worker.save_bulk_email_sent')
def test_check_emails_to_be_delivered_with_failed_send_email(mock_save_bulk_email_sent, mock_send_email, mock_get_all_recipients, mock_get_emails_to_send):
    # Arrange
    # Mock the return values
    mock_email = MagicMock()
    mock_email.id = uuid.uuid4()
    mock_email.email_subject = "Test Subject"
    mock_email.email_content = "Test Content"
    mock_get_emails_to_send.return_value = [mock_email]

    mock_recipient = MagicMock()
    mock_recipient.email = "recipient@example.com"
    mock_get_all_recipients.return_value = [mock_recipient] * 20

    mock_send_email.return_value = False

    # Act
    check_emails_to_be_delivered()

    # Assert
    mock_get_emails_to_send.assert_called_once_with(datetime.now())
    mock_get_all_recipients.assert_called_once()

    # Ensure send_email & bulk_email called based on recipients chunks
    assert mock_send_email.call_count == 2
    assert mock_save_bulk_email_sent.call_count == 2

    # Check the arguments passed to save_bulk_email_sent to ensure correct payload was created
    args, kwargs = mock_save_bulk_email_sent.call_args
    email_sent_list = args[0]
    assert len(email_sent_list) == 10
    for email_sent in email_sent_list:
        assert email_sent.status == 'failed'
        assert email_sent.email_id == mock_email.id

@patch('src.celery_worker.check_emails_to_be_delivered')
def test_send_emails_task(mock_check_emails_to_be_delivered):
    send_emails_task()
