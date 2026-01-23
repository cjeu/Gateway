"""
MQTT consumer for edge analytics.

- Subscribes to raw sensor telemetry
- Passes data to analytics engine
- Writes enriched results to InfluxDB
"""

import json
import yaml
import paho.mqtt.client as mqtt

from analytics_engine import AnalyticsEngine
from influx_writer import InfluxWriter
from mqtt.topics import SENSORS_RAW

CONFIG_PATH = "../config/mqtt_config.yaml"

with open(CONFIG_PATH) as f:
    mqtt_cfg = yaml.safe_load(f)

analytics = AnalyticsEngine()
influx = InfluxWriter()

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    result = analytics.process(payload)
    influx.write(result)

client = mqtt.Client()
client.connect(mqtt_cfg["broker"], mqtt_cfg["port"], 60)
client.subscribe(SENSORS_RAW, qos=1)
client.on_message = on_message

client.loop_forever()
