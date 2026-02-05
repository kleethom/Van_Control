import sqlite3
from config.config import DB_PATH

_connection = None

def get_db():
    global _connection
    if _connection is None:
        _connection = sqlite3.connect(
            DB_PATH,
            check_same_thread=False
        )
        _connection.row_factory = sqlite3.Row
        _connection.execute("PRAGMA journal_mode=WAL;")
        _connection.execute("PRAGMA foreign_keys=ON;")
    return _connection