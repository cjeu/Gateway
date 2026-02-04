#!/bin/bash
# ==============================
# Pi 5 Edge Gateway Demo Starter
# ==============================
# Runs full demo on Raspberry Pi 5:



echo "Starting IoT Edge Gateway Demo"

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Activate venv
source "$PROJECT_ROOT/venv/bin/activate"

# Start Mosquitto if not running
if ! systemctl is-active --quiet mosquitto; then
  echo "🔧 Starting Mosquitto"
  sudo systemctl start mosquitto
fi

# Start InfluxDB if available
if systemctl list-units --type=service | grep -q influxdb; then
  sudo systemctl start influxdb
fi

# Launch services
python "$PROJECT_ROOT/data_generator/sensor_simulator.py" &
SIM_PID=$!

python "$PROJECT_ROOT/edge_analytics/mqtt_consumer.py" &
ANALYTICS_PID=$!

python "$PROJECT_ROOT/web_api/app.py" &
API_PID=$!

echo "✅ Demo running"
echo "Grafana  : http://<pi-ip>:3000"
echo "Web API  : http://<pi-ip>:5000"
echo "Press CTRL+C to stop"

# Graceful shutdown
trap "echo '🛑 Stopping demo'; kill $SIM_PID $ANALYTICS_PID $API_PID" INT
wait
