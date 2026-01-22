from kivy.clock import Clock


class Scheduler:
    def __init__(self, state, temp_sensor, humidity_sensor):
        self.state = state
        self.temp_sensor = temp_sensor
        self.humidity_sensor = humidity_sensor

    def start(self):
        Clock.schedule_interval(self.update_temperature, 2)
        Clock.schedule_interval(self.update_humidity, 2)

    def update_temperature(self, dt):
        data = self.temp_sensor.read()
        self.state.temperature_inside = data["temperature"]
        print("Temp:", self.state.temperature_inside)

#        print("STATE-ID:", id(self.state), self.state.temperature_inside)

    def update_humidity(self, dt):
        data = self.humidity_sensor.read()
        self.state.humidity_inside = data["humidity"]
        print("Humidity:", self.state.humidity_inside)