import sqlite3
import threading
from config.config import DB_PATH

_connection = None
_lock = threading.Lock()

def get_db():
    global _connection
    if _connection is None:
        with _lock:
            # Doppelt prüfen nach dem Lock
            if _connection is None:
                _connection = sqlite3.connect(
                    DB_PATH,
                    check_same_thread=False
                )
                _connection.row_factory = sqlite3.Row
                _connection.execute("PRAGMA journal_mode=WAL;")
                _connection.execute("PRAGMA foreign_keys=ON;")
                # Timeout bei konkurrierenden Writes
                _connection.execute("PRAGMA busy_timeout=3000;")
    return _connection

def execute_safe(query, params=()):
    """Thread-sicheres Execute """
    with _lock:
        db = get_db()
        cursor = db.execute(query, params)
        db.commit()
        return cursor