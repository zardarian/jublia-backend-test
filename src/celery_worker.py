from src.database import db
from src.email.models import Email
from src.recipient.models import Recipient
from src.email_sent.models import EmailSent
from src.email.queries import get_emails_to_send
from src.recipient.queries import get_all_recipients
from src.email_sent.queries import save_bulk_email_sent
from datetime import datetime
from main import app, celery
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_email(subject, body, recipients):
    print(f"Sending email to {recipients} with subject '{subject}'.")
    return True

def chunk_recipients(recipients, chunk_size):
    for i in range(0, len(recipients), chunk_size):
        yield recipients[i:i + chunk_size]

def check_emails_to_be_delivered():
    logger.info("Task started...")
    emails = get_emails_to_send(datetime.now())
    for email in emails:
        recipients = get_all_recipients()
        recipients_email = [recipient.email for recipient in recipients]

        for batch_recipients in chunk_recipients(recipients_email, 10):
            email_sent = []
            batch_id = uuid.uuid4()
            send_email_status = send_email(email.email_subject, email.email_content, batch_recipients)
            if send_email_status:
                for batch_recipient in batch_recipients:
                    payload_email_sent = EmailSent(
                        id = uuid.uuid4(),
                        email_id = email.id,
                        recipient = batch_recipient,
                        batch_id = batch_id,
                        status = 'sent'
                    )
                    email_sent.append(payload_email_sent)
            else:
                for batch_recipient in batch_recipients:
                    payload_email_sent = EmailSent(
                        id = uuid.uuid4(),
                        email_id = email.id,
                        recipient = batch_recipient,
                        batch_id = batch_id,
                        status = 'failed'
                    )
                    email_sent.append(payload_email_sent)
            save_bulk_email_sent(email_sent)

@celery.task(name='send_emails_task')
def send_emails_task():
    with app.app_context():
        check_emails_to_be_delivered()
