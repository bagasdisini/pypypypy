import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.APP_HOST = os.getenv('APP_HOST')
            self.APP_PORT = int(os.getenv('APP_PORT'))
            self.DATABASE_URL = os.getenv('DATABASE_URL')
            self.CORS_ALLOW_ORIGINS = os.getenv('CORS_ALLOW_ORIGINS')
            self.AUTH_JWT_KEY = os.getenv('AUTH_JWT_KEY')
            self.AUTH_JWT_EXPIRE = int(os.getenv('AUTH_JWT_EXPIRE'))
            self.MIDTRANS_SERVER_KEY = os.getenv('MIDTRANS_SERVER_KEY')
            self.MIDTRANS_CLIENT_KEY = os.getenv('MIDTRANS_CLIENT_KEY')

            self.RABBITMQ_USER = os.getenv('RABBITMQ_USER')
            self.RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
            self.RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
            self.RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT'))
            self.RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST')
            self.RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE')

            self._validate()

    def _validate(self):
        if not self.APP_HOST:
            raise ValueError("APP_HOST is not set or is empty")
        if not self.APP_PORT:
            raise ValueError("APP_PORT is not set or is empty")
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is not set or is empty")
        if not self.CORS_ALLOW_ORIGINS:
            raise ValueError("CORS_ALLOW_ORIGINS is not set or is empty")
        if not self.AUTH_JWT_KEY:
            raise ValueError("AUTH_JWT_KEY is not set or is empty")
        if not self.AUTH_JWT_EXPIRE:
            raise ValueError("AUTH_JWT_EXPIRE is not set or is empty")
        if not self.MIDTRANS_SERVER_KEY:
            raise ValueError("MIDTRANS_SERVER_KEY is not set or is empty")
        if not self.MIDTRANS_CLIENT_KEY:
            raise ValueError("MIDTRANS_CLIENT_KEY is not set or is empty")
        if not self.RABBITMQ_USER:
            raise ValueError("RABBITMQ_USER is not set or is empty")
        if not self.RABBITMQ_PASSWORD:
            raise ValueError("RABBITMQ_PASSWORD is not set or is empty")
        if not self.RABBITMQ_HOST:
            raise ValueError("RABBITMQ_HOST is not set or is empty")
        if not self.RABBITMQ_PORT:
            raise ValueError("RABBITMQ_PORT is not set or is empty")
        if not self.RABBITMQ_VHOST:
            raise ValueError("RABBITMQ_VHOST is not set or is empty")
        if not self.RABBITMQ_QUEUE:
            raise ValueError("RABBITMQ_QUEUE is not set or is empty")


config = Config()


CONST_CACHE_DURATION = 60 # seconds
CONST_JWT_ALGORITHM = "HS256"
CONST_MIDTRANS_API = "https://app.sandbox.midtrans.com/snap/v1/transactions"