import random
import math
import time

class BaseSensor:
    def __init__(self, base, noise):
        self.base = base
        self.noise = noise
        self.start_time = time.time()

    def noise_term(self):
        return random.uniform(-self.noise, self.noise)

class TemperatureSensor(BaseSensor):
    def read(self, fault=False):
        drift = math.sin((time.time() - self.start_time) / 60) * 0.5
        value = self.base + drift + self.noise_term()
        if fault:
            value += random.uniform(5, 10)
        return round(value, 2)

class HumiditySensor(BaseSensor):
    def read(self, fault=False):
        value = self.base + self.noise_term()
        if fault:
            value -= random.uniform(10, 20)
        return round(max(0, min(100, value)), 2)

class VibrationSensor(BaseSensor):
    def read(self, fault=False):
        value = abs(self.noise_term())
        if fault:
            value += random.uniform(2, 5)
        return round(value, 3)
