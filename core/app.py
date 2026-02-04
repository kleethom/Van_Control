from core.state import SystemState
from core.scheduler import Scheduler
from sensors.temp_1 import read as inside_read
from sensors.temp_2 import read as outside_read
from sensors.altitude import read as altitude_read
from sensors.level import read as level_read
from gui.gui_app import VanKivyApp

class SensorWrapper:
    def __init__(self, read_func, sensor_obj=None):
        self.read = read_func
        self.sensor = sensor_obj  # Optional: Zugriff auf Rohsensor

class VanControlApp:
    def __init__(self):
        self.state = SystemState()

        inside_sensor = SensorWrapper(inside_read)
        outside_sensor = SensorWrapper(outside_read)
        altitude_sensor = SensorWrapper(altitude_read)
        level_sensor = SensorWrapper(level_read)

        self.sensors = [
            {
                "name": "Inside Sensor",
                "device": inside_sensor,
                "map": {
                    "temperature": "temperature_inside",
                    "humidity": "humidity_inside"
                }
            },
            {
                "name": "Outside Sensor",
                "device": outside_sensor,
                "map": {
                    "temperature": "temperature_outside",
                    "humidity": "humidity_outside"
                }
            },
            {
                "name": "Altitude Sensor",
                "device": altitude_sensor,
                "map": {
                    "pressure": "pressure",
                    "altitude": "altitude"
                }
            },
            {
                "name": "Level Sensor",
                "device": level_sensor,
                "map": {
                    "tilt_x": "tilt_x",
                    "tilt_y": "tilt_y"
                }
            }
        ]

        self.scheduler = Scheduler(self.state, self.sensors)

    def start(self):
        self.scheduler.start()
        VanKivyApp(self.state).run()
