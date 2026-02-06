from database.db import get_db
from datetime import datetime, timedelta, timezone
import time

class HistoryProvider:
    
    @staticmethod
    def get_day(sensor_field, date: datetime):
        start_ts = int(date.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
        end_ts = int((date + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()) - 1

        db = get_db()
        return db.execute(
            f"""
            SELECT timestamp, {sensor_field}
            FROM sensor_1min
            WHERE timestamp >= ? AND timestamp <= ?
            ORDER BY timestamp
            """,
            (start_ts, end_ts)
        ).fetchall()

    @staticmethod
    def get_week(sensor_field):
        since = int(time.time()) - 7*24*3600
        db = get_db()
        return db.execute(
            f"""
            SELECT timestamp, {sensor_field}
            FROM sensor_1hour
            WHERE timestamp >= ?
            ORDER BY timestamp
            """,
            (since,)
        ).fetchall()

    @staticmethod
    def get_month(sensor_field):
        since = int(time.time()) - 30*24*3600
        db = get_db()
        return db.execute(
            f"""
            SELECT date, {sensor_field}
            FROM sensor_1day
            WHERE date >= ?
            ORDER BY date
            """,
            (since,)
        ).fetchall()