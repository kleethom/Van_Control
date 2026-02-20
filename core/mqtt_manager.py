import json
import paho.mqtt.client as mqtt
from database.db import get_db


class MqttManager:
    def __init__(self, broker, system_logger=None, topic_prefix="van/sensors"):
        self.broker = broker
        self.topic_prefix = topic_prefix
        self.sys_logger = system_logger
        self.client = mqtt.Client()
        self._connected = False

        # Callbacks setzen damit _connected korrekt gepflegt wird
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self._connected = True
            self._log_info("MQTT", "Verbunden mit Broker.")
        else:
            self._connected = False
            self._log_error("MQTT", f"Verbindung abgelehnt, rc={rc}")

    def _on_disconnect(self, client, userdata, rc):
        self._connected = False
        if rc != 0:
            self._log_error("MQTT", f"Unerwartete Trennung, rc={rc}")

    def is_connected(self):
        return self._connected

    def _log_error(self, module, message):
        method = getattr(self.sys_logger, "log_error", None)
        if method:
            method(module, message)
        else:
            print(f"[{module}] MQTT-Fehler: {message}")

    def _log_info(self, module, message):
        method = getattr(self.sys_logger, "log_info", None)
        if method:
            method(module, message)
        else:
            print(f"[{module}] {message}")

    def connect(self):
        try:
            self.client.connect(self.broker, 1883, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            self._connected = False
            self._log_error("MQTT_CONN", f"Verbindung fehlgeschlagen: {e}")
            return False

    def publish_package(self):
        try:
            db = get_db()

            current_row = db.execute(
                "SELECT * FROM sensor_1min ORDER BY timestamp DESC LIMIT 1"
            ).fetchone()

            avg_15min_row = db.execute("""
                SELECT 
                    AVG(temp_in_avg) as temp_in, 
                    AVG(hum_in_avg) as hum_in,
                    AVG(temp_out_avg) as temp_out,
                    AVG(hum_out_avg) as hum_out
                FROM sensor_1min 
                WHERE timestamp >= ?
            """, (int(__import__('time').time()) - 900,)).fetchone()

            history_rows = db.execute("""
                SELECT timestamp, temp_in_avg, temp_out_avg 
                FROM sensor_1hour 
                ORDER BY timestamp DESC LIMIT 24
            """).fetchall()

            payload = {
                "current": dict(current_row) if current_row else {},
                "avg_15min": dict(avg_15min_row) if avg_15min_row else {},
                "history_24h": [dict(row) for row in history_rows]
            }

            self.client.publish(f"{self.topic_prefix}/summary", json.dumps(payload))

        except Exception as e:
            self._log_error("MQTT_PUB", f"Fehler beim Paket-Versand: {e}")