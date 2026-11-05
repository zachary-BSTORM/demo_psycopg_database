import psycopg
from dotenv import load_dotenv
import os

load_dotenv()


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None

        return cls._instance

    @property
    def connection(self):
        if self._connection is None or self._connection.closed:
            self._connection = psycopg.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                autocommit=True,
            )

        return self._connection

    def close(self):
        if self._connection is not None and not self._connection.closed:
            self._connection.close()
            
        self._connection = None
