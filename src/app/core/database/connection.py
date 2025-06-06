import psycopg2
from psycopg2 import OperationalError, InterfaceError
from app.core.config import AppConfig
from typing import Optional


class DatabaseConnection:
    _instance: Optional["DatabaseConnection"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._instance._connect()
            except Exception as e:
                cls._instance = None
                raise
        return cls._instance

    def _connect(self):
        conn_params = {
            "host": AppConfig.get("DB_HOST"),
            "port": AppConfig.get("DB_PORT"),
            "dbname": AppConfig.get("DB_NAME"),
            "user": AppConfig.get("DB_USER"),
            "password": AppConfig.get("DB_PASSWORD"),
            "connect_timeout": 5,
        }

        conn_params = {k: v for k, v in conn_params.items() if v is not None}

        try:
            self.connection = psycopg2.connect(**conn_params)
            self.connection.autocommit = False
            print("✅ Connection to DB sucess")
        except OperationalError as e:
            print(f"❌ Error of connection to DB: {e}")
            raise

    def get_cursor(self):
        try:
            if not hasattr(self, "connection") or self.connection.closed:
                self._connect()
            return self.connection.cursor()
        except InterfaceError:
            self._connect()
            return self.connection.cursor()

    def close(self):
        if hasattr(self, "connection") and not self.connection.closed:
            self.connection.close()
            print("🔌 Connection to DB closed")

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_type is not None:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.close()
