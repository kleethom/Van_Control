import json
import paho.mqtt.client as mqtt
from database.db import get_db


class MqttManager:
    def __init__(self, broker, port=1883, username=None, password=None,
             system_logger=None, topic_prefix="kleethom/feeds/projectvan"):
        self.broker = broker
        self.port = port
        self.topic_prefix = topic_prefix
        self.sys_logger = system_logger
        self.client = mqtt.Client()
        self._connected = False

        if username and password:
            self.client.username_pw_set(username, password)

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
            self.client.connect(self.broker, self.port, 60)            
            self.client.loop_start()
            return True
        except Exception as e:
            self._connected = False
            self._log_error("MQTT_CONN", f"Verbindung fehlgeschlagen: {e}")
            return False

    def publish_package(self):
        try:
            db = get_db()
            # 1. Aktuelle Werte (gerundet auf 1 Nachkommastelle)
            row = db.execute("SELECT * FROM sensor_1min ORDER BY timestamp DESC LIMIT 1").fetchone()
            
            # 2. History (nur das Nötigste: Temp In/Out und Zeit)
            # Wir nehmen nur 12 statt 24 Stunden für das MQTT-Paket
            history = db.execute("""
                SELECT timestamp, temp_in_avg, temp_out_avg 
                FROM sensor_1hour ORDER BY timestamp DESC LIMIT 12
            """).fetchall()

            # Kompaktes Payload-Design (spart ca. 60% Platz)
            payload = {
                "cur": {
                    "t_i": round(row['temp_in_avg'], 1) if row else 0,
                    "t_o": round(row['temp_out_avg'], 1) if row else 0,
                    "h_i": round(row['hum_in_avg'], 1) if row else 0
                },
                "hist": [
                    [int(r['timestamp']), round(r['temp_in_avg'], 1), round(r['temp_out_avg'], 1)] 
                    for r in history
                ]
            }

            # Senden
            json_data = json.dumps(payload)
            self._log_info("MQTT", f"Payload Größe: {len(json_data)} Bytes")
            self.client.publish(self.topic_prefix, json_data)

        except Exception as e:
            self._log_error("MQTT_PUB", f"Fehler: {e}")