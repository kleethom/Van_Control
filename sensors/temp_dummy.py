import random


class TemperatureDummy:
    def read(self):
        return {
            "temperature": round(20 + random.uniform(-2, 2), 1)
        }

class HumidityDummy:
    def read(self):
        return {
            "humidity": round(30 + random.uniform(-3, 3), 1)
        }