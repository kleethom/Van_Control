import random


class TemperatureDummy:
    def read(self):
        return {
            "temperature": round(20 + random.uniform(-2, 2), 1)
        }