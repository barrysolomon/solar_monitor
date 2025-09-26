# Solar Monitor v1.0.0.36+ - Quick Start Guide 🏆

**🌞 Professional Solar Monitoring in 15 Minutes - PRODUCTION RELEASE!**

Get your SunPower local monitoring up and running with a single command. **Comprehensive database management, real-time monitoring, advanced analytics, and system management!**

![Solar Monitor Dashboard](docs/images/dashboard-v1.0.0-preview.png)
*Professional dashboard with comprehensive database management, real-time updates, and advanced system monitoring*

## ⚡ Super Quick Start (15 minutes total)

### Step 1: Prepare Raspberry Pi (10 minutes)
1. **Flash SD Card**: Use Raspberry Pi Imager with Raspberry Pi OS Lite
2. **Enable SSH**: Set username `barry` and password during imaging  
3. **Boot & Connect**: Connect Pi to your network via Ethernet
4. **Find IP**: Check router or use `nmap -sn 192.168.1.0/24`

### Step 2: One-Command Installation (3 minutes)
SSH to your Pi and run:

```bash
git clone https://github.com/barrysolomon/solar_monitor.git
cd solar_monitor
sudo ./install.sh
```

**🏆 This installs the PRODUCTION VERSION v1.0.0.36+ with:**
- ✅ **Overview Dashboard**: Real-time production, consumption, and performance metrics
- ✅ **Panels Page**: Individual inverter monitoring with status and performance (renamed from "Devices")
- ✅ **Analytics**: Streamlined Power Flow Analysis charts (Update Chart button removed)
- ✅ **Data Mgmt**: Complete SQL query interface with AG-Grid display and chart visualization (moved from Analytics)
- ✅ **System Management**: Comprehensive system monitoring with database statistics and maintenance (reorganized)
- ✅ **Enhanced Database Health**: Proper VACUUM time tracking with system metadata table
- ✅ **Professional UI**: Clean, modern interface with reorganized page structure
- ✅ **Comprehensive APIs**: 25+ endpoints for all system data and controls

### Step 3: Access Dashboard (2 minutes)
Open browser: `http://YOUR_PI_IP:5000/`

## 🎉 What You Get (v1.0.0.36+)

### 📊 Professional Interface (Reorganized)
- **Overview**: Real-time dashboard with performance summary and status indicators
- **Panels**: Individual inverter monitoring with power, efficiency, and temperature (renamed from "Inverters & Panels")
- **Analytics**: Streamlined Power Flow Analysis charts only (SQL interface moved to Data Mgmt)
- **Data Mgmt**: Complete SQL query interface with AG-Grid display, chart visualization, and export tools
- **System**: Comprehensive system monitoring with database statistics, maintenance, and PVS6 diagnostics
- **Help**: Up-to-date documentation reflecting the new page structure

### 🔧 Advanced Features
- **Web-based Configuration**: Set up PVS6 credentials and system settings via web interface
- **System Diagnostics**: Built-in PVS6 connection testing and WiFi reset tools
- **Database Tools**: Advanced SQL queries, table browsing, and maintenance functions
- **Status Monitoring**: Real-time system health indicators in navigation bar
- **Auto-refresh**: Page-aware refresh rates with manual controls

### 📈 Data & Analytics
- **Interactive Charts**: Chart.js with zoom, hover, and multiple time periods
- **Net Export Analysis**: Centered graphs showing import/export with color coding
- **Performance Metrics**: Peak production, consumption, and efficiency tracking
- **Historical Data**: SQLite storage with comprehensive querying capabilities
- **Data Export**: CSV/JSON export for all data with filtering options

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

## 📚 Need More Help?

### Detailed Guides
- **[PROJECT_SETUP.md](PROJECT_SETUP.md)** - Complete Raspberry Pi setup guide
- **[DESKTOP_SETUP.md](DESKTOP_SETUP.md)** - Complete desktop computer setup guide
- **[APPROACH_COMPARISON.md](APPROACH_COMPARISON.md)** - Compare all setup options

### Hardware & Network
- **[HARDWARE_CHECKLIST.md](HARDWARE_CHECKLIST.md)** - Detailed shopping list
- **[NETWORK_SETUP.md](NETWORK_SETUP.md)** - Network configuration help
- **[PVS6_PORTS_GUIDE.md](PVS6_PORTS_GUIDE.md)** - Understanding PVS6 ports

### Troubleshooting
- **[FAQ.md](FAQ.md)** - Frequently asked questions
- **[BEGINNER_GUIDE.md](BEGINNER_GUIDE.md)** - Non-technical user guide

## ⚠️ Important Notes

### PVS6 Port Usage
- **Always use the BLUE port** (LAN/Installer) on your PVS6
- **Never use the WHITE port** (WAN/Internet) for local monitoring
- The BLUE port provides full API access to solar data

### Network Requirements
- PVS6 creates an isolated network (172.27.153.x)
- You need a bridge (Pi or router) to access it from your home network
- Direct WiFi connection to PVS6 won't work for monitoring

### Cost Comparison
- **Raspberry Pi**: ~$100 (dedicated device, most reliable)
- **Desktop Computer**: ~$8 (uses existing hardware, budget option)
- **See APPROACH_COMPARISON.md for complete analysis**

## 🎯 Quick Decision Guide

### Choose Raspberry Pi If:
- You want a **dedicated monitoring device**
- You want **maximum reliability** and 24/7 operation
- You're comfortable with **basic Linux commands**
- You want **professional, clean setup**

### Choose Desktop Computer If:
- You want to **save money** (~$92 savings)
- You want **quickest setup** (1-2 hours vs 2-3 hours)
- You're comfortable with **Python and software installation**
- You want to **use existing hardware**

## 🚀 Ready to Start?

1. **Choose your approach** (Pi recommended, Desktop for budget)
2. **Follow the steps** above for your chosen approach
3. **Reference detailed guides** if you need help
4. **Enjoy your local solar monitoring!**

**Need help?** Check the [FAQ](FAQ.md) or [Beginner Guide](BEGINNER_GUIDE.md) for additional support.
