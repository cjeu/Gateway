"""
Core edge analytics logic.

Implements:
- Rolling averages
- Threshold checks
- Anomaly detection
"""

from collections import deque
from anomaly import is_anomalous
import yaml

THRESHOLD_PATH = "../config/thresholds.yaml"

with open(THRESHOLD_PATH) as f:
    thresholds = yaml.safe_load(f)

WINDOW = 10  # rolling window size

class AnalyticsEngine:
    def __init__(self):
        self.buffers = {
            "temperature": deque(maxlen=WINDOW),
            "humidity": deque(maxlen=WINDOW),
            "vibration": deque(maxlen=WINDOW),
        }

    def process(self, data):
        result = {
            "ts": data["ts"],
            "mode": data["mode"],
            "metrics": {},
            "alerts": {},
        }

        for key in ["temperature", "humidity", "vibration"]:
            value = data[key]
            self.buffers[key].append(value)

            avg = sum(self.buffers[key]) / len(self.buffers[key])
            alert = value > thresholds[key]["max"]
            anomaly = is_anomalous(self.buffers[key], value)

            result["metrics"][key] = {
                "value": value,
                "avg": round(avg, 2),
            }

            result["alerts"][key] = alert or anomaly

        return result
