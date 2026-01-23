#!/bin/bash
# Starts full edge demo stack

docker-compose -f docker/docker-compose.yml up -d
python3 data_generator/sensor_simulator.py &
python3 edge_analytics/mqtt_consumer.py &
python3 web_api/app.py &
