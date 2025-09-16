# Solar Monitor - SunPower Local Monitoring System

**The Complete Beginner's Guide to Local SunPower Monitoring**

A complete, step-by-step solution for monitoring your SunPower solar system locally, replacing the now-defunct SunPower cloud service. **Perfect for frustrated SunPower users who are tired of paying $10/month for features that used to be free!** **No technical background required** - just follow the guide!

## Features

### Core Monitoring
- **Real-time Monitoring**: Live solar production data from your PVS gateway
- **Historical Data**: Store and visualize historical production data
- **Web Dashboard**: Beautiful, responsive web interface
- **Device Management**: Monitor individual inverters and meters
- **Data Export**: Export data for analysis
- **Offline Operation**: Works completely locally, no internet required

### Advanced Features
- **Home Assistant Integration**: Monitor solar data in your smart home
- **Grafana Dashboards**: Professional-grade monitoring and alerting
- **Multiple Hardware Options**: Raspberry Pi, ESP32, or cloud deployment
- **Automation Support**: Create alerts and automations based on solar data
- **Mobile Access**: Access your data from any device
- **Community Integration**: Works with existing solar monitoring projects

### Bluetooth Features (Pi 4+)
- **Direct Mobile Connection**: Connect to Pi via Bluetooth without WiFi
- **Offline Data Sync**: Collect data when internet is down
- **Wireless Sensors**: Integrate Bluetooth temperature and weather sensors
- **Smart Home Automation**: Control devices based on solar production
- **Push Notifications**: Real-time alerts sent directly to your phone
- **Data Backup**: Wireless backup of monitoring data
- **Peer-to-Peer Sharing**: Share data between multiple Pi units

## 🛒 Recommended Hardware

### Choose Your Pi Configuration

