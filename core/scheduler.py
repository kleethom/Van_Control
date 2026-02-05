import time
from kivy.clock import Clock

class Scheduler:
    def __init__(self, state, sensors, logger=None, aggregator=None, retention_manager=None):
        self.state = state
        self.sensors = sensors
        self.logger = logger
        self.aggregator = aggregator
        self.retention_manager = retention_manager

        self._last_raw_log = 0


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
                        print(f"[Level Sensor] Kalibrier-Status Fehler: {e}")

            except Exception as e:
                # WICHTIG: verhindert App-Absturz
                print(f"[{sensor_name}] Sensor-Fehler: {e}")


        # Datenbank
        if self.logger and now - self._last_raw_log >= 10:  # Logge alle 10 Sekunden
            try:
                self.logger.log(self.state)
                self._last_raw_log = now
            except Exception as e:
                print(f"[Logger] Fehler beim Loggen: {e}")

        if self.aggregator:
            try:
                self.aggregator.aggregate()
            except Exception as e:
                print(f"[Aggregator] Fehler bei Aggregation: {e}")

        if self.retention_manager:
            try:
                self.retention_manager.run()
            except Exception as e:
                print(f"[RetentionManager] Fehler bei Retention: {e}")