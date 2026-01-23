#!/bin/bash
# ==============================
# Pi 5 Edge Gateway Demo Starter
# ==============================
# Runs full demo on Raspberry Pi 5:
# - Checks Python & Docker
# - Starts Docker services (Mosquitto, InfluxDB, Grafana)
# - Starts Python simulator, analytics, and Flask API
# - Optionally exposes Grafana via ngrok
# ==============================

# --- 1. Check Python ---
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found. Install Python3 before running."
    exit 1
fi

PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if (( $(echo "$PY_VER < 3.11" | bc -l) )); then
    echo "[WARNING] Python version < 3.11. Proceeding but some packages may fail."
fi

# --- 2. Check Docker ---
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker not installed. Install Docker for ARM before running."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "[ERROR] docker-compose not installed. Install docker-compose for ARM."
    exit 1
fi

# --- 3. Activate virtual environment ---
if [ ! -d "venv" ]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# --- 4. Start Docker stack ---
echo "[INFO] Starting Docker services..."
docker-compose -f docker/docker-compose.yml up -d

# Wait a few seconds for services to initialize
sleep 5

# --- 5. Start Python components ---
echo "[INFO] Starting sensor simulator..."
nohup python3 data_generator/sensor_simulator.py > logs/simulator.log 2>&1 &

echo "[INFO] Starting edge analytics..."
nohup python3 edge_analytics/mqtt_consumer.py > logs/analytics.log 2>&1 &

echo "[INFO] Starting Flask Web API..."
nohup python3 web_api/app.py > logs/api.log 2>&1 &

echo "[INFO] Demo started!"
echo "Grafana: http://localhost:3000"
echo "Web API: http://localhost:5000"

# --- 6. Optional ngrok ---
read -p "Expose Grafana via ngrok? (y/n): " NGROK
if [[ "$NGROK" == "y" ]]; then
    if ! command -v ngrok &> /dev/null; then
        echo "[ERROR] ngrok not installed. Install ngrok to continue."
    else
        echo "[INFO] Starting ngrok tunnel for Grafana..."
        ngrok http 3000
    fi
fi
