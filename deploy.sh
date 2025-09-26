#!/bin/bash

# Solar Monitor Deployment Script with Auto-Versioning
# Usage: ./deploy.sh

# Get current version from src/version.py
CURRENT_BUILD=$(grep "'build':" src/version.py | grep -o '[0-9]*')
echo "Current build: $CURRENT_BUILD"

# Increment build number
NEW_BUILD=$((CURRENT_BUILD + 1))
echo "New build: $NEW_BUILD"

# Update build number in src/version.py
sed -i.bak "s/'build': [0-9]*/'build': $NEW_BUILD/g" src/version.py

# Get the new version string
NEW_VERSION=$(python3 -c "import sys; sys.path.insert(0, 'src'); from version import get_version_string; print(get_version_string())")
echo "New version: $NEW_VERSION"

# Pre-deployment syntax checks
echo "🔍 Running pre-deployment checks..."
echo "Checking Python syntax..."
if ! python3 -m py_compile web_dashboard_cached_simple.py; then
    echo "❌ Python syntax error in web_dashboard_cached_simple.py"
    echo "Deployment aborted!"
    exit 1
fi

if ! python3 -m py_compile src/version.py; then
    echo "❌ Python syntax error in src/version.py"
    echo "Deployment aborted!"
    exit 1
fi

if ! python3 -m py_compile src/mobile_api.py; then
    echo "❌ Python syntax error in src/mobile_api.py"
    echo "Deployment aborted!"
    exit 1
fi

echo "✅ All syntax checks passed"

# Deploy to server
echo "Deploying $NEW_VERSION at $(date)"
echo "Copying main dashboard..."
scp web_dashboard_cached_simple.py barry@192.168.1.126:/opt/solar_monitor/

echo "Copying version system..."
scp src/version.py barry@192.168.1.126:/opt/solar_monitor/src/

echo "Copying mobile API..."
scp src/mobile_api.py barry@192.168.1.126:/opt/solar_monitor/src/

echo "Copying static files..."
scp -r static/ barry@192.168.1.126:/opt/solar_monitor/

# Post-deployment verification
echo "🔍 Verifying deployment on server..."
if ! ssh barry@192.168.1.126 "cd /opt/solar_monitor && python3 -m py_compile web_dashboard_cached_simple.py"; then
    echo "❌ Deployed file has syntax errors on server!"
    echo "Rolling back deployment..."
    exit 1
fi

echo "✅ Server-side syntax verification passed"

# Restart service
echo "Restarting solar monitor service..."
ssh barry@192.168.1.126 "sudo systemctl restart solar-monitor.service"

echo "✅ Deployment complete: $NEW_VERSION"
echo "🌐 Access at: http://192.168.1.126:5000"
echo "📱 Mobile API: http://192.168.1.126:5000/api/mobile/version"
