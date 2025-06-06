import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")


class AppConfig:
    @staticmethod
    def get(name, default=None):
        return os.getenv(name, default)

    APP_NAME = get("APP_NAME", "QtApp")
    APP_VERSION = get("APP_VERSION", "1.0.0")
    UI_FILE = get("UI_FILE", "main_window.ui")

    DB_HOST = get("DB_HOST", "localhost")
    DB_PORT = get("DB_HOST", "5432")
    DB_NAME = get("DB_NAME", "bank_db")
    DB_USER = get("DB_USER", "postgres")
    DB_PASSWORD = get("DB_PASSWORD")

    @classmethod
    def validate(cls):
        if not all([cls.APP_NAME, cls.APP_VERSION, cls.UI_FILE, cls.DB_PASSWORD]):
            raise EnvironmentError("Missing required environment variables")
