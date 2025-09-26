#!/bin/bash

# Solar Monitor Installation Script
# Installs dependencies and sets up the solar monitoring system

echo "Solar Monitor Installation Script"
echo "================================="

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.7"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✓ Python $python_version detected"
else
    echo "✗ Python 3.7 or higher required. Found: $python_version"
    exit 1
fi

# Install system dependencies (if needed)
echo "Installing system dependencies..."

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "Installing pip3..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y python3-pip
    elif command -v brew &> /dev/null; then
        brew install python3
    else
        echo "Please install pip3 manually for your system"
        exit 1
    fi
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

# Create necessary directories
mkdir -p logs
mkdir -p data

# Set permissions
chmod +x solar_monitor.py
chmod +x start.sh

echo ""
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Set up network connection to PVS gateway (see NETWORK_SETUP.md)"
echo "2. Test connection: python3 solar_monitor.py --test-connection"
echo "3. Start monitoring: ./start.sh"
echo ""
echo "For detailed setup instructions, see README.md"
