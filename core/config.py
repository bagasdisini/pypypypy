import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_HOST: str
    APP_PORT: int
    DATABASE_URL: str
    CORS_ALLOW_ORIGINS: str

    def __init__(self):
        self.APP_HOST = os.getenv('APP_HOST')
        self.APP_PORT = int(os.getenv('APP_PORT'))
        self.DATABASE_URL = os.getenv('DATABASE_URL')
        self.CORS_ALLOW_ORIGINS = os.getenv('CORS_ALLOW_ORIGINS')

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


config = Config()
