import yaml
from pathlib import Path
from collections import deque
from influx_writer import write_metrics, close_client
import atexit

# Ensure InfluxDB flushes on exit
atexit.register(close_client)

# ----------------------------
# Base directories
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"

# ----------------------------
# Load thresholds (case-insensitive)
# ----------------------------
with open(CONFIG_DIR / "thresholds.yaml") as f:
    raw_thresholds = yaml.safe_load(f)

# Normalize thresholds keys to lowercase
thresholds = {k.lower(): v for k, v in raw_thresholds.items() if isinstance(v, dict)}

# ----------------------------
# Moving average window
# ----------------------------
WINDOW = 5

# Buffers for metrics (auto-create)
buffers = {}

# ----------------------------
# Process metrics
# ----------------------------
def process_metrics(data: dict):
    """
    Processes incoming sensor metrics:
    - Computes moving average over WINDOW
    - Determines alerts based on thresholds
    - Writes data + alerts to InfluxDB synchronously
    """
    alerts = {}

    for key, value in data.items():
        key_lower = key.lower()

        # Initialize buffer if missing
        if key_lower not in buffers:
            buffers[key_lower] = deque(maxlen=WINDOW)

        # Append value
        buffers[key_lower].append(value)
        avg = sum(buffers[key_lower]) / len(buffers[key_lower])

        # Check threshold if exists
        if key_lower in thresholds:
            max_th = thresholds[key_lower].get("max", None)
            alerts[key_lower] = avg > max_th if max_th is not None else False
        else:
            alerts[key_lower] = False
            print(f"[Analytics] No threshold defined for {key}, skipping alert check")

    # Write to InfluxDB
    write_metrics(data, alerts)
