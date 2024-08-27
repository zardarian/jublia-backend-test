import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_pre_ping': True
    }
    broker_url  = os.getenv('CELERY_BROKER_URL')
    result_backend = os.getenv('CELERY_RESULT_BACKEND')

settings = Config()