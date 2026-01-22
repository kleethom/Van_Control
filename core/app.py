print(">>> core/app.py GELADEN <<<")

from core.state import SystemState
from core.scheduler import Scheduler
from sensors.temp_dummy import TemperatureDummy, HumidityDummy
from gui.gui_app import VanKivyApp

class VanControlApp:
    def __init__(self):
        self.state = SystemState()
        self.sensor = TemperatureDummy()
        self.humidity_sensor = HumidityDummy()
        self.scheduler = Scheduler(self.state, self.sensor, self.humidity_sensor)

    def start(self):
        self.scheduler.start()
        VanKivyApp(self.state).run()