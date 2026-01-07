from core.state import SystemState
from core.scheduler import Scheduler
from sensors.temp_dummy import TemperatureDummy
from gui.gui_app import VanKivyApp

class VanControlApp:
    def __init__(self):
        self.state = SystemState()
        self.sensor = TemperatureDummy()
        self.scheduler = Scheduler(self.state, self.sensor)

    def start(self):
        self.scheduler.start()
        VanKivyApp(self.state).run()