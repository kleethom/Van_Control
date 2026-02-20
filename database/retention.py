import time
from database.db import get_db
from config.config import RETENTION_RAW_DAYS, RETENTION_1MIN_DAYS, RETENTION_1HOUR_DAYS, RETENTION_LOGS_DAYS

class RetentionManager:
    def __init__(self):
        self._last_cleanup = 0
        self.cleanup_interval = 3600  # alle 1 Stunde prüfen

    def run(self):
        """Aufgerufen aus Scheduler-Loop"""
        now = time.time()
        if now - self._last_cleanup >= self.cleanup_interval:
            self._cleanup()
            self._last_cleanup = now

    def _cleanup(self):
        db = get_db()

        # sensor_raw: nur letzte 2 Tage behalten
        cutoff = int(time.time()) - RETENTION_RAW_DAYS*24*3600
        db.execute("DELETE FROM sensor_raw WHERE timestamp < ?", (cutoff,))

        # sensor_1min: nur letzte 7 Tage
        cutoff = int(time.time()) - RETENTION_1MIN_DAYS*24*3600
        db.execute("DELETE FROM sensor_1min WHERE timestamp < ?", (cutoff,))

        # sensor_1hour: nur letzte 12 Monate
        cutoff = int(time.time()) - RETENTION_1HOUR_DAYS*24*3600
        db.execute("DELETE FROM sensor_1hour WHERE timestamp < ?", (cutoff,))


        
        cutoff_logs = int(time.time()) - RETENTION_LOGS_DAYS*24*3600
        db.execute("DELETE FROM system_logs WHERE timestamp < ?", (cutoff_logs,))

        # Speicherplatz freigeben (Optional aber empfohlen)
        db.execute("VACUUM")

        db.commit()