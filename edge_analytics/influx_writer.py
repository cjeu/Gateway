"""
InfluxDB writer.

Writes:
- Raw values
- Rolling averages
- Alert states
"""

from influxdb_client import InfluxDBClient, Point
import yaml

CONFIG_PATH = "../config/influx_config.yaml"

with open(CONFIG_PATH) as f:
    cfg = yaml.safe_load(f)

class InfluxWriter:
    def __init__(self):
        self.client = InfluxDBClient(
            url=cfg["url"],
            token=cfg["token"],
            org=cfg["org"],
        )
        self.write_api = self.client.write_api()
        self.bucket = cfg["bucket"]

    def write(self, data):
        for metric, values in data["metrics"].items():
            point = (
                Point("edge_metrics")
                .tag("metric", metric)
                .tag("mode", data["mode"])
                .field("value", values["value"])
                .field("avg", values["avg"])
                .field("alert", int(data["alerts"][metric]))
                .time(data["ts"])
            )

            self.write_api.write(
                bucket=self.bucket,
                record=point,
            )
