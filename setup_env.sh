#!/bin/bash
# Setup environment configuration on Pi

echo "🔧 Setting up Solar Monitor environment configuration..."

# Create .env file if it doesn't exist
if [ ! -f /opt/solar_monitor/.env ]; then
    echo "📝 Creating .env file from template..."
    cp /opt/solar_monitor/env.template /opt/solar_monitor/.env
    
    # Set secure permissions (readable only by barry user)
    chmod 600 /opt/solar_monitor/.env
    chown barry:barry /opt/solar_monitor/.env
    
    echo "⚠️  IMPORTANT: Edit /opt/solar_monitor/.env with your actual values:"
    echo "   - PVS6_SERIAL_NUMBER"
    echo "   - PVS6_WIFI_PASSWORD"
    echo "   - WEATHER_API_KEY (optional - get free key from openweathermap.org)"
    echo "   - WEATHER_LATITUDE and WEATHER_LONGITUDE for your location"
    echo "   - Other configuration as needed"
else
    echo "✅ .env file already exists"
fi

# Create backups directory
mkdir -p /opt/solar_monitor/backups
chown barry:barry /opt/solar_monitor/backups
chmod 755 /opt/solar_monitor/backups

echo "✅ Environment configuration setup complete!"
echo "📁 Configuration file: /opt/solar_monitor/.env"
echo "🔒 Permissions: 600 (secure, barry user only)"
