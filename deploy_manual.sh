#!/bin/bash

echo "Manual deployment script"
echo "Copying files to server..."

# Copy main files
scp web_dashboard_cached_simple.py barry@192.168.1.126:/opt/solar_monitor/
scp src/version.py barry@192.168.1.126:/opt/solar_monitor/src/
scp src/mobile_api.py barry@192.168.1.126:/opt/solar_monitor/src/

# Copy static files
scp -r static/ barry@192.168.1.126:/opt/solar_monitor/

# Restart service
ssh barry@192.168.1.126 "sudo systemctl restart solar-monitor.service"

echo "Deployment complete"
