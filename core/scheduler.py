from kivy.clock import Clock

class Scheduler:
    def __init__(self, state, sensor):
        self.state = state
        self.sensor = sensor

    def start(self):
        Clock.schedule_interval(self.update_temperature, 2)

    def update_temperature(self, dt):
        data = self.sensor.read()
        self.state.temperature_inside = data["temperature"]