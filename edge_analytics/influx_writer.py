import yaml
from pathlib import Path
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# ----------------------------
# Base directories
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"

# ----------------------------
# Load InfluxDB config
# ----------------------------
with open(CONFIG_DIR / "influx_config.yaml") as f:
    influx_cfg = yaml.safe_load(f)

# ----------------------------
# Initialize client with synchronous write
# ----------------------------
client = InfluxDBClient(
    url=influx_cfg["url"],
    token=influx_cfg["token"],
    org=influx_cfg["org"]
)

write_api = client.write_api(write_options=SYNCHRONOUS)
bucket = influx_cfg["bucket"]

# ----------------------------
# Function to write metrics
# ----------------------------
def write_metrics(data: dict, alerts: dict):
    """
    Writes sensor data to InfluxDB.
    :param data: dict of {metric_name: value}
    :param alerts: dict of {metric_name: alert_flag}
    """
    if not data:
        print("[InfluxDB] No data to write.")
        return

    print("[InfluxDB] Preparing to write data:", data)
    print("[InfluxDB] With alerts:", alerts)

    for k, v in data.items():
        if v is None:
            print(f"[InfluxDB] Skipping {k} because value is None")
            continue
        try:
            # Ensure numeric values for fields
            point = (
                Point("sensor_data")
                .field(k, float(v))
                .tag("alert", str(alerts.get(k, False)))
            )
            write_api.write(bucket=bucket, record=point)
            print(f"[InfluxDB] Wrote {k}={v}")
        except Exception as e:
            print(f"[InfluxDB ERROR] Failed to write {k}={v}: {e}")

# ----------------------------
# Function to close client
# ----------------------------
def close_client():
    """Flush and close InfluxDB client properly."""
    write_api.__del__()  # ensures synchronous flush
    client.close()
