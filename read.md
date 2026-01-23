# Raspberry Pi Edge Gateway Demo

## Overview
This demo turns a Raspberry Pi into a **self-contained industrial edge gateway**.
It ingests sensor telemetry, performs **local analytics**, stores results locally,
and exposes **live dashboards and control APIs** — all on one device.

Designed for **interviews, client demos, and trade fairs**.
No toy LEDs. Real tools. Real architecture.

---

## What This Demo Shows

### 1. Device Telemetry Ingestion
- Simulated sensors:
  - Temperature
  - Humidity
  - Vibration
- Published via **MQTT**
- Realistic noise + fault injection

### 2. Edge Analytics (Key Value)
- Rolling averages
- Threshold-based alerts
- Simple anomaly detection
- Runs fully offline on the Pi

### 3. Visualization
- **Grafana** dashboards
- Live charts
- Alert states
- Same dashboard scales to many devices

### 4. Control Plane (Web API)
- Toggle simulation modes (normal / fault / noise)
- Update thresholds live
- Health endpoint for monitoring

---

## Why This Matters (Interview Framing)

- Demonstrates **system-level thinking**
- Clear **edge vs cloud responsibility split**
- Uses **industry-standard tools**
- Easy migration path to real sensors
- Scales linearly to thousands of devices

---

## Architecture Summary

- Python for simulation, analytics, and control
- Mosquitto for MQTT
- InfluxDB for time-series storage
- Grafana for visualization
- Flask for REST control
- Docker for infra services

All running locally on one Raspberry Pi.

---

## Project Structure

rpi-edge-gateway-demo/
├─ data_generator/ # Simulated sensors
├─ edge_analytics/ # Local analytics pipeline
├─ web_api/ # Control & configuration API
├─ dashboards/ # Grafana dashboards
├─ mqtt/ # Topic definitions
├─ docker/ # Mosquitto, InfluxDB, Grafana
├─ scripts/ # Start/stop/demo helpers
├─ config/ # MQTT, Influx, thresholds
└─ requirements.txt

yaml
Copy code

---

## Running the Demo

```bash
./scripts/start_all.sh
Access:

Grafana: http://localhost:3000

Control API: http://localhost:5000

MQTT: localhost:1883

Optional remote access:

bash
Copy code
./scripts/expose_ngrok.sh
Live Demo Flow (Recommended)
Open Grafana → normal sensor behavior

POST /mode → fault

Graphs spike, alerts trigger

Explain how this maps to real industrial failures

Extension Ideas
Replace simulator with real sensors

Bridge MQTT to cloud

Add TLS + cert-based auth

OTA updates

Fleet management dashboard