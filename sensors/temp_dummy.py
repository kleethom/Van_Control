import random

class DummySHT31:
    def read(self):
        return {
            "temperature": 20 + random.random() * 5,
            "humidity": 40 + random.random() * 10
        }