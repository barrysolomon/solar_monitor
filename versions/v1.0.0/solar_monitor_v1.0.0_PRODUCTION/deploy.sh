#!/bin/bash
# Solar Monitor v1.0.0 Production Deployment Script
# Safely deploys the production version without breaking the running system

set -e  # Exit on any error

PI_HOST="barry@192.168.1.126"
REMOTE_PATH="/opt/solar_monitor"
BACKUP_PATH="/opt/solar_monitor/backup_$(date +%Y%m%d_%H%M%S)"

echo "🚀 Solar Monitor v1.0.0 Production Deployment"
echo "=============================================="

# Create backup on Pi
echo "📦 Creating backup of current system..."
ssh $PI_HOST "sudo mkdir -p $BACKUP_PATH"
ssh $PI_HOST "sudo cp $REMOTE_PATH/web_dashboard_cached_simple.py $BACKUP_PATH/ 2>/dev/null || true"
ssh $PI_HOST "sudo cp $REMOTE_PATH/simple_data_collector.py $BACKUP_PATH/ 2>/dev/null || true"
ssh $PI_HOST "sudo cp $REMOTE_PATH/pvs_client.py $BACKUP_PATH/ 2>/dev/null || true"

# Deploy new files
echo "📤 Deploying production files..."
scp app.py $PI_HOST:$REMOTE_PATH/web_dashboard_cached_simple.py
scp data_collector.py $PI_HOST:$REMOTE_PATH/simple_data_collector.py
scp pvs_client.py $PI_HOST:$REMOTE_PATH/
scp requirements.txt $PI_HOST:$REMOTE_PATH/

# Set permissions
echo "🔐 Setting permissions..."
ssh $PI_HOST "sudo chown barry:barry $REMOTE_PATH/*.py"
ssh $PI_HOST "sudo chmod +x $REMOTE_PATH/*.py"

# Test the deployment
echo "🧪 Testing deployment..."
ssh $PI_HOST "python3 -m py_compile $REMOTE_PATH/web_dashboard_cached_simple.py"
ssh $PI_HOST "python3 -m py_compile $REMOTE_PATH/simple_data_collector.py"
ssh $PI_HOST "python3 -m py_compile $REMOTE_PATH/pvs_client.py"

# Restart services
echo "🔄 Restarting services..."
ssh $PI_HOST "sudo systemctl restart solar-monitor.service"
ssh $PI_HOST "sudo systemctl restart solar-data-collector.service"

# Wait and verify services
echo "⏳ Waiting for services to start..."
sleep 5

# Check service status
echo "✅ Checking service status..."
ssh $PI_HOST "sudo systemctl is-active solar-monitor.service" || {
    echo "❌ Web service failed to start! Rolling back..."
    ssh $PI_HOST "sudo cp $BACKUP_PATH/web_dashboard_cached_simple.py $REMOTE_PATH/ 2>/dev/null || true"
    ssh $PI_HOST "sudo systemctl restart solar-monitor.service"
    exit 1
}

ssh $PI_HOST "sudo systemctl is-active solar-data-collector.service" || {
    echo "❌ Collector service failed to start! Rolling back..."
    ssh $PI_HOST "sudo cp $BACKUP_PATH/simple_data_collector.py $REMOTE_PATH/ 2>/dev/null || true"
    ssh $PI_HOST "sudo systemctl restart solar-data-collector.service"
    exit 1
}

# Test web interface
echo "🌐 Testing web interface..."
curl -s "http://192.168.1.126:5000/api/version/current" | grep -q "1.0.0" || {
    echo "❌ Version check failed! Rolling back..."
    ssh $PI_HOST "sudo cp $BACKUP_PATH/* $REMOTE_PATH/ 2>/dev/null || true"
    ssh $PI_HOST "sudo systemctl restart solar-monitor.service"
    ssh $PI_HOST "sudo systemctl restart solar-data-collector.service"
    exit 1
}

echo "✅ Deployment successful!"
echo "🎉 Solar Monitor v1.0.0 is now running!"
echo ""
echo "📊 Access your dashboard at: http://192.168.1.126:5000"
echo "🔧 Backup saved at: $BACKUP_PATH"
echo ""
echo "🏆 Welcome to Solar Monitor v1.0.0 Production!"
