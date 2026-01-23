# mqtt/topics.py
"""
Central MQTT topic definitions for the edge gateway demo.

Why this exists:
- Avoids hard-coded topic strings scattered across the codebase
- Makes it easy to evolve from simulated → real sensors
- Clean talking point for system design interviews
"""

# Root namespace for the demo
ROOT = "edge"

# Device / gateway identifier (can be extended to multiple gateways)
GATEWAY_ID = "rpi-01"

# ===== Telemetry Topics =====
# Raw sensor data published by the simulator
SENSORS_RAW = f"{ROOT}/{GATEWAY_ID}/sensors/raw"

# Processed / enriched data after edge analytics
SENSORS_PROCESSED = f"{ROOT}/{GATEWAY_ID}/sensors/processed"

# ===== Alert Topics =====
# Threshold or anomaly alerts generated at the edge
ALERTS = f"{ROOT}/{GATEWAY_ID}/alerts"

# ===== Control Topics =====
# Control messages sent to the edge (mode switch, resets, etc.)
CONTROL = f"{ROOT}/{GATEWAY_ID}/control"

# ===== Utility =====
def all_topics():
    """
    Returns all MQTT topics used by the demo.
    Useful for debugging or wildcard subscriptions.
    """
    return [
        SENSORS_RAW,
        SENSORS_PROCESSED,
        ALERTS,
        CONTROL,
    ]
