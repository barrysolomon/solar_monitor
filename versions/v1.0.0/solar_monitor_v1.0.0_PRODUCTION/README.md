# Solar Monitor v1.0.0 - Production Release

A professional solar monitoring system for SunPower PVS6 gateways with real-time data collection, beautiful web dashboard, and comprehensive analytics.

## Features

### 📊 **Beautiful Web Dashboard**
- **Overview Page**: Real-time solar production, consumption, and export data
- **Inverters & Panels**: Monitor all 18 inverters with status, power output, and efficiency
- **Analytics**: Interactive charts with Chart.js showing historical data trends
- **System Management**: Comprehensive system monitoring with diagnostics and controls
- **Data Management**: SQL query interface, database tools, and data export

### ⚡ **Real-Time Monitoring**
- Live data collection from SunPower PVS6 gateway
- 21 total devices (18 inverters + 3 monitoring devices)
- Automatic data logging to SQLite database
- Professional gradient card design throughout

### 🔧 **System Management**
- PVS6 gateway diagnostics and recovery tools
- WiFi connection management and reset capabilities
- System temperature, disk usage, and uptime monitoring
- Database statistics and health monitoring
- Service status monitoring for all components

## Installation

### Prerequisites
- Raspberry Pi (tested on Pi 4)
- Python 3.7+
- SunPower PVS6 gateway on local network
- WiFi connection to PVS6 hotspot (SunPower12345)

### Quick Install
```bash
# Clone and setup
git clone <repository>
cd solar_monitor_v1.0.0_PRODUCTION
pip install -r requirements.txt

# Run the application
python app.py
```

### Production Deployment
```bash
# Copy files to Pi
scp -r * pi@your-pi-ip:/opt/solar_monitor/

# Setup systemd services
sudo systemctl enable solar-monitor.service
sudo systemctl enable solar-data-collector.service

# Start services
sudo systemctl start solar-monitor.service
sudo systemctl start solar-data-collector.service
```

## Architecture

### Core Components
- **`app.py`**: Main Flask web application with all routes and APIs
- **`data_collector.py`**: Background service for continuous data collection
- **`pvs_client.py`**: PVS6 gateway communication client
- **`requirements.txt`**: Python dependencies

### API Endpoints
- `/api/current_status` - Real-time system status
- `/api/devices/inverters` - Inverter data and status
- `/api/historical_data` - Historical data for charts
- `/api/system/pvs6-status` - PVS6 gateway diagnostics
- `/api/db/status` - Database health and statistics

### Database Schema
SQLite database (`solar_data.db`) with tables:
- `solar_data`: Time-series production/consumption data
- `device_data`: Device status and metadata

## Configuration

### PVS6 Connection Setup

**Before Installation - Customize Your Settings:**

1. **Find Your PVS6 Serial Number**: Look for the serial number on your PVS6 unit (format: ZT############)

2. **Calculate Your WiFi Password**: 
   - Take the first 3 digits after "ZT" + last 4 digits of serial
   - Example: ZT123456789012345 → Password: 12345

3. **Update Configuration Files**:
   ```bash
   # In app.py, replace YOUR_WIFI_PASSWORD with your calculated password
   sed -i 's/YOUR_WIFI_PASSWORD/your_actual_password/g' app.py
   
   # In app.py, replace YOUR_PVS6_SERIAL with your actual serial number  
   sed -i 's/YOUR_PVS6_SERIAL/your_actual_serial/g' app.py
   ```

**Network Configuration:**
- **SSID**: SunPower12345 (or your PVS6's hotspot name)
- **Password**: YOUR_WIFI_PASSWORD (calculated from your serial)
- **Gateway IP**: 172.27.152.1

### Network Setup
- **Pi WiFi (wlan0)**: Connected to PVS6 hotspot
- **Pi Ethernet (eth0)**: Home network for remote access
- **Web Interface**: http://pi-ip:5000

## Monitoring

### System Health
- All 18 inverters online and producing power (250-430W each)
- Real-time data collection every minute
- Automatic database cleanup and maintenance
- PVS6 connectivity monitoring with auto-recovery

### Performance
- **Database**: ~60 records per hour, auto-managed
- **Memory**: Optimized connection pooling
- **CPU**: Low impact background collection
- **Storage**: Efficient SQLite with automatic cleanup

## Troubleshooting

### Common Issues
1. **PVS6 Offline**: Power cycle the PVS6 unit to restart WiFi hotspot
2. **Database Errors**: Check file permissions (`chown barry:barry solar_data.db*`)
3. **Service Issues**: Restart with `sudo systemctl restart solar-monitor.service`

### Diagnostics
- Use built-in System Management page for diagnostics
- PVS6 Recovery Wizard for connectivity issues
- Database tools for data integrity checks

## Version History

### v1.0.0 (Production Release)
- Complete redesign with modern, professional UI
- Beautiful gradient cards and responsive design
- Interactive Chart.js analytics with multiple time periods
- Comprehensive system monitoring and diagnostics
- All 18 inverters properly monitored and displayed
- Real-time data collection from PVS6 gateway
- Production-ready with clean codebase

## License

MIT License - See LICENSE file for details.

## Support

For issues or questions, check the built-in diagnostics tools or review the system logs:
- Web interface diagnostics: System Management page
- Service logs: `journalctl -u solar-monitor.service`
- Collector logs: `journalctl -u solar-data-collector.service`