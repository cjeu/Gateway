"""
InfluxDB writer.

Writes:
- Raw values
- Rolling averages
- Alert states
"""

from influxdb_client import InfluxDBClient, Point
import yaml
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR=BASE_DIR/"config"

with open(CONFIG_DIR / "influx_config.yaml","r") as f: 
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