#### **Option 1: Basic Setup (2GB) - $75**
- **[Raspberry Pi 4 (2GB)](https://amzn.to/your-pi-2gb-link)** - $35-45
- **[32GB MicroSD Card](https://amzn.to/your-sd-link)** - $8-12  
- **[Official USB-C Power Supply (5V/3A)](https://www.amazon.com/Official-Connector-Raspberry-XYGStudy-PI-PSU-5V3A-USB-C-US/dp/B0CYZ7FPH4)** - $10-15
- **[Cat6 Ethernet Cable (50ft)](https://www.amazon.com/Cable-Matters-Snagless-Ethernet-Black/dp/B007NZHQDY)** - $12-20
- **[Pi Case with Fan](https://amzn.to/your-case-link)** - $10-15

**Best for:** Simple monitoring, budget-conscious users

#### **Option 2: Advanced Setup (4GB) - $95**
- **[Raspberry Pi 4 (4GB)](https://amzn.to/your-pi-4gb-link)** - $55-65
- **[64GB MicroSD Card](https://amzn.to/your-sd-64gb-link)** - $12-18
- **[USB-C Power Supply with Switch](https://www.amazon.com/Adapter-Raspberry-Version-Supply-Charger/dp/B08523QCT6)** - $12-18
- **[Cat6 Ethernet Cable (50ft)](https://www.amazon.com/Cable-Matters-Snagless-Ethernet-Black/dp/B007NZHQDY)** - $12-20
- **[Pi Case with Fan](https://amzn.to/your-case-link)** - $10-15

**Best for:** Home Assistant integration, Grafana, Bluetooth features

#### **Option 3: Professional Setup (8GB) - $115**
- **[Raspberry Pi 4 (8GB)](https://amzn.to/your-pi-8gb-link)** - $75-85
- **[128GB MicroSD Card](https://amzn.to/your-sd-128gb-link)** - $18-25
- **[Premium USB-C Power Supply](https://www.amazon.com/Miuzei-Raspberry-Compatible-Charger-Adapter/dp/B09WYRFWMW)** - $12-18
- **[Outdoor Cat6 Ethernet Cable (50ft)](https://www.amazon.com/Maximm-Cat6-Outdoor-Cable-50ft/dp/B0745ZQ1KR)** - $18-25
- **[Premium Pi Case with OLED](https://amzn.to/your-premium-case-link)** - $25-35

**Best for:** Complete smart home hub, multiple projects, advanced automation

### Optional Accessories
- **[MicroSD Card Reader](https://amzn.to/your-reader-link)** - $5-10
- **[Heat Sinks](https://amzn.to/your-heatsink-link)** - $5-8
- **[Bluetooth Sensors](https://amzn.to/your-bluetooth-sensors-link)** - $15-25
- **[Weather Station](https://amzn.to/your-weather-station-link)** - $30-50

### 💰 Cost Comparison vs SunStrong

| Feature | SunStrong | Your Local System | Annual Savings |
|---------|-----------|-------------------|----------------|
| **Basic Monitoring** | $10/month | **FREE** | **$120/year** |
| **Historical Data** | $10/month | **FREE** | **$120/year** |
| **Data Ownership** | ❌ No | **✅ Complete** | **Priceless** |
| **No Internet Required** | ❌ No | **✅ Works Offline** | **Reliability** |
| **Custom Features** | ❌ Limited | **✅ Unlimited** | **Flexibility** |

**Total Annual Savings: $120+ per year** (plus complete data ownership and reliability!)

## ⚠️ Important Disclaimer

**This project is a compilation of information and approaches gathered from various community sources and research, plus the author's imagination and musings of possibilities (both practical and not). It has NOT been personally tested by the author yet, but testing is planned.**

### What This Project Is
- **Compiled information** from multiple community sources
- **Theoretical implementation** based on proven concepts
- **Educational resource** for understanding SunPower local monitoring
- **Creative exploration** of possibilities and potential solutions
- **Community-driven approach** building on existing work

### What This Project Is NOT
- **Personally tested** by the author
- **Guaranteed to work** in all scenarios
- **Official SunPower documentation**
- **Professional installation guide**

### 🚨 Comprehensive Legal Disclaimer
**I will not be held liable for ANY damage, injury, warranty voiding, system failures, electrical fires, data loss, or any other consequences that result from:**

- **Following any instructions** in this project
- **Attempting any modifications** to your solar system
- **Using any code or scripts** provided
- **Making any electrical connections** or modifications
- **Opening or modifying** your PVS6 or any solar equipment
- **Installing any hardware** suggested in this project
- **Doing anything stupid** with any part of this project

**You are 100% responsible for your own actions and decisions.** This is educational material only. Use at your own risk. If you break something, electrocute yourself, void warranties, or burn down your house, that's on you, not me.

**Seriously, don't be stupid. If you're not sure what you're doing, don't do it.**

### Sources and Inspiration
This project builds upon the work of:

#### Primary Contributors
- **[Scott Gruby](https://blog.gruby.com/2020/04/28/monitoring-a-sunpower-solar-system/)** - "Monitoring a SunPower Solar System" blog post (April 2020)
- **[Nelson Minar](https://nelsonslog.wordpress.com/2021/12/02/getting-local-access-to-sunpower-pvs6-data/)** - Comprehensive PVS6 documentation and monitoring system setup
- **[Gino Ledesma](https://github.com/ginoledesma/sunpower-pvs-exporter)** - sunpower-pvs-exporter Prometheus integration
- **[Kiel Koleson](https://gist.github.com/koleson/5c719620039e0282976a8263c068e85c)** - Extensive PVS6 technical notes and documentation
- **[Kevin Fleming](https://github.com/kpfleming/esphome-sunpower)** - ESPHome components for SunPower PVS devices
- **[Hasherati](https://github.com/hasherati/solar)** - Alternative SunPower PVS6 query methods and approaches

#### Community Projects
- **[GitHub community projects](https://github.com/search?q=sunpower+monitoring)** - Various SunPower monitoring implementations
- **[Home Assistant integrations](https://www.home-assistant.io/integrations/)** - Community-developed HA components
- **[ESPHome components](https://esphome.io/)** - Experimental SunPower data collection
- **[Prometheus/Grafana exporters](https://prometheus.io/docs/instrumenting/exporters/)** - Professional monitoring approaches

### Theoretical Basis
The approaches described here are **theoretically sound** because they:
- **Use documented API endpoints** that have been tested by others
- **Follow established networking principles** for PVS6 access
- **Build upon proven hardware configurations** (Raspberry Pi, Powerline adapters)
- **Implement standard software patterns** (Python, Flask, SQLite, etc.)

### Use at Your Own Risk
- **Test thoroughly** before deploying in production
- **Follow electrical safety guidelines** when working with solar equipment
- **Backup your data** before making changes
- **Consult professionals** for electrical work if needed
- **Verify compatibility** with your specific PVS6 model and firmware

### Contributing and Testing
If you successfully implement this system:
- **Share your experience** - What worked, what didn't
- **Report issues** - Help improve the documentation
- **Submit improvements** - Enhance the guides and code
- **Test on different systems** - Verify compatibility across setups

**Remember**: This is a community-driven project based on research and compilation of existing work. Your mileage may vary!


## 🚀 Quick Start

### Option 1: Raspberry Pi Setup (RECOMMENDED)
**Total Time: 2-3 hours | Cost: ~$100 | Difficulty: Medium**

#### Step 1: Buy Hardware (15 minutes)
- Raspberry Pi 4 (4GB) - $65
- 32GB MicroSD card - $10  
- Power supply - $10
- Ethernet cable (25-50 feet) - $15-25
- Case - $10
- **Total: ~$110**

#### Step 2: Set Up Raspberry Pi (30 minutes)
1. Download Raspberry Pi Imager
2. Flash SD card with Raspberry Pi OS Lite
3. Enable SSH and set password
4. Boot Pi and find it on your network

#### Step 3: Connect to Your PVS Gateway (45 minutes)
1. Run Ethernet cable from outdoor PVS6 to your garage/house
2. Connect cable to PVS6 "LAN" or "Installer" port
3. Configure Pi network settings
4. Test connection: `ping 172.27.153.1`

#### Step 4: Install Software (30 minutes)
1. Copy this code to your Pi
2. Install Python dependencies
3. Configure the application
4. Test: `python3 solar_monitor.py --test-connection`

#### Step 5: Access Your Dashboard (5 minutes)
- Open web browser
- Go to `http://YOUR_PI_IP:5000`
- See your solar data in real-time!

**That's it! You now have local solar monitoring.**

*See [PROJECT_SETUP.md](RASPBERRY_PI_SETUP.md) for detailed instructions*

---

### Option 2: Desktop Computer Setup
**Total Time: 1-2 hours | Cost: ~$8 | Difficulty: Easy**

#### Step 1: Find Hardware (5 minutes)
- Old WiFi router with Ethernet ports - $0 (you already own this!)
- Ethernet cable (10-25 feet) - ~$8
- Your computer - $0 (you already own this!)
- **Total: ~$8**

#### Step 2: Set Up Router Bridge (30 minutes)
1. Connect PVS6 BLUE port to router WAN port via Ethernet
2. Power on router and connect to its WiFi (temporarily)
3. Access router web interface (usually 192.168.1.1)
4. Configure router WiFi to connect to your home network
5. **Important**: Your computer stays connected to your normal home WiFi

#### Step 3: Install Software (45 minutes)
1. Install Python 3.7+ on your computer
2. Download the solar monitoring software
3. Install dependencies: `pip install -r requirements.txt`
4. Test PVS6 connection: `python solar_monitor.py --test-connection`

#### Step 4: Run Monitoring Software (30 minutes)
1. Start data collection: `python solar_monitor.py --mode collector`
2. Start web dashboard: `python solar_monitor.py --mode dashboard`
3. Access dashboard at http://localhost:5000
4. Verify data collection and charts

#### Step 5: Set Up Auto-Start (Optional)
1. Configure as Windows service, macOS launchd, or Linux systemd
2. Set up automatic startup on computer boot
3. Monitor logs and performance

**🎉 Congratulations! You now have local solar monitoring for just $8!**

*See [DESKTOP_SETUP.md](DESKTOP_SETUP.md) for detailed instructions*

## 📚 Complete Documentation

### 🚀 Getting Started
- **[Quick Start Guide](QUICKSTART.md)** - **Quick start guide with both setup options**
- **[Beginner's Guide](docs/guides/BEGINNER_GUIDE.md)** - Complete guide for non-technical users
- **[FAQ](docs/guides/FAQ.md)** - Frequently asked questions and troubleshooting
- **[Approach Comparison](docs/APPROACH_COMPARISON.md)** - **Compare all setup options and get recommendations**

### 🔧 Hardware & Setup
- **[Hardware Checklist](docs/hardware/HARDWARE_CHECKLIST.md)** - Detailed shopping list and purchase guide
- **[Hardware Comparison](docs/hardware/HARDWARE_COMPARISON.md)** - Compare Pi vs ESP32 vs other options
- **[Raspberry Pi Setup](RASPBERRY_PI_SETUP.md)** - **Raspberry Pi setup instructions (~$100)**
- **[Network Setup](docs/guides/NETWORK_SETUP.md)** - Network configuration and troubleshooting
- **[PVS6 Ports Guide](docs/hardware/PVS6_PORTS_GUIDE.md)** - Understanding BLUE vs WHITE Ethernet ports
- **[Powerline Setup](docs/hardware/POWERLINE_SETUP.md)** - Use Powerline adapters instead of Ethernet cables

### 🌐 Network Solutions
- **[Desktop Setup](DESKTOP_SETUP.md)** - Desktop computer setup (~$8)
- **[Old Router Setup](OLD_ROUTER_SETUP.md)** - Use old router as bridge (~$8)
- **[WiFi Dongle Solutions](docs/wifi/WIFI_DONGLE_SOLUTION.md)** - No-cable WiFi options
- **[Power Tapping Guide](docs/wifi/PVS6_POWER_TAPPING.md)** - Tap PVS6 internal power ⚠️

### 🔗 Integrations
- **[Home Assistant Integration](docs/HOME_ASSISTANT_INTEGRATION.md)** - Integrate with Home Assistant
- **[Grafana Integration](docs/GRAFANA_INTEGRATION.md)** - Professional monitoring with Grafana
- **[Bluetooth Setup](docs/bluetooth/BLUETOOTH_SETUP.md)** - Bluetooth integration and mobile app connectivity
- **[Community Integration](docs/COMMUNITY_INTEGRATION.md)** - Connect with community projects

### 📱 Mobile Development
- **[Mobile App Project](docs/mobile/MOBILE_APP_PROJECT.md)** - **iOS/Android mobile app development**
- **[Mobile App Development](docs/mobile/MOBILE_APP_DEVELOPMENT.md)** - **Complete mobile app development guide**

### 🛒 Business & Legal
- **[Legal Considerations](docs/legal/LEGAL_CONSIDERATIONS.md)** - Business and legal analysis
- **[Disclaimer](docs/legal/DISCLAIMER.md)** - Legal notice and project status
- **[Acknowledgments](docs/legal/ACKNOWLEDGMENTS.md)** - Complete credits and references

### 📊 Tools & Resources
- **[SEO Meta Tags](docs/SEO_META_TAGS.md)** - **SEO optimization for search engines**
- **[Scott Gruby's Blog](https://blog.gruby.com/2020/04/28/monitoring-a-sunpower-solar-system/)** - Original PVS6 API research
- **[Nelson Minar's Documentation](https://nelsonslog.wordpress.com/2021/12/02/getting-local-access-to-sunpower-pvs6-data/)** - PVS6 access methods
- **[Gino Ledesma's Prometheus Exporter](https://github.com/ginoledesma/sunpower-pvs-exporter)** - Professional monitoring
- **[Kiel Koleson's Technical Notes](https://gist.github.com/koleson/5c719620039e0282976a8263c068e85c)** - PVS6 specifications
- **[Kevin Fleming's ESPHome Components](https://github.com/kpfleming/esphome-sunpower)** - ESP32 integration
- **[Hasherati's Solar Project](https://github.com/hasherati/solar)** - Alternative approaches

### 🐍 Source Code (`src/` Directory)
- **solar_monitor.py** - Main application launcher
- **pvs_client.py** - PVS6 API client
- **data_collector.py** - Data collection service
- **database.py** - Database management
- **web_dashboard.py** - Web dashboard interface
- **config.py** - Configuration settings
- **bluetooth_monitor.py** - Bluetooth monitoring and automation
- **mobile_api.py** - Mobile app API endpoints

### Project Information
- **[DISCLAIMER.md](docs/legal/DISCLAIMER.md)** - Important disclaimer and legal notice
- **[ENHANCEMENT_OPPORTUNITIES.md](docs/ENHANCEMENT_OPPORTUNITIES.md)** - Community projects and future enhancements

## Configuration

Edit `src/config.py` to customize settings:

```python
# PVS Gateway Configuration
PVS_IP = '172.27.153.1'  # Change if your PVS has different IP
PVS_PORT = '80'

# Polling Configuration
POLL_INTERVAL_SECONDS = 30  # How often to collect data

# Web Dashboard Configuration
WEB_HOST = "0.0.0.0"  # Allow access from other devices
WEB_PORT = 5000
```

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   PVS Gateway   │───▶│  Data Collector  │───▶│   SQLite DB     │
│  (172.27.153.1) │    │  (pvs_client.py)  │    │ (solar_data.db) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Browser   │◀───│  Web Dashboard   │◀───│   Data Storage  │
│  (localhost:5000)│    │ (web_dashboard.py)│    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## File Structure

```
Projects/solar_monitor/
├── solar_monitor.py      # Main application launcher
├── config.py             # Configuration settings
├── pvs_client.py         # PVS gateway API client
├── database.py           # Database management
├── data_collector.py     # Data collection service
├── web_dashboard.py      # Web dashboard server
├── templates/
│   └── dashboard.html    # Web dashboard template
├── requirements.txt      # Python dependencies
├── NETWORK_SETUP.md      # Network configuration guide
├── install.sh            # Installation script
├── start.sh              # Startup script
└── README.md            # This file
```

## API Endpoints

The web dashboard provides several API endpoints:

- `GET /api/current_status` - Current system status
- `GET /api/power_chart?hours=24` - Power production chart data
- `GET /api/energy_chart?days=7` - Daily energy chart data
- `GET /api/system_summary` - System summary statistics
- `GET /api/devices` - List of devices and their status
- `GET /api/health` - System health check

## Data Storage

Data is stored in SQLite database (`solar_data.db`) with the following tables:

- `solar_data` - Individual device readings
- `system_status` - Overall system status

Data is automatically cleaned up to prevent database from growing too large (configurable in `config.py`).

## Troubleshooting

### Connection Issues

1. **Cannot reach PVS gateway (172.27.153.1)**
   - Check network cable connection
   - Verify your computer's IP is in same subnet
   - Try rebooting PVS gateway

2. **API returns 403/500 errors**
   - Reboot PVS gateway (unplug for 30 seconds)
   - Wait 2-3 minutes for full startup

3. **No data in dashboard**
   - Check data collector is running
   - Verify database file exists
   - Check logs for errors

### Performance Issues

1. **High CPU usage**
   - Increase `POLL_INTERVAL_SECONDS` in config.py
   - Reduce `MAX_DATA_POINTS` for smaller database

2. **Large database file**
   - Run data cleanup: `python -c "from database import SolarDatabase; SolarDatabase().cleanup_old_data()"`

## Advanced Usage

### Running as Service (Linux/macOS)

Create a systemd service or use launchd to run automatically:

```bash
# Create service file
sudo nano /etc/systemd/system/solar-monitor.service

[Unit]
Description=Solar Monitor Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/solar_monitor
ExecStart=/usr/bin/python3 solar_monitor.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl enable solar-monitor.service
sudo systemctl start solar-monitor.service
```

### Remote Access

To access dashboard from other devices:

1. Set `WEB_HOST = "0.0.0.0"` in config.py
2. Access via `http://YOUR_IP:5000`
3. Consider setting up reverse proxy for HTTPS

### Data Export

Export data for analysis:

```python
from database import SolarDatabase
import pandas as pd

db = SolarDatabase()
data = db.get_latest_data(hours=24*30)  # Last 30 days
df = pd.DataFrame(data)
df.to_csv('solar_data_export.csv')
```

## Contributing

This is a community-driven project. Feel free to:

- Report issues
- Suggest improvements
- Submit pull requests
- Share your setup experiences

## Acknowledgments

This project builds upon the work of Scott Gruby and the SunPower community. See `ACKNOWLEDGMENTS.md` for detailed credits and references.

## License

This project is open source. Use at your own risk.

## Support

- Check `NETWORK_SETUP.md` for network troubleshooting
- Review logs in `solar_monitor.log`
- Test connection with `python solar_monitor.py --test-connection`

## Disclaimer

This software is not affiliated with SunPower Corporation. Use at your own risk. Always follow electrical safety guidelines when working with solar equipment.
