import time
import json
import random
import yaml
from pathlib import Path
import paho.mqtt.client as mqtt

# ---------- Config loading ----------
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"

with open(CONFIG_DIR / "mqtt_config.yaml") as f:
    mqtt_cfg = yaml.safe_load(f)

with open(CONFIG_DIR / "thresholds.yaml") as f:
    thresholds = yaml.safe_load(f)
# -----------------------------------

BROKER = mqtt_cfg["broker"]
PORT = mqtt_cfg["port"]
TOPIC = mqtt_cfg["topic"]
INTERVAL = mqtt_cfg.get("publish_interval", 1)

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

def generate_sensor_data():
    mode = thresholds.get("simulation_mode", "normal")

    temp = random.uniform(20, 25)
    hum = random.uniform(40, 60)
    vib = random.uniform(0.2, 0.6)

    if mode == "fault":
        temp += random.uniform(10, 20)
        vib += random.uniform(2, 4)

    return {
        "temperature": round(temp, 2),
        "humidity": round(hum, 2),
        "vibration": round(vib, 2)
    }

while True:
    payload = generate_sensor_data()
    client.publish(TOPIC, json.dumps(payload))
    print("Published:", payload)
    time.sleep(INTERVAL)
