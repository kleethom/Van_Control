import time
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
            self._aggregate_1min(db)
            self._last_1min = now

        # --- 1-Hour Aggregation (alle 3600s) ---
        if now - self._last_1hour >= 3600:
            self._aggregate_1hour(db)
            self._last_1hour = now

        # --- 1-Day Aggregation (alle 86400s) ---
        if now - self._last_1day >= 86400:
            self._aggregate_1day(db)
            self._last_1day = now

    def _aggregate_1min(self, db):
        query = """
        INSERT OR REPLACE INTO sensor_1min (
            timestamp,
            temp_in_avg, temp_in_min, temp_in_max,
            hum_in_avg,
            temp_out_avg, temp_out_min, temp_out_max,
            hum_out_avg,
            altitude_avg
        )
        SELECT
            strftime('%s','now','-1 minute') AS ts,

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
        WHERE timestamp >= strftime('%s','now','-1 minute');
        """
        db.execute(query)
        db.commit()

    def _aggregate_1hour(self, db):
        query = """
        INSERT OR REPLACE INTO sensor_1hour (
            timestamp,
            temp_in_avg, temp_in_min, temp_in_max,
            hum_in_avg,
            temp_out_avg, temp_out_min, temp_out_max,
            hum_out_avg,
            altitude_avg
        )
        SELECT
            strftime('%s','now','-1 hour') AS ts,

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
        WHERE timestamp >= strftime('%s','now','-1 hour');
        """
        db.execute(query)
        db.commit()

    def _aggregate_1day(self, db):
        query = """
        INSERT OR REPLACE INTO sensor_1day (
            date,
            temp_in_avg, temp_in_min, temp_in_max,
            hum_in_avg,
            temp_out_avg, temp_out_min, temp_out_max,
            hum_out_avg,
            altitude_avg
        )
        SELECT
            strftime('%s','now','start of day') AS day_ts,

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
        WHERE timestamp >= strftime('%s','now','start of day');
        """
        db.execute(query)
        db.commit()