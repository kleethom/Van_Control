import time
import datetime
from database.db import get_db

class Aggregator:
    def __init__(self):
        self._last_1min = 0
        self._last_1hour = 0
        self._last_1day = 0

    def aggregate(self):
        now = time.time()
        db = get_db()

        # --- 1-Minute Aggregation (alle 60s) ---
        if now - self._last_1min >= 60:
            self._aggregate_1min(db, now)
            self._last_1min = now

        # --- 1-Hour Aggregation (alle 3600s) ---
        if now - self._last_1hour >= 3600:
            self._aggregate_1hour(db, now)
            self._last_1hour = now

        # --- 1-Day Aggregation (alle 86400s) ---
        if now - self._last_1day >= 86400:
            self._aggregate_1day(db, now)
            self._last_1day = now

    def _aggregate_1min(self, db, now):
        ts = int(now) - 60
        cutoff = int(now) - 60
        db.execute("""
        INSERT OR REPLACE INTO sensor_1min (
            timestamp,
            temp_in_avg, temp_in_min, temp_in_max,
            hum_in_avg,
            temp_out_avg, temp_out_min, temp_out_max,
            hum_out_avg,
            altitude_avg
        )
        SELECT
                ? AS ts,
                AVG(temperature_inside),
                MIN(temperature_inside),
                MAX(temperature_inside),
                AVG(humidity_inside),
                AVG(temperature_outside),
                MIN(temperature_outside),
                MAX(temperature_outside),
                AVG(humidity_outside),
                AVG(altitude)
            FROM sensor_raw
            WHERE timestamp >= ?
        """, (ts, cutoff))
        db.commit()

    def _aggregate_1hour(self, db, now):
        ts = int(now) - 3600
        cutoff = int(now) - 3600
        db.execute("""
        INSERT OR REPLACE INTO sensor_1hour (
            timestamp,
            temp_in_avg, temp_in_min, temp_in_max,
            hum_in_avg,
            temp_out_avg, temp_out_min, temp_out_max,
            hum_out_avg,
            altitude_avg
        )
        SELECT
                ? AS ts,
                AVG(temp_in_avg),
                MIN(temp_in_min),
                MAX(temp_in_max),
                AVG(hum_in_avg),
                AVG(temp_out_avg),
                MIN(temp_out_min),
                MAX(temp_out_max),
                AVG(hum_out_avg),
                AVG(altitude_avg)
            FROM sensor_1min
            WHERE timestamp >= ?
        """, (ts, cutoff))
        db.commit()

    def _aggregate_1day(self, db, now):
        # Mitternacht des aktuellen Tages (lokale Zeit) als Unix-Timestamp
        today_midnight = datetime.datetime.combine(
            datetime.date.today(), datetime.time.min
        )
        day_ts = int(today_midnight.timestamp())
        cutoff = day_ts
        db.execute("""
        INSERT OR REPLACE INTO sensor_1day (
            date,
            temp_in_avg, temp_in_min, temp_in_max,
            hum_in_avg,
            temp_out_avg, temp_out_min, temp_out_max,
            hum_out_avg,
            altitude_avg
        )
        SELECT
                ? AS day_ts,
                AVG(temp_in_avg),
                MIN(temp_in_min),
                MAX(temp_in_max),
                AVG(hum_in_avg),
                AVG(temp_out_avg),
                MIN(temp_out_min),
                MAX(temp_out_max),
                AVG(hum_out_avg),
                AVG(altitude_avg)
            FROM sensor_1hour
            WHERE timestamp >= ?
        """, (day_ts, cutoff))
        db.commit()