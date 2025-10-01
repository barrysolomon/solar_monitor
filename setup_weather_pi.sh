#!/bin/bash

# Setup Weather Configuration on Pi
echo "Setting up weather configuration on Pi..."

# SSH into Pi and create .env file
ssh barry@192.168.1.126 << 'EOF'
# Create .env file from template
sudo cp /opt/solar_monitor/env.template /opt/solar_monitor/.env

# Set proper permissions
sudo chown barry:barry /opt/solar_monitor/.env

# Update the .env file with weather configuration
# Note: You'll need to replace YOUR_OPENWEATHERMAP_API_KEY with your actual API key
sudo sed -i 's/YOUR_OPENWEATHERMAP_API_KEY/your_actual_api_key_here/g' /opt/solar_monitor/.env

# Restart the service
sudo systemctl restart solar-monitor.service

echo "✅ Weather configuration setup complete!"
echo "📝 Next step: Edit /opt/solar_monitor/.env and replace 'your_actual_api_key_here' with your OpenWeatherMap API key"
echo "🔄 Then run: sudo systemctl restart solar-monitor.service"
EOF
