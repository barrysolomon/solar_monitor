#!/bin/bash

# Setup Weather Configuration
echo "Setting up weather configuration..."

# Create .env file from template
cp env.template /opt/solar_monitor/.env

echo "✅ Created /opt/solar_monitor/.env from template"
echo ""
echo "📝 Next steps:"
echo "1. Edit /opt/solar_monitor/.env"
echo "2. Replace 'YOUR_OPENWEATHERMAP_API_KEY' with your actual API key"
echo "3. Update latitude/longitude for your location if needed"
echo "4. Restart the solar monitor service"
echo ""
echo "🔧 To edit the file:"
echo "   sudo nano /opt/solar_monitor/.env"
echo ""
echo "🔄 To restart the service:"
echo "   sudo systemctl restart solar_monitor"
