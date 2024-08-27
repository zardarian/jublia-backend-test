import pytest
from unittest.mock import patch, MagicMock
from flask_sqlalchemy import SQLAlchemy

print("Applying global mocks...")

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
