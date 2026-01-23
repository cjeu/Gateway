import json
import time
import yaml
import paho.mqtt.client as mqtt

from sensor_models import (
    TemperatureSensor,
    HumiditySensor,
    VibrationSensor,
)
from modes import SimulationMode, apply_mode

CONFIG_PATH = "../config/mqtt_config.yaml"
MODE_PATH = "../config/thresholds.yaml"  # reused for demo simplicity

with open(CONFIG_PATH) as f:
    mqtt_cfg = yaml.safe_load(f)

client = mqtt.Client()
client.connect(mqtt_cfg["broker"], mqtt_cfg["port"], 60)

temp = TemperatureSensor(base=22.0, noise=0.3)
hum = HumiditySensor(base=50.0, noise=1.0)
vib = VibrationSensor(base=0.0, noise=0.05)

def get_mode():
    try:
        with open(MODE_PATH) as f:
            mode = yaml.safe_load(f).get("simulation_mode", "normal")
            return SimulationMode(mode)
    except Exception:
        return SimulationMode.NORMAL

while True:
    mode = get_mode()
    params = apply_mode(mode)

    payload = {
        "temperature": temp.read(fault=params["fault"]),
        "humidity": hum.read(fault=params["fault"]),
        "vibration": vib.read(fault=params["fault"]),
        "mode": mode.value,
        "ts": int(time.time()),
    }

    client.publish(
        mqtt_cfg["topic"],
        json.dumps(payload),
        qos=1,
    )

    time.sleep(mqtt_cfg.get("publish_interval", 1))
