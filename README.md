# Raspberry Pi Edge Gateway Demo

## Overview
This demo turns a Raspberry Pi into a **self-contained industrial edge gateway**.
It ingests sensor telemetry, performs **local analytics**, stores results locally,
and exposes **live dashboards and control APIs** — all on one device. The idea is to envision this as a smart factory solution ingesting live data and helping on floor operators get live input. 

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
- **Grafana** dashboards (Not yet functional)
- Live charts
- Alert states
- Same dashboard scales to many devices

### 4. Control Plane (Web API)
- Toggle simulation modes (normal / fault / noise)
- Update thresholds live
- Health endpoint for monitoring

---

## Architecture Summary

- Python for simulation, analytics, and control
- Mosquitto for MQTT
- InfluxDB for time-series storage
- Grafana for visualization
- Flask for REST control
- Docker for infra services  --> not functional

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
./scripts/start_demo_pi5.sh
Access:

Grafana: http://localhost:3000
InfluxDB: http://localhost:8086
Control API: http://localhost:5000

MQTT: localhost:1883
