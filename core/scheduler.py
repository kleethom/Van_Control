from kivy.clock import Clock


class Scheduler:
    def __init__(self, state, temp_sensor):
        self.state = state
        self.temp_sensor = temp_sensor

    def start(self):
        Clock.schedule_interval(self.update_temperature, 2)

    def update_temperature(self, dt):
        data = self.temp_sensor.read()
        self.state.temperature_inside = data["temperature"]
        print("Temp:", self.state.temperature_inside)
        print("STATE-ID:", id(self.state), self.state.temperature_inside)