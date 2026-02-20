import time
from database.db import get_db

class SensorLogger:
    def __init__(self, system_logger=None):
        self.sys_logger = system_logger

    def log(self, state):
        """Speichert die aktuellen Sensor-Rohdaten"""
        try:
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

        except Exception as e:
            
            method = getattr(self.sys_logger, "log_error", None)
            if method:
                method("SENSOR_LOGGER", f"DB-Fehler: {e}")
            else:
                print(f"Backup-Print (Kein Logger aktiv): {e}")

class SystemLogger:
    """Speichert Fehlermeldungen und Systemereignisse"""
    def log(self, level, module, message):
        try:
            db = get_db()
            db.execute("""
                INSERT INTO system_logs (timestamp, level, module, message)
                VALUES (?, ?, ?, ?)
            """, (int(time.time()), level, module, message))
            db.commit()
        except Exception as e:
            print(f"CRITICAL DB ERROR: Cannot log error: {e}")

    def log_error(self, module, message):
        self.log("ERROR", module, message)

    def log_info(self, module, message):
        self.log("INFO", module, message)