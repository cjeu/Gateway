import json
import yaml
from pathlib import Path
import paho.mqtt.client as mqtt
from analytics_engine import process_metrics

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"

with open(CONFIG_DIR / "mqtt_config.yaml") as f:
    mqtt_cfg = yaml.safe_load(f)

BROKER = mqtt_cfg["broker"]
PORT = mqtt_cfg["port"]
TOPIC = mqtt_cfg["topic"]

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    process_metrics(data)

client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC)

print("MQTT consumer started")
client.loop_forever()
