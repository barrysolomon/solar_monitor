#!/bin/bash

# Solar Monitor Startup Script
# This script sets up and starts the solar monitoring system

echo "Starting Solar Monitor..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "solar_monitor.py" ]; then
    echo "Error: Please run this script from the solar_monitor directory"
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt
fi

# Test PVS connection first
echo "Testing PVS gateway connection..."
python3 solar_monitor.py --test-connection

if [ $? -ne 0 ]; then
    echo "Error: Cannot connect to PVS gateway."
    echo "Please check your network setup (see NETWORK_SETUP.md)"
    exit 1
fi

echo "PVS connection successful! Starting Solar Monitor..."

# Start the application
python3 solar_monitor.py

echo "Solar Monitor stopped."
