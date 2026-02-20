from kivy.config import Config


def setup():
    Config.set("graphics", "fullscreen", "auto")
    Config.set("graphics", "borderless", "1")
    Config.set("graphics", "resizable", "0")
    Config.set("kivy", "keyboard_mode", "systemanddock")
    Config.set("input", "mouse", "mouse,disable_multitouch")


# Datenbank
DB_PATH = "data/van_control.db"

# MQTT
MQTT_BROKER = "192.168.1.50"
MQTT_TOPIC_PREFIX = "van/sensors"


# Speicerdauer Daten
LOG_INTERVAL_RAW = 10        # Sekunden
AGG_INTERVAL_1MIN = 60
AGG_INTERVAL_1HOUR = 3600
AGG_INTERVAL_1DAY = 86400

# Speicherdauer des Logs
RETENTION_LOGS_DAYS = 60


RETENTION_RAW_DAYS = 3
RETENTION_1MIN_DAYS = 7
RETENTION_1HOUR_DAYS = 365