import time
import config.config as config
from core.state import SystemState
from core.scheduler import Scheduler
from sensors.temp_1 import read as inside_read
from sensors.temp_2 import read as outside_read
from sensors.altitude import read as altitude_read
from sensors.level import read as level_read
from gui.gui_app import VanKivyApp
from database.schema import init_schema
from database.db import get_db
from database.logger import SensorLogger, SystemLogger
from database.aggregator import Aggregator
from database.retention import RetentionManager
from core.mqtt_manager import MqttManager

class SensorWrapper:
    def __init__(self, read_func, sensor_obj=None):
        self.read = read_func
        self.sensor = sensor_obj  # Optional: Zugriff auf Rohsensor

class VanControlApp:
    def __init__(self):
        self.state = SystemState()
        self.sys_logger = SystemLogger()
        self._session_id = None
        
        self.mqtt = MqttManager(
            broker=config.MQTT_BROKER,
            port=config.MQTT_PORT,
            username=config.ADAFRUIT_AIO_USERNAME,
            password=config.ADAFRUIT_AIO_KEY,
            system_logger=self.sys_logger
        )
        self.logger = SensorLogger(system_logger=self.sys_logger)
        self.aggregator = Aggregator()
        self.retention_manager = RetentionManager()

        inside_sensor = SensorWrapper(inside_read)
        outside_sensor = SensorWrapper(outside_read)
        altitude_sensor = SensorWrapper(altitude_read)
        level_sensor = SensorWrapper(level_read)

        self.sensors = [
            {
                "name": "Inside Sensor",
                "device": inside_sensor,
                "map": {"temperature": "temperature_inside", "humidity": "humidity_inside"}
            },
            {
                "name": "Outside Sensor",
                "device": outside_sensor,
                "map": {"temperature": "temperature_outside", "humidity": "humidity_outside"}
            },
            {
                "name": "Altitude Sensor",
                "device": altitude_sensor,
                "map": {"pressure": "pressure", "altitude": "altitude"}
            },
            {
                "name": "Level Sensor",
                "device": level_sensor,
                "map": {"tilt_x": "tilt_x", "tilt_y": "tilt_y"}
            }
        ]

        self.logger = SensorLogger()
        self.aggregator = Aggregator()
        self.retention_manager = RetentionManager()

        self.scheduler = Scheduler(
            self.state, 
            self.sensors, 
            self.logger, 
            self.sys_logger, 
            self.aggregator, 
            self.retention_manager, 
            mqtt_client=self.mqtt
        )


    def start(self):
        init_schema()

        self.mqtt.connect()

        db = get_db()
        cursor = db.execute(
            "INSERT INTO system_sessions (start_ts) VALUES (?)",
            (int(time.time()),))
        db.commit()
        self._session_id = cursor.lastrowid

        self.scheduler.start()
        VanKivyApp(self.state).run()
        self._on_stop()

    def _on_stop(self):
        """Wird beim Beenden aufgerufen"""
        try:
            if self._session_id:
                db = get_db()
                db.execute(
                    "UPDATE system_sessions SET end_ts = ? WHERE id = ?",
                    (int(time.time()), self._session_id)
                )
                db.commit()
                self.sys_logger.log_info("APP", "Session sauber beendet.")
        except Exception as e:
            print(f"[APP] Fehler beim Session-Close: {e}")

        try:
            self.mqtt.client.loop_stop()
            self.mqtt.client.disconnect()
        except Exception:
            pass