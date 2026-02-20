import time
from kivy.clock import Clock
from config.config import MQTT_PUBLISH_INTERVAL_MIN

class Scheduler:
    def __init__(self, state, sensors, logger=None,sys_logger=None, aggregator=None, retention_manager=None, mqtt_client=None):
        self.state = state
        self.sensors = sensors
        self.logger = logger
        self.sys_logger = sys_logger
        self.aggregator = aggregator
        self.retention_manager = retention_manager
        self.mqtt_client = mqtt_client
        
        
        self._last_mqtt_publish = 0
        self._last_raw_log = 0
        self._last_retention = 0


    def start(self):
        Clock.schedule_interval(self.update_all, 2)

    def update_all(self, dt):

        now = time.time()

        for sensor in self.sensors:
            sensor_name = sensor.get("name", "Sensor")

            try:
                # Sensor auslesen
                data = sensor["device"].read()

                # Leere oder ungültige Daten abfangen
                if not isinstance(data, dict):
                    print(f"[{sensor_name}] Ungültige Daten: {data}")
                    continue

                # State aktualisieren
                for key, state_attr in sensor["map"].items():
                    if key in data:
                        setattr(self.state, state_attr, data[key])

                # Debug-Ausgabe
                print(f"[{sensor_name}] {data}")

                # --- Speziell für Level Sensor (BNO055) ---
                if (
                    sensor_name == "Level Sensor"
                    and hasattr(sensor["device"], "sensor")
                    and sensor["device"].sensor is not None
                ):
                    try:
                        sys_c, gyro_c, accel_c, mag_c = (
                            sensor["device"].sensor.calibration_status
                        )

                        if sys_c < 3 or gyro_c < 3 or accel_c < 3 or mag_c < 3:
                            print(
                                f"[Level Sensor] Nicht kalibriert: "
                                f"SYS={sys_c} GYR={gyro_c} ACC={accel_c} MAG={mag_c}"
                            )
                    except Exception as e:
                        method = getattr(self.sys_logger, "log_error", None)
                        if method:
                            method("LEVEL_SENSOR", f"Kalibrier-Status konnte nicht gelesen werden: {e}")

            except Exception as e:
            # WICHTIG: verhindert App-Absturz
                method = getattr(self.sys_logger, "log_error", None)
                if method:
                    method(sensor_name, f"Sensor-Lese-Fehler: {e}")




        # Datenbank
        if self.logger and now - self._last_raw_log >= 10:
            try:
                self.logger.log(self.state)
                self._last_raw_log = now
            except Exception as e:
                method = getattr(self.sys_logger, "log_error", None)
                if method: method("Logger", f"Fehler: {e}")

        if self.aggregator:
            try:
                self.aggregator.aggregate()
            except Exception as e:
                method = getattr(self.sys_logger, "log_error", None)
                if method: method("Aggregator", f"Fehler: {e}")

        #MQTT:
        if self.mqtt_client:
            if now - self._last_mqtt_publish >= MQTT_PUBLISH_INTERVAL_MIN * 60:
                try:
                    if not self.mqtt_client.is_connected():
                        self._log_error("MQTT", "Keine Verbindung – versuche Reconnect...")
                        self.mqtt_client.connect()

                    if self.mqtt_client.is_connected():
                        self.mqtt_client.publish_package()
                        self._last_mqtt_publish = now
                    else:
                        # Trotzdem Timer zurücksetzen, damit nicht sofort nochmal versucht wird
                        self._last_mqtt_publish = now
                except Exception as e:
                    self._log_error("MQTT", f"Fehler: {e}")
                    self._last_mqtt_publish = now

        if self.retention_manager and now - self._last_retention >= 3600:
            try:
                self.retention_manager.run()
                self._last_retention = now
            except Exception as e:
                self._log_error("RetentionManager", f"Fehler: {e}")

    def _log_error(self, module, message):
        method = getattr(self.sys_logger, "log_error", None)
        if method:
            method(module, message)
        else:
            print(f"[{module}] {message}")

        