import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_HOST: str
    APP_PORT: int
    DATABASE_URL: str
    CORS_ALLOW_ORIGINS: str
    AUTH_JWT_KEY: str
    AUTH_JWT_EXPIRE: int
    MIDTRANS_SERVER_KEY: str

    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_VHOST: str
    RABBITMQ_QUEUE: str

    def __init__(self):
        self.APP_HOST = os.getenv('APP_HOST')
        self.APP_PORT = int(os.getenv('APP_PORT'))
        self.DATABASE_URL = os.getenv('DATABASE_URL')
        self.CORS_ALLOW_ORIGINS = os.getenv('CORS_ALLOW_ORIGINS')
        self.AUTH_JWT_KEY = os.getenv('AUTH_JWT_KEY')
        self.AUTH_JWT_EXPIRE = int(os.getenv('AUTH_JWT_EXPIRE'))
        self.MIDTRANS_SERVER_KEY = os.getenv('MIDTRANS_SERVER_KEY')

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