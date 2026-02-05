import time
from database.db import get_db

class SensorLogger:
    def log(self, state):
        db = get_db()
        db.execute("""
            INSERT OR REPLACE INTO sensor_raw VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            int(time.time()),
            state.temperature_inside,
            state.humidity_inside,
            state.temperature_outside,
            state.humidity_outside,
            state.pressure,
            state.altitude,
            state.tilt_x,
            state.tilt_y
        ))
        db.commit()