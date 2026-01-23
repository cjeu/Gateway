#!/bin/bash
# Stops all services cleanly

pkill -f sensor_simulator.py
pkill -f mqtt_consumer.py
pkill -f app.py
docker-compose -f docker/docker-compose.yml down
